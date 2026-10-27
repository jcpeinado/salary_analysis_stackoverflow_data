from pathlib import Path
p=Path('dashboard/tools/build_summary.py');s=p.read_text(encoding='utf8')
s=s.replace("table_names=['", "table_names=['selection_flow','employment_audit','q2_boot_summary', '")
s=s.replace('xe=np.arange(0,161,5)','xe=np.arange(0,86,5)')
s=s.replace("'verified_date':'2026-10-12'", "'verified_date':'2026-10-15','report_sha256':hashlib.sha256((ROOT/'reports/Julian_Peinado_1012953314_assignment1.pdf').read_bytes()).hexdigest(),'original_n':ns['original_n'],'retired_n':ns['retired_n'],'over_80_n':ns['over_80_n'],'overlap_n':ns['overlap_n'],'age80_n':int(ns['survey'].Age.eq(80).sum()),'employment_indicator_n':ns['employment_indicator_n']")
s=s.replace("len(tables['salary_by_title'])==32", "len(tables['salary_by_title'])==31")
s=s.replace('32 titles','31 titles')
# Extract exact embedded notebook figures; never export scatter coordinates or respondents.
s += '''
import base64
figdir=OUT/'figures';figdir.mkdir(exist_ok=True)
figure_count=0
for cell in nb['cells']:
 for output in cell.get('outputs',[]):
  png=output.get('data',{}).get('image/png')
  if png:
   figure_count+=1
   (figdir/f'figure-{figure_count}.png').write_bytes(base64.b64decode(''.join(png) if isinstance(png,list) else png))
assert figure_count==9
# Compare canonical full-precision calculations with the notebook's saved result narrative.
outputs='\\n'.join(str(o.get('data',{}).get('text/markdown','')) for c in nb['cells'] for o in c.get('outputs',[]))
for value in [f"{ns['mean_difference']:,.2f}",f"{ns['n_remote']:,}",f"{ns['n_hybrid']:,}",f"{ns['anova'].statistic:.4f}"]:
 assert value in outputs, ('Saved notebook output mismatch',value)
print('PASS: saved notebook narrative matches execution; nine exact embedded figures exported.')
'''
p.write_text(s,encoding='utf8')
