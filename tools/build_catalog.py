"""Build the dated Markdown and offline HTML catalog from public evidence."""
from collections import Counter
import html
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
RESEARCH = ROOT / 'docs/research/2026-11-11'
SOURCE = RESEARCH / 'catalog-evidence.json'

LICENSE_NOTES = {
    'Open WebUI': 'Custom Open WebUI license; inspect exact release terms',
    'Dify': 'Modified Apache terms; additional conditions',
    'Browserless': 'SSPL or commercial terms',
    'Onyx': 'MIT core plus separately licensed enterprise directories',
    'pgvector': 'PostgreSQL-style license; inspect source license',
    'Weaviate': 'BSD core plus separately licensed wl directory',
    'LiteLLM': 'MIT core plus separately licensed enterprise directory',
    'Langfuse': 'MIT core plus separately licensed enterprise directories',
    'Arize Phoenix': 'Elastic License 2.0',
    'Authentik': 'Mixed core, enterprise and documentation licensing',
    'n8n': 'Fair-code/custom terms; inspect exact distribution',
    'Docker Sandboxes': 'Proprietary product terms; release repository is not an OSS license',
    'FFmpeg': 'Build-dependent LGPL/GPL and optional codec constraints',
    'LibreOffice core': 'Mixed source licensing; GitHub classifier is not a complete distribution license',
}

CATEGORY_NOTES = {
    'Agent workspaces': 'Choose one primary interface and one execution model. An integrated agent computer is powerful but shares browser, file and shell state. Archived entries are retained only for reference.',
    'Orchestration': 'These are application frameworks, not standalone isolation boundaries. Package only the selected framework and write explicit tool authorization.',
    'Tool gateways': 'Gateways, MCP servers and server-building libraries have different responsibilities. Dynamic discovery must not grant permission. Keep infrastructure control outside the model.',
    'Browsing and research': 'Separate search discovery, page extraction, persistent research capture and interactive account actions. Browser sessions and downloads are untrusted or credential-bearing.',
    'Knowledge and RAG': 'Evaluate an integrated product against a simpler custom pipeline. Test source ACL propagation, deletion, citations and temporal facts before ingesting private material.',
    'Document ingestion': 'Documents are untrusted parser input. Bound file sizes, decompression, time and memory. Preserve page/section provenance and original files.',
    'Databases and search': 'Start with one primary retrieval store. A graph database, vector index and full-text index serve different query needs. Extensions require compatible database images.',
    'Model services': 'Model runtime, model weights and GPU drivers have independent compatibility and licensing. No model ranking or tokens-per-second benchmark was performed.',
    'Programs and desktops': 'Editors, notebooks and desktops are code execution. Mount a project workspace, not an entire home directory. Export reviewed outputs from disposable jobs.',
    'Knowledge sources': 'These own source documents or synchronization. Retrieval should preserve their permissions and provenance. A plugin is not itself a server container.',
    'Storage and exchange': 'Object stores, caches and message brokers have different persistence semantics. Validate S3 compatibility and backups with actual clients.',
    'Automation': 'Workflow authors can often execute code or use stored credentials. Prefer durable, idempotent jobs with retry budgets and explicit ownership.',
    'Evaluation and telemetry': 'Trace payloads can contain private source text. Use metadata first and test citation, retrieval and permission behavior separately.',
    'Identity and perimeter': 'VPN, login, authorization and outbound policy are distinct controls. A proxy only enforces egress when alternate routes are blocked.',
    'Isolation and supply chain': 'Several entries are host runtimes or build tools, not Compose applications. Kernel/device/nested-virtualization support must be demonstrated on the target.',
    'Management and backup': 'Container managers have administrator power. Application-consistent backups and off-host restore evidence complement VM snapshots.',
}

