from pathlib import Path
import json,re,shutil
root=Path('tmp/dashboard_site'); local=Path('dashboard')
shutil.copy2(local/'dist/summary.json',root/'dist/summary.json')
shutil.copytree(local/'dist/figures',root/'dist/figures',dirs_exist_ok=True)
h=(root/'dist/index.html').read_text(encoding='utf8')
h=re.sub(r'<script id="dashboard-data" type="application/json">.*?</script>','<script id="dashboard-data" type="application/json">'+(root/'dist/summary.json').read_text(encoding='utf8')+'</script>',h,flags=re.S)
(root/'dist/index.html').write_text(h,encoding='utf8')
s=(local/'tools/validate.py').read_text(encoding='utf8').replace('==32','==31').replace("{'index.html','app.js','styles.css','summary.json'}", "{'index.html','app.js','styles.css','summary.json','vendor','figures'}")
s += '''
assert (m['original_n'],m['retired_n'],m['over_80_n'],m['overlap_n'],m['rows'])==(20407,2,93,0,20312)
assert (s['n_remote'],s['n_hybrid'],s['total_n'])==(6888,7776,4316)
assert all((ROOT/f'dist/figures/figure-{i}.png').is_file() for i in range(1,10))
assert (ROOT/'dist/vendor/plotly.min.js').stat().st_size>1000000
assert len(list((ROOT/'dist').rglob('*.*')))==14
print('PASS: current selection, group counts, original figures, bundled Plotly, aggregate-only file allowlist.')
'''
(local/'tools/validate.py').write_text(s,encoding='utf8')
shutil.copy2(local/'tools/validate.py',root/'tools/validate.py')
shutil.copy2(local/'tools/build_summary.py',root/'tools/build_summary.py')
s=(local/'tools/embed_summary.py').read_text(encoding='utf8').replace('20261012-2','20261015')
(local/'tools/embed_summary.py').write_text(s,encoding='utf8');(root/'tools/embed_summary.py').write_text(s,encoding='utf8')
# Round only when verifying the written presentation; aggregates retain numerical precision.
d=json.loads((root/'dist/summary.json').read_text(encoding='utf8'))
report=Path('tmp/dashboard_review/Julian_Peinado_1012953314_assignment1.txt').read_text(encoding='utf8')
checks=['20,407','20,312','6,888','7,776','4,316','5,413','2,954','1,067','295']
for name in ['q2_descriptives','q3_descriptives']:
 for row in d['tables'][name]:
  for col in ['Mean','Median','SD']:checks.append(f'{row[col]:,.2f}')
for row in d['tables']['q2_cis']:
 for col in ['Lower USD','Upper USD','Width USD']:checks.append(f'{row[col]:,.2f}')
checks += [f"{d['scalars']['mean_difference']:,.2f}",f"{d['tests']['anova']['statistic']:.4f}",f"{d['tests']['mood']['statistic']:.4f}",f"{d['tests']['bootstrap_means_anova']['statistic']:,.4f}"]
missing=[x for x in checks if x not in report]
assert not missing,missing
Path('tmp/dashboard_review/REPORT_COMPARISON.json').write_text(json.dumps({'checked_values':checks,'mismatches':missing},indent=2),encoding='utf8')
print('PASS:',len(checks),'report numbers match notebook-generated values.')
