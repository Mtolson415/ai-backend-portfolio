"""Scan only this demo's exported images; no Docker socket is mounted."""
import json
from pathlib import Path
import subprocess
import tempfile
import sys
from datetime import datetime, timezone

ROOT=Path(__file__).resolve().parents[1]
SCANNER='aquasec/trivy:0.76.2@sha256:8f6bb947dbc528902e11f2f5be52f7b519f6a39d5d148f41166f2040499768fb'
local=ROOT/'local'
local.mkdir(exist_ok=True)
reports=[]
with tempfile.TemporaryDirectory(prefix='image-scan-',dir=local) as tmp:
    for index,image in enumerate(sys.argv[1:] or ('ai-backend-reference:local','ai-backend-gateway:local')):
        archive=Path(tmp)/f'image-{index}.tar'
        subprocess.run(['docker','save','-o',str(archive),image],check=True,capture_output=True)
        command=['docker','run','--rm','--mount',f'type=bind,source={Path(tmp).resolve()},target=/scan,readonly',
                 '--mount','type=volume,source=ai-backend-portfolio-trivy-cache,target=/root/.cache/trivy',
                 SCANNER,'image','--input',f'/scan/{archive.name}','--scanners','vuln','--severity','HIGH,CRITICAL','--format','json']
        result=subprocess.run(command,capture_output=True,text=True,encoding='utf-8',errors='replace')
        if result.returncode:
            raise SystemExit('Image scan could not complete: '+result.stderr[-1800:])
        payload=json.loads(result.stdout)
        findings=[]
        for item in payload.get('Results',[]):
            for v in item.get('Vulnerabilities',[]):
                findings.append({k:v.get(k) for k in ('VulnerabilityID','PkgName','InstalledVersion','FixedVersion','Severity')})
        reports.append({'image':image,'artifact_id':payload.get('Metadata',{}).get('ImageID'),
                        'high_critical_findings':findings,'finding_count':len(findings)})
report={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'scanner':SCANNER,'reports':reports,
        'limits':'Known HIGH/CRITICAL vulnerability scan of two local images at this observation time. Does not certify safety or cover source secrets, all severities, browser/model components or future updates.'}
target=ROOT/'docs/evidence/image-scan.json'
target.parent.mkdir(parents=True,exist_ok=True)
target.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'images':len(reports),'high_critical_findings':sum(x['finding_count'] for x in reports)},indent=2))
raise SystemExit(1 if any(x['finding_count'] for x in reports) else 0)
