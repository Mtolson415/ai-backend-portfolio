"""Create local synthetic-demo credentials without printing them."""
import os
from pathlib import Path
import secrets

path=Path(__file__).resolve().parents[1]/'.env'
with path.open('x',encoding='utf-8') as stream:
    stream.write('AI_ALPHA_TOKEN='+secrets.token_hex(32)+'\nAI_BETA_TOKEN='+secrets.token_hex(32)+'\n')
try: os.chmod(path,0o600)
except OSError: pass
print('Created ignored .env with two random demo credentials. Do not commit it.')
