"""Reproduce notebook calculations in memory and export aggregate-only dashboard data."""
from pathlib import Path
import contextlib,io,json,hashlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'dashboard/dist'
OUT.mkdir(parents=True,exist_ok=True)
nbpath=ROOT/'notebooks/peinado_1012953314_assignment1.ipynb'
data=ROOT/'data/raw_data/clean_stackoverflow_data.csv'
before={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in [nbpath,data]}
nb=json.loads(nbpath.read_text(encoding='utf8'));ns={}
import os
os.chdir(ROOT)
with contextlib.redirect_stdout(io.StringIO()):
 for i,c in enumerate(nb['cells']):
  if c['cell_type']=='code' and i:
   exec(compile(''.join(c['source']),f'notebook_cell_{i}','exec'),ns)
   if i==3:
    ns['display']=lambda *a,**k:None
    ns['narrative']=lambda *a,**k:None
    ns['show_figure']=lambda fig,name:(ns['primary_figures'].append(name),plt.close(fig))
def plain(x):
 if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
 if isinstance(x,(list,tuple,np.ndarray)):return [plain(v) for v in x]
 if isinstance(x,np.generic):return x.item()
 return x
def frame(df):
 df=df.copy();df.index.name='Group'
 return plain(df.reset_index().to_dict(orient='records'))
table_names=['q2_descriptives','q2_outliers','q2_sensitivity','q2_t_comparison','q2_cis','q2_median_tests','contingency','q3_descriptives','q3_outliers','q3_sensitivity','q3_mean_tests','satisfaction_by_title','salary_by_title','sat_sensitivity']
tables={name:frame(ns[name]) for name in table_names if name in ns}
scalars={k:plain(v) for k,v in ns.items() if isinstance(v,(int,float,np.integer,np.floating)) and k not in ['i','observed','direct_t','direct_f','draw_sp2','shortcut_t','direct_median_gap','check_grand','check_within','shortcut_f']}
tests={}
for name in ['student','welch','mood','anova','q2_levene','q3_levene','bootstrap_means_t','bootstrap_means_anova']:
 if name in ns:
  obj=ns[name];tests[name]={k:plain(getattr(obj,k)) for k in ['statistic','pvalue','df','median'] if hasattr(obj,k)}
for name in ['q2_boot_test','q2_median_boot_test','q3_boot_test']:tests[name]=plain(ns[name])
def hist(groups,scale=1):
 arrays={k:np.asarray(x)/scale for k,x in groups.items()}
 edges=np.histogram_bin_edges(np.concatenate(list(arrays.values())),bins=48)
 series=[]
 for name,x in arrays.items():
  counts,_=np.histogram(x,bins=edges);assert counts.sum()==len(x)
  series.append({'name':name,'counts':counts.tolist(),'density':(counts/(len(x)*np.diff(edges))).tolist(),'mean':float(x.mean()),'sd':float(x.std(ddof=1))})
 return {'edges':edges.tolist(),'series':series,'unit':'USD thousands' if scale==1000 else 'standard deviations'}
diff=ns['bootstrap_difference']
charts={
 'q2means':hist({'Remote':ns['boot_remote']['mean'],'Hybrid':ns['boot_hybrid']['mean']},1000),
 'q2difference':hist({'Remote − Hybrid':diff},1000),
 'q2standardized':hist({'Remote − Hybrid':(diff-diff.mean())/diff.std(ddof=1)}),
 'q3means':hist({k:ns['education_boot'][k]['mean'] for k in ns['education_labels']},1000),
 'q3differences':hist(ns['education_differences'],1000),
 'q3standardized':hist(ns['education_standardized'])}
ages=ns['age_salary_data'];xe=np.arange(0,161,5);ye=np.arange(2,8.01,.25)
counts,_,_=np.histogram2d(ages.Age,np.log10(ages[ns['SALARY']]),bins=[xe,ye])
assert int(counts.sum())==len(ages)
suppressed=int(counts[counts<5].sum());counts[counts<5]=0
charts['age']={'age_edges':xe.tolist(),'log_salary_edges':ye.tolist(),'counts':counts.astype(int).tolist(),'minimum_cell_count':5,'suppressed_observations':suppressed,'plotted_observations':int(counts.sum()),'nonmissing_observations':len(ages)}
meta={'rows':len(ns['survey']),'columns':len(ns['survey'].columns),'countries':ns['survey'].Country.nunique(),'missing_satisfaction':int(ns['survey'].JobSat.isna().sum()),'invalid_satisfaction':int(ns['satisfaction_invalid'].sum()),'missing_age':int(ns['survey'].Age.isna().sum()),'flagged_age':int(ns['age_suspect'].sum()),'duplicates':int(ns['survey'].duplicated().sum()),'salary_min':float(ns['survey'][ns['SALARY']].min()),'salary_max':float(ns['survey'][ns['SALARY']].max()),'salary_mean':float(ns['survey'][ns['SALARY']].mean()),'salary_median':float(ns['survey'][ns['SALARY']].median()),'q3_country_count':int(ns['survey'].Country.isin(ns['north_america']).sum()),'seed':ns['SEED'],'replications':ns['B'],'alpha':ns['ALPHA'],'salary_unit':'Annual USD','input_sha256':before[str(data)],'notebook_sha256':before[str(nbpath)],'verified_date':'2026-10-12'}
extra={'manual_steps':plain(ns['manual_steps'].to_dict()),'median_ties':{'Remote':int((ns['remote']==ns['mood'].median).sum()),'Hybrid':int((ns['hybrid']==ns['mood'].median).sum())},'education_labels':ns['education_labels'],'countries':ns['north_america'],'pair_differences':plain(ns['observed_pair_differences']),'diagnostics':[ns[f'q1_diagnostic_{i}'].replace('\\$','$') for i in [1,2,3]],'median_expected_min':float(ns['expected_counts'].min())}
result=plain({'meta':meta,'scalars':scalars,'tables':tables,'tests':tests,'charts':charts,'extra':extra})
(OUT/'summary.json').write_text(json.dumps(result,ensure_ascii=False,allow_nan=False,indent=2),encoding='utf8')
assert all(hashlib.sha256(Path(p).read_bytes()).hexdigest()==sha for p,sha in before.items())
assert len(charts)==7 and len(tables['salary_by_title'])==32
assert abs(scalars['manual_p']-tests['student']['pvalue'])<1e-12
assert len(charts['q3differences']['series'])==3
print('PASS: notebook calculations and assertions; all histogram totals; 32 titles; original files unchanged; only aggregates exported.')
print('Tables:',list(tables));print('Tests:',list(tests));print('Scalars:',list(scalars))
