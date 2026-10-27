from pathlib import Path
import json,math,re
ROOT=Path(__file__).resolve().parents[1]
d=json.loads((ROOT/'dist/summary.json').read_text(encoding='utf8'))
m,s,t,T=d['meta'],d['scalars'],d['tests'],d['tables']
def close(a,b):assert math.isclose(a,b,rel_tol=1e-11,abs_tol=1e-10),(a,b)
assert m['replications']==10000 and m['seed']==16242026
assert s['n_remote']+s['n_hybrid']==sum(r['n'] for r in T['q2_descriptives'])
assert sum(r['n'] for r in T['q3_descriptives'])==s['total_n']
close(s['mean_remote']-s['mean_hybrid'],s['mean_difference'])
close(s['manual_t'],t['student']['statistic']);close(s['manual_p'],t['student']['pvalue'])
close(s['pooled_sd']**2,s['pooled_variance'])
close(s['mean_difference']/s['pooled_se'],s['manual_t'])
for r in T['q2_cis']:close(r['Upper USD']-r['Lower USD'],r['Width USD'])
for name in ['q2_boot_test','q2_median_boot_test','q3_boot_test']:close(t[name]['p'],(t[name]['exceedances']+1)/(m['replications']+1))
for name,c in d['charts'].items():
 if name=='age':continue
 for series in c['series']:
  assert sum(series['counts'])==m['replications']
  close(sum(v*(b-a) for v,a,b in zip(series['density'],c['edges'],c['edges'][1:])),1)
  if 'standardized' in name:close(series['mean'],0);close(series['sd'],1)
a=d['charts']['age'];assert all(v==0 or v>=5 for row in a['counts'] for v in row)
assert sum(map(sum,a['counts']))+a['suppressed_observations']==m['rows']-m['missing_age']
assert len(T['satisfaction_by_title'])==len(T['salary_by_title'])==31
assert {p.name for p in (ROOT/'dist').iterdir()}=={'index.html','app.js','styles.css','summary.json','vendor','figures'}
h=(ROOT/'dist/index.html').read_text(encoding='utf8')
embedded=re.search(r'<script id="dashboard-data" type="application/json">(.*?)</script>',h,re.S)
assert embedded and json.loads(embedded.group(1))==d, 'Embedded summary must match the verified source'
for n in range(1,10):assert f'Figure {n} ' in h
for q in ['q2a','q2b','q2c','q2d','q2e','q2f','q3a','q3b','q3c','q3d']:assert f'id="{q}"' in h
assert not re.search(r'<script[^>]+src=["\']https?://',h)
assert not any(p.suffix in ['.csv','.ipynb','.env'] for p in (ROOT/'dist').rglob('*'))
print('PASS: source identities, counts, p-values, interval widths, histogram normalization, standardization, age suppression, nine figures, all subsections, 14-file public allowlist.')

assert (m['original_n'],m['retired_n'],m['over_80_n'],m['overlap_n'],m['rows'])==(20407,2,93,0,20312)
assert (s['n_remote'],s['n_hybrid'],s['total_n'])==(6888,7776,4316)
assert all((ROOT/f'dist/figures/figure-{i}.png').is_file() for i in range(1,10))
assert (ROOT/'dist/vendor/plotly.min.js').stat().st_size>1000000
assert len(list((ROOT/'dist').rglob('*.*')))==14
print('PASS: current selection, group counts, original figures, bundled Plotly, aggregate-only file allowlist.')
