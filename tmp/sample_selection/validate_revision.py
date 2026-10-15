from pathlib import Path
import json,hashlib,pickle
import pandas as pd
import numpy as np
root=Path.cwd()
p=root/'notebooks/peinado_1012953314_assignment1.ipynb'
n=json.loads(p.read_text(encoding='utf-8'))
with open('tmp/sample_selection/results.pkl','rb') as f:r=pickle.load(f)
d=pd.read_csv('data/raw_data/clean_stackoverflow_data.csv')
selected=d.loc[~d.DevType.eq('Retired') & ~d.Age.gt(80)]
assert len(selected)==20312 and len(d)==20407
assert r['survey'].equals(selected)
for key,mode in [('remote','Remote'),('hybrid','Hybrid')]:
 np.testing.assert_array_equal(r[key],selected.loc[selected.RemoteWork.eq(mode),'ConvertedCompYearly'].to_numpy())
code=[c for c in n['cells'] if c['cell_type']=='code']
assert [c['execution_count'] for c in code]==list(range(1,29))
assert not any(o['output_type']=='error' for c in code for o in c['outputs'])
assert sum('image/png' in o.get('data',{}) for c in code for o in c['outputs'])==9
sha=hashlib.sha256(Path('data/raw_data/clean_stackoverflow_data.csv').read_bytes()).hexdigest()
assert sha==r['source_hash_before']==r['source_hash_after']
n['cells'][51]['source'] += ['\n**Verification of the selected-population revision.** All 28 code cells completed in a fresh\n',
'local kernel with zero execution errors. All numerical and selection assertions passed; nine\n',
'embedded figures were regenerated and visually reviewed. An independent reconstruction from\n',
'raw records reproduced the selected DataFrame and both Q2 salary arrays. The synchronized\n',
'six-page PDF report was generated from these results and every page was visually reviewed.\n',
'The DOCX content was regenerated, but native Word rendering did not complete; PDF layout\n',
'was verified using a separate ReportLab export. Prior reports/dashboard outputs are historical.\n']
p.write_text(json.dumps(n,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
print('PASS: independent sample and group arrays, 28 sequential code cells, 0 errors, 9 figures, unchanged CSV hash',sha)
