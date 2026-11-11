"""Read-only official upstream evidence collection. No deployment or account mutations."""
import base64, concurrent.futures, csv, datetime, json, pathlib, re, subprocess, urllib.request, urllib.error, time

ROOT = pathlib.Path(__file__).resolve().parent
token = subprocess.run(['gh', 'auth', 'token'], capture_output=True, text=True, check=True).stdout.strip()
headers = {'Authorization': 'Bearer ' + token, 'Accept': 'application/vnd.github+json', 'User-Agent': 'Portfolio-Research'}

def api(path):
    req = urllib.request.Request('https://api.github.com/' + path, headers=headers)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=35) as response:
                return json.load(response)
        except urllib.error.HTTPError as exc:
            if exc.code in (404, 403, 451): return {'error': str(exc.code)}
            if attempt == 2: return {'error': str(exc.code)}
        except Exception as exc:
            if attempt == 2: return {'error': type(exc).__name__}
        time.sleep(attempt + 1)

def collect(row):
    repo = row['repository']
    meta = api('repos/' + repo)
    if 'error' in meta:
        return {**row, 'lookup_error': meta['error']}
    canonical = meta['full_name']
    release = api('repos/' + canonical + '/releases/latest')
    readme = api('repos/' + canonical + '/readme')
    body = ''
    if readme.get('encoding') == 'base64':
        body = base64.b64decode(readme.get('content', '')).decode('utf-8', errors='replace')
    evidence = []
    terms = re.compile(r'docker|compose|container|self.host|licen[sc]e|secur|sandbox|deprecat|archiv', re.I)
    for number, line in enumerate(body.splitlines(), 1):
        if terms.search(line) and line.strip() and len(evidence) < 14:
            evidence.append({'line': number, 'text': line[:450]})
    license_info = meta.get('license') or {}
    result = {**row, 'canonical_repository': canonical, 'official_url': meta['html_url'],
              'description': meta.get('description'), 'archived': meta.get('archived'),
              'disabled': meta.get('disabled'), 'default_branch': meta.get('default_branch'),
              'pushed_at': meta.get('pushed_at'), 'license_spdx': license_info.get('spdx_id', 'Unknown'),
              'latest_release': release.get('tag_name'), 'release_published_at': release.get('published_at'),
              'release_url': release.get('html_url'), 'release_lookup_error': release.get('error'),
              'readme_url': readme.get('html_url'), 'readme_blob_sha': readme.get('sha'),
              'readme_lookup_error': readme.get('error'), 'readme_evidence': evidence,
              'checked_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    (ROOT / 'evidence' / (canonical.replace('/', '__') + '.md')).write_text(body, encoding='utf-8')
    return result

if __name__ == '__main__':
    (ROOT / 'evidence').mkdir(exist_ok=True)
    with (ROOT / 'catalog-seed.tsv').open(encoding='utf-8', newline='') as stream:
        rows = list(csv.DictReader(stream, delimiter='\t'))
    output = []
    existing = {}
    if (ROOT / 'catalog-evidence.json').exists():
        existing = {x['repository']: x for x in json.loads((ROOT / 'catalog-evidence.json').read_text(encoding='utf-8')) if not x.get('lookup_error')}
    def cached_collect(row):
        return {**existing[row['repository']], **row} if row['repository'] in existing else collect(row)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for index, result in enumerate(pool.map(cached_collect, rows), 1):
            output.append(result)
            if index % 20 == 0: print(f'Checked {index}/{len(rows)} official repositories', flush=True)
    (ROOT / 'catalog-evidence.json').write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({'entries': len(output), 'categories': len(set(x['category'] for x in output)),
                      'lookup_errors': [{k:x.get(k) for k in ['name','repository','lookup_error']} for x in output if x.get('lookup_error')],
                      'archived': [x['name'] for x in output if x.get('archived')],
                      'license_review': [x['name'] for x in output if x.get('license_spdx') in ('NOASSERTION','Unknown')]}, indent=2), flush=True)
