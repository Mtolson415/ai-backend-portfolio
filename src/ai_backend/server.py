"""Authenticated synthetic tool API with metadata-only request records."""
import hmac
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import secrets
import time
from .core import Principal, ToolError, Workspace, load_knowledge

MAX_BODY = 8192

def token_principals():
    alpha = os.environ.get('AI_ALPHA_TOKEN', '')
    beta = os.environ.get('AI_BETA_TOKEN', '')
    if any(len(x) < 32 or not x.isascii() for x in (alpha, beta)) or hmac.compare_digest(alpha, beta):
        raise ValueError('Two distinct ASCII authentication tokens of at least 32 characters are required')
    return [(alpha, Principal('alpha-user', frozenset({'alpha'}), frozenset({'knowledge.search','files.read','files.write_output'}))),
            (beta, Principal('beta-reader', frozenset({'beta'}), frozenset({'knowledge.search','files.read'})))]

def create_server(address, workspace, knowledge, credentials, audit=None):
    class Handler(BaseHTTPRequestHandler):
        server_version = 'AIBackendReference'
        sys_version = ''
        timeout = 5

        def log_message(self, *args):
            pass

        def reply(self, status, body):
            data = json.dumps(body, ensure_ascii=False).encode('utf-8')
            self.send_response(status)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(data)))
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == '/health': self.reply(200, {'status':'ok','mode':'synthetic-reference'})
            else: self.reply(404, {'error':'Unknown route'})

        def do_POST(self):
            started = time.monotonic()
            request_id = secrets.token_hex(8)
            principal, project, status, body = None, None, 500, {'error':'Request failed'}
            operation = {'/v1/knowledge/search':'knowledge.search','/v1/files/read':'files.read','/v1/files/write-output':'files.write_output'}.get(self.path,'unknown')
            try:
                headers = self.headers.get_all('Authorization') or []
                supplied = headers[0][7:] if len(headers)==1 and headers[0].startswith('Bearer ') else ''
                for expected, candidate in credentials:
                    if supplied.isascii() and hmac.compare_digest(supplied, expected): principal=candidate
                if principal is None:
                    status,body=401,{'error':'Authentication required'}
                elif operation == 'unknown':
                    status,body=404,{'error':'Unknown route'}
                else:
                    lengths = self.headers.get_all('Content-Length') or []
                    if self.headers.get('Transfer-Encoding') or len(lengths)!=1: raise ToolError()
                    try: length=int(lengths[0])
                    except ValueError: raise ToolError() from None
                    if length < 0: raise ToolError()
                    if length > MAX_BODY:
                        status,body=413,{'error':'Request too large'}
                    else:
                        if self.headers.get_content_type() != 'application/json': raise ToolError()
                        raw=self.rfile.read(length)
                        if len(raw)!=length: raise ToolError()
                        try: args=json.loads(raw)
                        except (ValueError,UnicodeError): raise ToolError() from None
                        if not isinstance(args,dict): raise ToolError()
                        project=args.get('project')
                        if operation=='knowledge.search': body=knowledge.search(principal,project,args.get('query'))
                        elif operation=='files.read': body=workspace.read(principal,project,args.get('path'))
                        else: body=workspace.write_output(principal,project,args.get('path'),args.get('text'))
                        status=200
            except ToolError as exc:
                status,body=exc.status,{'error':exc.message}
            except (TimeoutError,ConnectionError):
                status,body=408,{'error':'Request timed out'}
            except Exception:
                status,body=500,{'error':'Request failed'}
            finally:
                record={'request_id':request_id,'principal':principal.name if principal else None,
                        'operation':operation,'status':status,'elapsed_ms':round((time.monotonic()-started)*1000,2)}
                if audit is not None: audit(record)
            self.reply(status,{**body,'request_id':request_id})

    return ThreadingHTTPServer(address,Handler)

def main():
    credentials=token_principals()
    workspace=Workspace(os.environ.get('WORKSPACE_ROOT','/data/workspaces'))
    knowledge=load_knowledge(os.environ.get('KNOWLEDGE_FILE','/app/examples/knowledge.json'))
    server=create_server(('0.0.0.0',8080),workspace,knowledge,credentials,
                         audit=lambda record: print(json.dumps(record),flush=True))
    server.serve_forever()

if __name__=='__main__': main()
