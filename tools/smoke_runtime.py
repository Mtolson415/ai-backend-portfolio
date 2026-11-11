"""Check a running local Compose demo; never print authentication material."""
import json
from pathlib import Path
import subprocess
import uuid
from datetime import datetime, timezone
from urllib import request,error

ROOT=Path(__file__).resolve().parents[1]
env=dict(line.split('=',1) for line in (ROOT/'.env').read_text().splitlines() if '=' in line)

def call(path,args=None,token=None):
    headers={'Content-Type':'application/json'}
    if token: headers['Authorization']='Bearer '+token
    req=request.Request('http://127.0.0.1:8080'+path,data=json.dumps(args).encode() if args is not None else None,headers=headers)
    try:
        with request.urlopen(req,timeout=5) as response: return response.status,json.load(response)
    except error.HTTPError as response: return response.code,json.load(response)

checks={}
checks['health']=call('/health')[0]==200
checks['unauthenticated_denied']=call('/v1/files/read',{'project':'alpha','path':'notes.txt'})[0]==401
status,result=call('/v1/knowledge/search',{'project':'alpha','query':'recovery'},env['AI_ALPHA_TOKEN'])
checks['cited_authorized_retrieval']=status==200 and result['matches'][0]['source'].startswith('synthetic://alpha/')
checks['cross_project_denied']=call('/v1/files/read',{'project':'beta','path':'notes.txt'},env['AI_ALPHA_TOKEN'])[0]==403
checks['traversal_denied']=call('/v1/files/read',{'project':'alpha','path':'../beta/notes.txt'},env['AI_ALPHA_TOKEN'])[0]==403
output='outputs/smoke-'+uuid.uuid4().hex+'.txt'
checks['write_output']=call('/v1/files/write-output',{'project':'alpha','path':output,'text':'Synthetic smoke report'},env['AI_ALPHA_TOKEN'])[0]==200
checks['read_output']=call('/v1/files/read',{'project':'alpha','path':output},env['AI_ALPHA_TOKEN'])[1].get('text')=='Synthetic smoke report'
container_id=subprocess.run(['docker','compose','-p','ai-backend-portfolio-demo','ps','-q','tools'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
info=json.loads(subprocess.run(['docker','inspect',container_id],capture_output=True,text=True,check=True).stdout)[0]
host=info['HostConfig']
checks['nonroot']=info['Config']['User']=='10001:10001'
checks['readonly_root']=host['ReadonlyRootfs']
checks['drop_all_capabilities']='ALL' in host.get('CapDrop',[])
checks['no_new_privileges']=any(x.startswith('no-new-privileges') for x in host.get('SecurityOpt',[]))
checks['memory_limit']=host['Memory']==256*1024*1024
checks['pid_limit']=host['PidsLimit']==64
checks['backend_not_published']=not host.get('PortBindings')
gateway_id=subprocess.run(['docker','compose','-p','ai-backend-portfolio-demo','ps','-q','gateway'],cwd=ROOT,capture_output=True,text=True,check=True).stdout.strip()
gateway=json.loads(subprocess.run(['docker','inspect',gateway_id],capture_output=True,text=True,check=True).stdout)[0]
checks['loopback_gateway_binding']=all(x['HostIp']=='127.0.0.1' for x in gateway['HostConfig']['PortBindings']['8080/tcp'])
checks['gateway_nonroot_readonly']=gateway['Config']['User']=='10001:10001' and gateway['HostConfig']['ReadonlyRootfs']
networks=[json.loads(subprocess.run(['docker','network','inspect',n],capture_output=True,text=True,check=True).stdout)[0] for n in info['NetworkSettings']['Networks']]
checks['internal_network_only']=bool(networks) and all(n['Internal'] for n in networks)
probe="import socket; s=socket.socket(); s.settimeout(2); result=s.connect_ex(('1.1.1.1',443)); s.close(); raise SystemExit(0 if result != 0 else 1)"
checks['sample_direct_outbound_connection_denied']=subprocess.run(['docker','exec',container_id,'python','-c',probe],capture_output=True).returncode==0
checks['no_host_bind_mounts']=all(m['Type']!='bind' for container in (info,gateway) for m in container['Mounts'])
report={'observed_at_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'passed':all(checks.values()),'limits':'Single-host synthetic demonstration. The outbound probe covers one IPv4 destination, not a complete egress bypass audit. No Proxmox deployment, browser execution, vector database or model integration is tested.'}
evidence=ROOT/'docs/evidence/runtime-smoke.json'
evidence.parent.mkdir(parents=True,exist_ok=True)
evidence.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
raise SystemExit(0 if report['passed'] else 1)
