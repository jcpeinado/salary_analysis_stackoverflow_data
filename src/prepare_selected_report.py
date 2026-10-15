"""Rebuild the selected-population Word report from the executed notebook.
Run src/reproduce_selected_report.py first to refresh results and notebook outputs.
"""
from pathlib import Path
import pickle
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy import stats
import json
ROOT=Path(__file__).resolve().parents[1]
with (ROOT/'tmp/sample_selection/results.pkl').open('rb') as f: globals().update(pickle.load(f))
plt.rcParams.update({'font.size':8,'axes.spines.top':False,'axes.spines.right':False})
OUT=ROOT/'tmp/sample_selection'; OUT.mkdir(exist_ok=True,parents=True)
replacements={}
def setp(i,text): replacements[i]=text
def usd(x): return f'${x:,.2f}'
def pv(x): return f'{x:.4g}' if x else 'below floating-point resolution'
def seq(xs,fmt=lambda x:f'{x:,}'): return '/'.join(fmt(x) for x in xs)
student=stats.ttest_ind(remote,hybrid,equal_var=True)
welch=stats.ttest_ind(remote,hybrid,equal_var=False)
anova=stats.f_oneway(*education_groups.values())
trimmed_anova=stats.f_oneway(*education_trimmed.values())
q2_levene=stats.levene(remote,hybrid,center='median')
q3_levene=stats.levene(*education_groups.values(),center='median')
bootstrap_means_t=stats.ttest_ind(boot_remote['mean'],boot_hybrid['mean'],equal_var=True)
bootstrap_means_anova=stats.f_oneway(*(education_boot[k]['mean'] for k in education_labels))
mood=stats.median_test(remote,hybrid,ties='below',correction=True)
# Remove the prior dashboard link: it describes a different population.
setp(2,'Updated October 14, 2026 | Selected-population analysis')
selection=[
('Study Population and Sample Selection Criteria','Heading 1'),
(f'The study aims to examine workforce participation. I exclude explicit retired classifications and recorded ages greater than 80 as researcher-defined scope decisions based on engineering judgment. Age 80 remains eligible. These criteria do not identify data errors or statistical outliers and are distinct from satisfaction cleaning and salary-IQR sensitivity analysis.','Normal'),
(f'The original sample contains {original_n:,} respondents. Retirement excludes {retired_n}; age >80 identifies {over_80_n} exclusions; their overlap is {overlap_n}. Applying retirement first removes {retired_n}, then age removes {age_excluded_after_retirement}, leaving {len(survey):,} respondents. All reported analyses use this selected sample.','Normal'),
('Employment has four supplied categories: Employed; Independent contractor, freelancer, or self-employed; Student; and Not employed. Neither Employment nor supplementary activities explicitly labels anyone Retired. Two DevType records do, although both say Employed. I prioritize their explicit retired classification without resolving the underlying inconsistency. Supplementary activities are semicolon-delimited; transitioning to retirement does not establish completed retirement and is retained.','Normal'),
(f'The retained employment counts are '+ '; '.join(f'{k}: {v:,}' for k,v in survey.Employment.value_counts().items())+f'. Employment/self-employment or supplementary paid work is reported by {employment_indicator_n:,}; {len(survey)-employment_indicator_n:,} lack that affirmative indicator. These fields support self-reported indicators, not independent verification of current employment. Students and respondents marked not employed remain because no additional employed-only restriction is imposed.','Normal'),
(f'There are {int(survey.Age.eq(80).sum())} retained respondents aged exactly 80. The {survey.Age.isna().sum()} missing ages remain in analyses not requiring age, since missingness does not establish age >80; they are omitted from the age plot. The age ceiling therefore cannot be verified for every retained respondent. Findings concern selected salary-reporting respondents, not a verified population of actively employed workers.','Normal')]
setp(4,f'How does developer pay vary with work arrangement and education? Among the {len(survey):,} selected respondents, remote workers report higher mean and median salaries, while US and Canadian degree groups differ in average pay. The analysis explores how robust these patterns are. Salaries are positive, finite annual USD; the source contains {survey.shape[1]} variables.')
setp(5,f'Within the selected sample, satisfaction analysis excludes {survey[SAT].isna().sum():,} missing ratings and {satisfaction_invalid.sum()} rating outside the working scale of 0–10. The age plot omits {survey.Age.isna().sum()} missing ages. Each row has one supplied job category; recorded ages have an unknown cleaning history.')
setp(7,f'Figures 1–2 show the lowest two and highest three means, with valid counts; the notebook covers all {len(salary_by_title)} retained titles. '+q1_diagnostic_1.replace('\\$','$')+' '+q1_diagnostic_2.replace('\\$','$'))
setp(9,f'Figure 3 uses a logarithmic salary axis. '+q1_diagnostic_3.replace('\\$','$')+' The population age ceiling applies to all tests; the remaining diagnostic flags cause no additional exclusions.')
setp(12,f'I compare exact labels Remote and Hybrid, excluding {len(survey)-len(q2_data):,} other selected respondents. All salaries in these groups remain in the primary analysis. Positive Remote − Hybrid differences indicate higher remote pay.')
a=q2_descriptives
setp(14,f'The middle half of salaries spans {usd(a.loc["Remote","Q1"])}–{usd(a.loc["Remote","Q3"])} for Remote and {usd(a.loc["Hybrid","Q1"])}–{usd(a.loc["Hybrid","Q3"])} for Hybrid. Minimum values are {usd(remote.min())} and {usd(hybrid.min())}.')
setp(15,f'The largest Hybrid and Remote salaries are {usd(hybrid.max())} and {usd(remote.max())}, contributing {100*hybrid.max()/hybrid.sum():.2f}% and {100*remote.max()/remote.sum():.2f}% of their group salary totals. Size alone does not establish an error, so these remain in the selected population.')
r,h=q2_trimmed['Remote'],q2_trimmed['Hybrid']
setp(16,f'A separate sensitivity check uses each group’s Q1 − 1.5×IQR and Q3 + 1.5×IQR fences. Upper limits are {usd(q2_outliers.loc["Remote","Upper fence"])} and {usd(q2_outliers.loc["Hybrid","Upper fence"])}; both lower limits are negative. It removes {len(remote)-len(r)} and {len(hybrid)-len(h)}, leaving {len(r):,} and {len(h):,}. Means become {usd(r.mean())} and {usd(h.mean())}; the gap is {usd(r.mean()-h.mean())} (pooled p={pv(stats.ttest_ind(r,h,equal_var=True).pvalue)}). These truncated distributions answer a different question; the primary analyses retain salary extremes.')
setp(18,f'I test H₀: μR − μH = 0 against H₁: μR − μH ≠ 0 at α=0.05. Using n−1, sample variances are {variance_remote:,.2f} and {variance_hybrid:,.2f} USD². The pooled calculation is:')
setp(21,f'Here n is group size, x̄ the mean, s² sample variance and sₚ pooled SD. Results are sₚ={usd(pooled_sd)} and SE={usd(pooled_se)}. SE describes uncertainty in the gap; SD describes variation between individuals.')
setp(23,f'Manual and built-in results agree and reject H₀ at 0.05. The {usd(mean_difference)} gap is {100*mean_difference/mean_hybrid:.1f}% of the Hybrid mean, but this test cannot explain why it exists.')
setp(24,f'Independence is unverified, and skew may weaken normal approximations. The variance ratio is {variance_ratio_q2:.2f} (median-centered Levene p={pv(q2_levene.pvalue)}). Welch’s test allows unequal variances and also rejects. A p-value is not the probability that H₀ is true.')
setp(26,f'I resample within each group with replacement, retaining {n_remote:,} Remote and {n_hybrid:,} Hybrid salaries per draw. There are 10,000 replications, seed {SEED}, and separate named NumPy streams. Mean SEs are {usd(boot_remote["mean"].std(ddof=1))} and {usd(boot_hybrid["mean"].std(ddof=1))}; the difference SE is {usd(bootstrap_difference.std(ddof=1))}. These describe estimated means, not individual salary dispersion.')
setp(32,f'The required pooled t-test on two arrays of 10,000 unshifted bootstrap means gives t={bootstrap_means_t.statistic:.3f}, df=19,998 and p {pv(bootstrap_means_t.pvalue)}. It rejects, but simulations reuse the same respondents. The nominal SE falls as 1/√B; more replications can reduce p without adding population evidence.')
setp(33,f'For a separate null test, each group is shifted to the combined mean, preserving shape and variance. Resamples retain original sizes and recalculate the pooled SE. Comparing |T₀*|=|(Δ*−Δ̂)/SE*| with |{manual_t:.5f}| yields {q2_boot_test["exceedances"]} extreme draws: p=({q2_boot_test["exceedances"]}+1)/10,001={pv(q2_boot_test["p"])}. This rejects under an approximate null calibration; empirical tails and simulation error affect the result.')
setp(36,f'Both intervals exclude zero. The analytical interval is Δ̂ ± t(0.975, {degrees_freedom:,})SE = {usd(mean_difference)} ± {usd((parametric_ci[1]-parametric_ci[0])/2)}. The bootstrap interval uses the 2.5th and 97.5th percentiles of unshifted Δ*. Its width differs from the pooled interval by {usd((bootstrap_ci[1]-bootstrap_ci[0])-(parametric_ci[1]-parametric_ci[0]))}. Coverage concerns repeated sampling of a fixed parameter, not its probability. Percentile intervals and t-tests need not always agree.')
setp(38,f'Remote and Hybrid medians are {usd(median_remote)} and {usd(median_hybrid)}, a gap of {usd(median_difference)}. Mood’s test counts salaries above versus at/below the pooled median {usd(mood.median)}. Ties ({int((remote==mood.median).sum())} Remote; {int((hybrid==mood.median).sum())} Hybrid) go below. With Yates correction, χ²(1)={mood.statistic:.4f}, p={pv(mood.pvalue)}, rejecting equal medians.')
setp(39,f'I bootstrap the median difference 10,000 times at original group sizes. Shifting each group to the pooled median is equivalent to subtracting the observed gap from each simulated gap. There are {q2_median_boot_test["exceedances"]} extreme absolute null gaps; plus-one p={pv(q2_median_boot_test["p"])}. The 95% Monte Carlo upper bound is {pv(q2_median_boot_test["MC tail upper"])}. A zero exceedance count identifies the simulation floor, not a precise population tail probability.')
setp(43,f'The selected sample includes {int(survey.Country.isin(north_america).sum()):,} US/Canada respondents. Exact Bachelor’s, Master’s and Professional degree categories leave {total_n:,}. B, M and P abbreviate those categories. Professional is used as supplied, without assuming its qualifications. Other countries and degrees are outside Q3 scope; all eligible salaries remain.')
setp(45,f'The degree-group IQR check flags '+seq([int(q3_outliers.loc[k,"Flagged n"]) for k in education_labels])+f' salaries, leaving '+seq([len(education_trimmed[k]) for k in education_labels])+'. Restricted means are '+seq([education_trimmed[k].mean() for k in education_labels],usd)+f'. Their ordering illustrates tail sensitivity; restricted ANOVA p={pv(trimmed_anova.pvalue)}. This is separate from population selection.')
setp(47,f'For H₀: μB=μM=μP, ordinary ANOVA gives F(2, {df_within:,})={anova.statistic:.4f}, p={pv(anova.pvalue)}, rejecting equality. It does not identify which pairs differ. The exact reference assumes independent normal errors and equal variances. The variance ratio is {variance_ratio_q3:.2f} (Levene p={pv(q3_levene.pvalue)}). Welch ANOVA also rejects: F(2, {welch_df2:.2f})={welch_f:.4f}, p={pv(welch_anova_p)}.')
setp(49,'Using 10,000 independent resamples of sizes '+seq(group_sizes)+' (B/M/P), mean SEs are '+seq([education_boot[k]['mean'].std(ddof=1) for k in education_labels],usd)+f'. Separate streams use seed {SEED}. Shared group draws preserve contrast dependence. Observed B−M, B−P and M−P gaps are '+seq([education_means[0]-education_means[1],education_means[0]-education_means[2],education_means[1]-education_means[2]],usd)+'.')
setp(53,f'ANOVA on three sets of 10,000 unshifted bootstrap means gives F(2, 29,997)={bootstrap_means_anova.statistic:,.4f}, p {pv(bootstrap_means_anova.pvalue)}. It rejects, but increasing B adds simulations, not respondents. This provides no independent confirmation or significant pair identification.')
setp(54,f'The separate null bootstrap shifts each degree group to the combined mean and resamples at original sizes, preserving within-group variances. There are {q3_boot_test["exceedances"]} extreme F* values out of 10,000: p=({q3_boot_test["exceedances"]}+1)/10,001={pv(q3_boot_test["p"])}. This approximate test rejects while allowing unequal empirical shapes and variances. Sparse tail counts limit precision. No formal post-hoc tests were performed.')
setp(56,f'Remote respondents have higher mean and median pay, and US/Canada degree groups differ overall. These are associations within the selected salary-reporting sample. Country, role and experience can confound comparisons; survey selection, self-report and uncertain independence limit generalization. The two exclusions do not establish an employed-only population or verify missing ages. Bootstrap resampling cannot repair these limitations. The {int(survey.duplicated().sum())} identical rows remain because respondent identities are unverified. No overall multiplicity correction was applied.')
setp(58,'OpenAI Codex assisted with analysis and report revision. The current request was to exclude retired respondents and ages above 80, rerun all analyses, and document scope and employment limitations. Numerical checks cover selection, manual/library agreement, bootstrap calculations and source integrity. Earlier reports and the published dashboard describe a previous population and are superseded by this report. Colab execution and independent student review remain unverified.')
setp(59,'Sources: supplied CSV and executed assignment notebook. Statistical methods follow the SciPy references and Shalizi, The Bootstrap §5.2.4, linked in the notebook.')
# Refresh all four numeric tables.
rows=[]
for label,x in [('Remote',remote),('Hybrid',hybrid)]: rows.append([label,f'{len(x):,}',f'{x.mean():,.2f}',f'{np.median(x):,.2f}',f'{x.std(ddof=1):,.2f}'])
tables=[rows,[[label,f'{t:.5f}',f'{df:,.2f}' if label.startswith('Welch') else f'{int(df):,}',pv(p)] for label,t,df,p in [('Manual pooled',manual_t,degrees_freedom,manual_p),('SciPy pooled',student.statistic,degrees_freedom,student.pvalue),('Welch supplement',welch.statistic,welch.df,welch.pvalue)]],[[label,f'{lo:,.2f}',f'{hi:,.2f}',f'{hi-lo:,.2f}'] for label,(lo,hi) in [('Pooled t',parametric_ci),('Bootstrap percentile',bootstrap_ci)]],[[label,f'{len(x):,}',f'{x.mean():,.2f}',f'{np.median(x):,.2f}',f'{x.std(ddof=1):,.2f}'] for label,x in zip(['B','M','P'],education_groups.values())]]
# Recreate compact report panels from the same calculation arrays.
import textwrap
fig,axs=plt.subplots(1,2,figsize=(13,4.4),layout='constrained')
for ax,df,col,title in [(axs[0],satisfaction_by_title,'mean','Figure 1 · Satisfaction'),(axs[1],salary_by_title,'mean','Figure 2 · Mean salary')]:
    small=df.iloc[[0,1,-3,-2,-1]]
    labels=['\n'.join(textwrap.wrap(k,25))+f' (n={int(v.n):,})' for k,v in small.iterrows()]
    ax.barh(labels,small[col]/(1000 if ax==axs[1] else 1),color='#176B87')
    ax.set_title(title); ax.set_xlabel('USD thousands' if ax==axs[1] else 'Mean rating (0–10)');ax.tick_params(labelsize=8)
