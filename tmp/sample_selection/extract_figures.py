from pathlib import Path
import json,base64
p=Path('notebooks/peinado_1012953314_assignment1.ipynb')
n=json.loads(p.read_text(encoding='utf-8'));i=0
for c in n['cells']:
 for o in c.get('outputs',[]):
  if 'image/png' in o.get('data',{}):
   i+=1; data=o['data']['image/png'];data=''.join(data) if isinstance(data,list) else data
   Path(f'tmp/sample_selection/notebook_figure_{i}.png').write_bytes(base64.b64decode(data))
print('Extracted',i,'figures')
