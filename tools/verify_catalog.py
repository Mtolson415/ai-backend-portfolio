"""Validate generated catalog consistency and local documentation links."""
import json
from pathlib import Path
import re
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
R = ROOT / 'docs/research/2026-11-11'

class CatalogParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.capture = False
        self.embedded = ''
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'script' and attrs.get('id') == 'catalog-data': self.capture = True
    def handle_endtag(self, tag):
        if tag == 'script': self.capture = False
    def handle_data(self, data):
        if self.capture: self.embedded += data

rows = json.loads((R/'catalog-evidence.json').read_text(encoding='utf-8'))
assert len(rows) == 181 and len({x['category'] for x in rows}) == 16
assert len({x['name'] for x in rows}) == len(rows)
assert all(x.get('official_url','').startswith('https://') for x in rows)
assert all(x.get('readme_blob_sha') or x.get('documentation_verified') for x in rows)
assert all(not x.get('archived') or x['priority'] == 'Avoid-new' for x in rows)
assert all('license_excerpt' not in x for x in rows)
assert all(sum(len(v['text'].split()) for v in x.get('readme_evidence',[])) <= 85 for x in rows)
parser = CatalogParser()
parser.feed((R/'catalog.html').read_text(encoding='utf-8'))
assert json.loads(parser.embedded) == rows
missing=[]
for path in ROOT.rglob('*.md'):
    if '.git' in path.parts or 'evidence' in path.parts: continue
    for raw in re.findall(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
        target=raw.split('#')[0]
        if not target or '://' in target or target.startswith('mailto:'): continue
        if not (path.parent/target).exists(): missing.append(str(path.relative_to(ROOT))+': '+target)
assert not missing, missing
print('PASS: 181 entries, 16 categories, evidence identifiers, archived flags, short excerpts, HTML data and local documentation links')
