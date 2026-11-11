"""Application policy and Linux descriptor-relative workspace operations.

This is a reference service, not an arbitrary-code sandbox or network firewall.
"""
from dataclasses import dataclass
import errno
import json
import os
from pathlib import Path
import re
import secrets
import stat

MAX_FILE_BYTES = 65536

class ToolError(Exception):
    status = 400
    message = 'Invalid request'

class Denied(ToolError):
    status = 403
    message = 'Operation denied'

class Missing(ToolError):
    status = 404
    message = 'Resource not found'

class Conflict(ToolError):
    status = 409
    message = 'Output already exists'

class TooLarge(ToolError):
    status = 413
    message = 'Size limit exceeded'

@dataclass(frozen=True)
class Principal:
    name: str
    projects: frozenset[str]
    capabilities: frozenset[str]

def authorize(principal, project, capability):
    if not isinstance(project, str) or not re.fullmatch(r'[a-z][a-z0-9-]{0,31}', project):
        raise ToolError()
    if project not in principal.projects or capability not in principal.capabilities:
        raise Denied()

def parts_for(path):
    if not isinstance(path, str) or not path or len(path) > 512:
        raise ToolError()
    parts = path.split('/')
    if any(x in ('', '.', '..') for x in parts) or any(c in path for c in ('\\', ':', '\x00')):
        raise Denied()
    return parts

class Workspace:
    def __init__(self, root):
        self.root = Path(root)

    def _parent(self, project, parts):
        # Every directory lookup uses an already-open directory, prohibiting symlink traversal.
        flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
        fd = os.open(self.root, flags)
        try:
            for name in [project, *parts[:-1]]:
                child = os.open(name, flags, dir_fd=fd)
                os.close(fd)
                fd = child
            return fd
        except BaseException:
            os.close(fd)
            raise

    @staticmethod
    def _translate(exc):
        if isinstance(exc, FileNotFoundError): raise Missing() from None
        if isinstance(exc, FileExistsError): raise Conflict() from None
        if exc.errno in (errno.ELOOP, errno.ENOTDIR, errno.EACCES, errno.EPERM): raise Denied() from None
        raise ToolError() from None

    def read(self, principal, project, path):
        authorize(principal, project, 'files.read')
        parts = parts_for(path)
        parent = None
        try:
            parent = self._parent(project, parts)
            fd = os.open(parts[-1], os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK, dir_fd=parent)
            with os.fdopen(fd, 'rb') as stream:
                info = os.fstat(stream.fileno())
                if not stat.S_ISREG(info.st_mode): raise Denied()
                if info.st_size > MAX_FILE_BYTES: raise TooLarge()
                data = stream.read(MAX_FILE_BYTES + 1)
                if len(data) > MAX_FILE_BYTES: raise TooLarge()
            return {'project': project, 'path': path, 'text': data.decode('utf-8')}
        except OSError as exc:
            self._translate(exc)
        except UnicodeError:
            raise ToolError() from None
        finally:
            if parent is not None: os.close(parent)

    def write_output(self, principal, project, path, text):
        authorize(principal, project, 'files.write_output')
        parts = parts_for(path)
        if len(parts) < 2 or parts[0] != 'outputs': raise Denied()
        if not isinstance(text, str): raise ToolError()
        data = text.encode('utf-8')
        if len(data) > MAX_FILE_BYTES: raise TooLarge()
        parent, temp = None, None
        try:
            parent = self._parent(project, parts)
            temp = '.job-' + secrets.token_hex(16)
            fd = os.open(temp, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600, dir_fd=parent)
            with os.fdopen(fd, 'wb') as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            # Create without following or overwriting any existing destination, including symlinks.
            os.link(temp, parts[-1], src_dir_fd=parent, dst_dir_fd=parent, follow_symlinks=False)
            return {'project': project, 'path': path, 'bytes': len(data)}
        except OSError as exc:
            self._translate(exc)
        finally:
            if parent is not None:
                if temp is not None:
                    try: os.unlink(temp, dir_fd=parent)
                    except FileNotFoundError: pass
                os.close(parent)

class Knowledge:
    def __init__(self, documents):
        self.documents = documents

    def search(self, principal, project, query):
        authorize(principal, project, 'knowledge.search')
        if not isinstance(query, str) or not query.strip() or len(query) > 500:
            raise ToolError()
        terms = set(re.findall(r'\w+', query.casefold()))
        if not terms: raise ToolError()
        ranked = []
        for doc in self.documents:
            # Filter authorization before scoring or returning text.
            if doc['project'] != project: continue
            words = set(re.findall(r'\w+', (doc['title']+' '+doc['text']).casefold()))
            score = len(terms & words)
            if score:
                ranked.append((score, doc))
        ranked.sort(key=lambda item: (-item[0], item[1]['id']))
        return {'project': project, 'method': 'lexical-baseline', 'matches': [
            {'id': doc['id'], 'title': doc['title'], 'text': doc['text'], 'source': doc['source'], 'score': score}
            for score, doc in ranked[:3]]}

def load_knowledge(path):
    return Knowledge(json.loads(Path(path).read_text(encoding='utf-8')))