fig.savefig(OUT/'eda.png',dpi=180);plt.close(fig)
fig,ax=plt.subplots(figsize=(13,3.4),layout='constrained')
ax.scatter(age_salary_data.Age,age_salary_data[SALARY],s=4,alpha=.18,color='#176B87');ax.set(yscale='log',xlabel='Recorded age (years; selected population)',ylabel='Annual USD (log scale)',title='Figure 3 · Salary versus age')
fig.savefig(OUT/'age.png',dpi=180);plt.close(fig)
def hist(ax,arrays,title,unit):
    for name,x in arrays.items():ax.hist(x,bins=40,density=True,alpha=.45,label=name)
    ax.set(title=title,xlabel=unit,ylabel='Density');ax.legend(fontsize=7)
fig,axs=plt.subplots(1,3,figsize=(13,3.8),layout='constrained')
hist(axs[0],{'Remote':boot_remote['mean']/1000,'Hybrid':boot_hybrid['mean']/1000},'Figure 4 · Bootstrap means','USD thousands')
hist(axs[1],{'R − H':bootstrap_difference/1000},'Figure 5 · Mean difference','USD thousands');axs[1].axvline(0,color='black',ls='--')
hist(axs[2],{'R − H':standardized_difference},'Figure 6 · Standardized','Standard deviations')
fig.savefig(OUT/'q2.png',dpi=180);plt.close(fig)
fig,axs=plt.subplots(1,3,figsize=(13,3.8),layout='constrained')
hist(axs[0],{short:education_boot[k]['mean']/1000 for short,k in zip(['B','M','P'],education_labels)},'Figure 7 · Degree means','USD thousands')
hist(axs[1],{short:x/1000 for short,x in zip(['B−M','B−P','M−P'],education_differences.values())},'Figure 8 · Pairwise gaps','USD thousands')
hist(axs[2],{short:x for short,x in zip(['B−M','B−P','M−P'],education_standardized.values())},'Figure 9 · Standardized','Standard deviations')
fig.savefig(OUT/'q3.png',dpi=180);plt.close(fig)
(OUT/'report_content.json').write_text(json.dumps({'paragraphs':replacements,'selection':selection,'tables':tables},ensure_ascii=False),encoding='utf-8')
print('Prepared report content and charts from notebook results.')