def clean(rows):
    for row in rows:
        # Publish short source pointers, not complete upstream documents or license prose.
        row.pop('license_excerpt', None)
        row['readme_evidence'] = [{'line': x['line'], 'text': x['text'][:120]} for x in row.get('readme_evidence', [])[:3]]
        row['license_note'] = LICENSE_NOTES.get(row['name'], '')
        row['license_review_required'] = bool(row['license_note']) or row.get('license_spdx') in ('NOASSERTION', 'Unknown', None)
        if row.get('archived'): row['priority'] = 'Avoid-new'
        row['verification_level'] = 'Official docs checked; runtime unverified' if row.get('documentation_verified') else 'Upstream metadata/README checked; runtime unverified'
    return rows

def md(value):
    return str(value or 'Not established').replace('|', '\\|').replace('\n', ' ')

def slug(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')

def build_markdown(rows):
    categories = list(dict.fromkeys(x['category'] for x in rows))
    lines = ['# AI container and tool catalog', '', 'Research snapshot: **November 11, 2026**. **181 projects / 16 categories.**', '',
             'This is a broad bounded inventory, including libraries, extensions and host runtimes that can support containerized AI work. It is not 181 ready-made containers or a tested stack. Read [the analysis](ANALYSIS.md) and [the source evidence](catalog-evidence.json).', '',
             '## Reading the catalog', '',
             '- **Start:** suitable for an early limited pilot, subject to validation.',
             '- **Evaluate:** strong fit worth comparing against a baseline.',
             '- **Alternative:** an overlapping choice; do not install all alternatives.',
             '- **Experimental:** higher uncertainty; keep out of the initial persistent platform.',
             '- **Later:** defer until scale or complexity warrants it.',
             '- **Reference:** source or building block, not a recommended standalone deployment.',
             '- **Avoid-new:** archived upstream; retain as research/migration context.', '',
             '**Deployment families are editorial classifications:** Container/Stack indicate a service-style deployment to investigate, not proof of a production image. Build/Library/Extension require packaging/integration. Platform/Runtime/Host need infrastructure work. Plugin needs a separate host application/backend.', '',
             '**Release references** come from the repository latest-release endpoint (or stated official documentation). They can name subpackages and are not tested service/image pins. A missing reference is not proof of inactivity. GitHub license classification is not a complete legal assessment. Follow the license source for custom/mixed cases.', '',
             '| Category | Entries |', '|---|---:|']
    counts = Counter(x['category'] for x in rows)
    for category in categories: lines.append(f'| [{category}](#{slug(category)}) | {counts[category]} |')
    for category in categories:
        lines += ['', '## ' + category, '', CATEGORY_NOTES[category], '', '| Project / official source | Purpose | Family / recommendation | Repository release reference | License classification | Boundary / adoption concern |', '|---|---|---|---|---|---|']
        for row in (x for x in rows if x['category'] == category):
            url = row.get('official_url', 'https://github.com/' + row['repository'])
            release = md(row.get('latest_release') or 'No latest-release reference; inspect tags/docs')
            if row.get('release_url'): release = f'[{release}]({row["release_url"]})'
            license_text = row.get('license_spdx', 'Unknown')
            if row.get('license_note'): license_text += '; ' + row['license_note']
            elif row['license_review_required']: license_text += '; inspect exact license'
            license_url = row.get('license_source')
            if license_url: license_text = f'[{md(license_text)}]({license_url})'
            else: license_text = md(license_text)
            lines.append(f'| [{md(row["name"])}]({url}) | {md(row["function"])} | {md(row["form"])} / **{md(row["priority"])}** | {release} | {license_text} | {md(row["boundary"])} |')
        lines += ['', 'Source detail, README blob identifiers, observation times and root deployment/license paths are in the structured evidence. No runtime validation is implied.']
    lines += ['', '## Additional infrastructure outside the container catalog', '',
              '- [Proxmox VE documentation](https://pve.proxmox.com/pve-docs/): hypervisor, VM lifecycle, networking and storage.',
              '- [Proxmox Backup Server documentation](https://pbs.proxmox.com/docs/): evaluate dedicated backup infrastructure and off-host recovery.',
              '- [Docker Engine security](https://docs.docker.com/engine/security/): runtime and administrator boundaries.',
              '- [MCP security guidance](https://modelcontextprotocol.io/specification/latest/basic/security_best_practices): protocol and identity risks.', '',
              'No claim is made that all tools interoperate. Choose one component per responsibility, validate CPU/GPU support and permissions, and record actual deployment evidence.']
    return '\n'.join(lines) + '\n'

HTML = r'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; base-uri 'none'; form-action 'none'">
<title>AI Backend — Research Catalog</title>
<style>
:root{color-scheme:dark;--bg:#0b1220;--panel:#121e30;--muted:#a9b9cc;--line:#2a3b52;--accent:#74e3c2}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:#edf4ff;font:16px/1.55 system-ui,sans-serif}header,main{max-width:1440px;margin:auto;padding:30px}header{padding-bottom:12px}h1{font-size:clamp(2rem,4vw,3.2rem);line-height:1.1;margin:12px 0}h2{margin:8px 0;font-size:1.18rem}.eyebrow{color:var(--accent);letter-spacing:.12em;font-size:.8rem;text-transform:uppercase}p{max-width:1000px}.muted,small{color:var(--muted)}a{color:#9ad8ff}.controls{display:grid;grid-template-columns:2fr repeat(3,1fr);gap:12px;padding:18px;background:var(--panel);border:1px solid var(--line);border-radius:12px}label{font-size:.85rem;color:var(--muted)}input,select{display:block;width:100%;padding:12px;margin-top:5px;border:1px solid #496079;border-radius:7px;background:#0c1626;color:white;font:inherit}.summary{display:flex;gap:22px;flex-wrap:wrap;margin:20px 0}.summary span{color:var(--accent)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px}.card{padding:20px;border:1px solid var(--line);border-radius:12px;background:var(--panel)}.badge{display:inline-block;font-size:.74rem;padding:3px 8px;border:1px solid #426078;border-radius:6px;margin:0 4px 5px 0;color:#c8e2ff}.start{color:#8af1cb;border-color:#347665}.avoid{color:#ffb7b7;border-color:#a35d5d}.card p{margin:10px 0}.detail{border-top:1px solid var(--line);padding-top:10px;font-size:.88rem}.warning{border-left:3px solid #ddad6a;padding-left:14px;color:#e8cfaa}details{margin-top:12px}summary{cursor:pointer;color:#9ad8ff}ul{padding-left:20px}footer{padding:30px;color:var(--muted);text-align:center}button{background:none;border:1px solid #496079;color:white;padding:8px 14px;border-radius:6px;cursor:pointer}.empty{padding:40px;border:1px dashed var(--line)}@media(max-width:800px){header,main{padding:18px}.controls{grid-template-columns:1fr 1fr}.controls label:first-child{grid-column:1/-1}}@media(max-width:460px){.grid,.controls{grid-template-columns:1fr}.controls label:first-child{grid-column:auto}}
</style></head><body>
<header><div class="eyebrow">AI Backend / public-source research / November 11, 2026</div><h1>A workspace for agents.<br>A boundary for every capability.</h1>
<p>181 projects across 16 categories: knowledge, browsers, files, programs, models and the infrastructure that contains them. Filter by function, deployment family and recommendation.</p>
<p class="warning">Research, not a deployed stack. Release references are repository observations, not tested image pins. Libraries, host runtimes and plugins are labeled separately from services.</p></header>
<main><div class="controls"><label>Search capabilities, products or licenses<input id="search" type="search" placeholder="browser, graph, OCR, offline, MIT…"></label><label>Category<select id="category"><option value="">All categories</option></select></label><label>Recommendation<select id="priority"><option value="">All recommendations</option></select></label><label>Deployment family<select id="form"><option value="">All families</option></select></label></div>
<div class="summary"><div><span id="count" aria-live="polite">181</span> projects shown</div><div>Official upstream sources</div><div>No external scripts or analytics</div><button id="reset" type="button">Reset filters</button></div>
<div id="cards" class="grid"></div><noscript>JavaScript is needed for filtering. Read CATALOG.md for the complete static catalog.</noscript>
</main><footer>Start = pilot candidate · Evaluate = compare first · Alternative = overlapping choice · Experimental/Later = defer · Avoid-new = archived upstream<br>See ANALYSIS.md for recommendations and PROXMOX-ARCHITECTURE.md for proposed placement.</footer>
<script id="catalog-data" type="application/json">__DATA__</script>
<script>
const rows=JSON.parse(document.getElementById('catalog-data').textContent);
const el=id=>document.getElementById(id);
const escapeText=v=>String(v??'Not established').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const link=(url,label)=>/^https:\/\//.test(url||'')?`<a href="${escapeText(url)}" target="_blank" rel="noopener noreferrer">${escapeText(label)}</a>`:escapeText(label);
for(const key of ['category','priority','form']){for(const value of [...new Set(rows.map(r=>r[key]))].sort()){const option=document.createElement('option');option.value=value;option.textContent=value;el(key).append(option)}}
function render(){const q=el('search').value.toLowerCase().trim();const terms=q.split(/\s+/).filter(Boolean);const selected=rows.filter(r=>['category','priority','form'].every(k=>!el(k).value||r[k]===el(k).value)&&terms.every(t=>[r.name,r.category,r.function,r.boundary,r.license_spdx,r.license_note].join(' ').toLowerCase().includes(t)));el('count').textContent=selected.length;el('cards').innerHTML=selected.length?selected.map(r=>`<article class="card"><div class="muted">${escapeText(r.category)}</div><h2>${link(r.official_url,r.name)}</h2><span class="badge ${r.priority==='Start'?'start':r.priority==='Avoid-new'?'avoid':''}">${escapeText(r.priority)}</span><span class="badge">${escapeText(r.form)}</span><p>${escapeText(r.function)}</p><div class="detail"><strong>Boundary:</strong> ${escapeText(r.boundary)}</div><p class="detail"><strong>Release reference:</strong> ${link(r.release_url,r.latest_release||'Inspect tags / official docs')}<br><strong>License classification:</strong> ${escapeText(r.license_spdx||'Unknown')}${r.license_review_required?' · review required':''}<br>${escapeText(r.license_note||'Check exact component and distribution terms.')}</p><details><summary>Evidence and deployment pointers</summary><p>${escapeText(r.verification_level)}</p><p>${r.archived?'Archived upstream. ':''}${escapeText(r.metadata_note||'')}${r.pushed_at?' Last upstream push: '+escapeText(r.pushed_at):''}</p><ul>${r.readme_url?'<li>'+link(r.readme_url,'Official README')+'</li>':''}${r.license_source?'<li>'+link(r.license_source,'Official license source')+'</li>':''}${(r.deployment_and_license_paths||[]).map(p=>'<li>'+link(p.url,p.path)+'</li>').join('')}</ul></details></article>`).join(''):'<p class="empty">No matches. Try a broader term or reset the filters.</p>'}
for(const key of ['search','category','priority','form'])el(key).addEventListener(key==='search'?'input':'change',render);
el('reset').addEventListener('click',()=>{for(const key of ['search','category','priority','form'])el(key).value='';render()});render();
</script></body></html>'''

def main():
    rows = clean(json.loads(SOURCE.read_text(encoding='utf-8')))
    SOURCE.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    (RESEARCH / 'CATALOG.md').write_text(build_markdown(rows), encoding='utf-8')
    # Embedded data cannot terminate the script element, even if upstream content contains HTML.
    serialized = json.dumps(rows, ensure_ascii=False).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    (RESEARCH / 'catalog.html').write_text(HTML.replace('__DATA__', serialized), encoding='utf-8')
    print(json.dumps({'entries':len(rows),'categories':len(set(x['category'] for x in rows)),'archived':[x['name'] for x in rows if x.get('archived')],'license_review_flags':sum(x['license_review_required'] for x in rows)}, indent=2))

if __name__ == '__main__': main()
