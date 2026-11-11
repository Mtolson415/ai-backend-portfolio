import concurrent.futures, datetime, json, pathlib, re, base64
from collect_evidence import ROOT, api

path = ROOT / 'catalog-evidence.json'
rows = json.loads(path.read_text(encoding='utf-8'))

def enrich(row):
    if row.get('lookup_error'):
        if row['name'] == 'Forgejo':
            row.update(official_url='https://forgejo.org/docs/latest/admin/installation/docker/',
                       canonical_repository='codeberg.org/forgejo/forgejo', license_spdx='GPL-3.0-or-later',
                       license_source='https://forgejo.org/faq/', latest_release='v17.0.1 (documentation channel)',
                       release_url='https://forgejo.org/docs/latest/admin/installation/docker/',
                       metadata_note='GitHub lookup is inapplicable; official Docker documentation and FAQ checked through web research. Source-host API and archive state not verified.',
                       documentation_verified=True)
        return row
    canonical = row['canonical_repository']
    content = api('repos/' + canonical + '/contents')
    paths = []
    if isinstance(content, list):
        for item in content:
            if re.search(r'docker|compose|container|deploy|helm|licen[sc]e|copying', item['name'], re.I):
                paths.append({'path': item['path'], 'url': item['html_url'], 'type': item['type'], 'sha': item['sha']})
    row['deployment_and_license_paths'] = paths
    if row.get('license_spdx') in ('NOASSERTION', 'Unknown'):
        license_doc = api('repos/' + canonical + '/license')
        if license_doc.get('encoding') == 'base64':
            text = base64.b64decode(license_doc['content']).decode('utf-8', errors='replace')
            target = ROOT / 'evidence' / (canonical.replace('/', '__') + '.LICENSE.txt')
            target.write_text(text, encoding='utf-8')
            row['license_source'] = license_doc.get('html_url')
            row['license_excerpt'] = text[:2400]
    return row

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    enriched = list(pool.map(enrich, rows))
path.write_text(json.dumps(enriched, indent=2, ensure_ascii=False), encoding='utf-8')
print(json.dumps({'entries': len(enriched), 'with_root_deployment_paths': sum(bool(x.get('deployment_and_license_paths')) for x in enriched), 'documented_non_github': [x['name'] for x in enriched if x.get('documentation_verified')]}, indent=2))
