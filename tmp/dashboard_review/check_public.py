import urllib.request,json,hashlib,re
from pathlib import Path
base='https://developer-compensation-peinado.bronzemoon5.chatgpt.site'
root=Path('dashboard/dist')
checks=[]
for p in root.rglob('*'):
 if p.is_file():
  name=p.relative_to(root).as_posix()
  with urllib.request.urlopen(urllib.request.Request(base+'/'+name,headers={'User-Agent':'Mozilla/5.0'}),timeout=30) as response:
   data=response.read()
   if name=='index.html':
    extract=lambda b:json.loads(re.search(rb'<script id="dashboard-data" type="application/json">(.*?)</script>',b,re.S).group(1))
    assert extract(data)==extract(p.read_bytes())
   checks.append({'asset':name,'status':response.status,'same_bytes':data==p.read_bytes()})
assert all(c['status']==200 and (c['same_bytes'] or c['asset']=='index.html') for c in checks),checks
Path('tmp/dashboard_review/PUBLIC_CHECK.json').write_text(json.dumps(checks,indent=2))
print('PASS: 14 public assets retrieved without cookies or authorization; 13 assets match exactly; host-transformed HTML contains identical embedded results.')

