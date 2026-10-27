# Assignment coverage and source mapping

The dashboard reads `dist/summary.json`; calculations are not manually retyped into the UI. `tools/build_summary.py` executes the unchanged notebook code in memory, suppresses display output, runs the notebook assertions, and exports an explicit aggregate allowlist. Notebook cell numbers below are zero-based.

| Requirement | Notebook source | Summary key | Dashboard |
|---|---|---|---|
| Q1 satisfaction and diagnostic | 7, 9 | tables.satisfaction_by_title, extra.diagnostics | Figure 1, all-title display control |
| Q1 salary by title | 11 | tables.salary_by_title | Figure 2, all-title display control |
| Q1 salary vs age | 13 | charts.age, extra.diagnostics | Exact Figure 3 PNG plus optional aggregated heatmap |
| Missingness / categories / anomalies | 5, 7, 9 | meta, tables.sat_sensitivity | Q1 preparation disclosure |
| Q2(a) descriptions, extremes, exclusions | 16 | q2_descriptives, q2_outliers, q2_sensitivity | #q2a |
| Q2(b) manual pooled t and SciPy match | 18 | extra.manual_steps, scalars, tests.student | #q2b and manual disclosure |
| Assumptions / Welch / Levene | 18 | tests.welch, tests.q2_levene | #q2b |
| Q2(c) 10,000 n-out-of-n replicates | 20–23 | meta, charts.q2means/q2difference/q2standardized | Figures 4–6 |
| Q2(d) required bootstrap-means t | 25 | tests.bootstrap_means_t | #q2d; explicit pseudoreplication caveat |
| Q2(d) supplementary null bootstrap | 25 | tests.q2_boot_test | #q2d disclosure |
| Q2(e) intervals and widths | 27 | tables.q2_cis | #q2e, interval plot and table |
| Q2(f) medians, Mood, ties | 29 | tests.mood, extra.median_ties, contingency | #q2f |
| Q2(f) null median bootstrap | 29 | tests.q2_median_boot_test | #q2f disclosure and Monte Carlo floor |
| Q3(a) US/Canada, degrees, outliers | 33 | extra, q3_descriptives/q3_outliers/q3_sensitivity | #q3a |
| Q3(b) ordinary/Welch/IQR ANOVA | 35 | tests.anova/trimmed_anova/q3_levene, scalars | #q3b plus sensitivity disclosure |
| Q3(c) original group sizes and bootstrap | 37–40 | charts.q3means/q3differences/q3standardized | Figures 7–9, all pairs plus selector |
| Q3(d) required bootstrap-means ANOVA | 42 | tests.bootstrap_means_anova | #q3d; pseudoreplication caveat |
| Q3(d) supplementary null F bootstrap | 42 | tests.q3_boot_test | #q3d disclosure |
| Conclusions and limitations | 45, 46 | verified results, methodological narrative | executive summary and #methods |

## Display transformations

- All 31 job-title aggregates are available; initial view shows the highest ten means. This changes display only.
- All nine exact notebook figures are retained as PNG snapshots. Figure 3 is shown directly; other snapshots expand alongside interactive equivalents. No row-level coordinates are served. The optional age heatmap suppresses cells below five (112 observations); 20,190 are displayed, accounting for all 20,302 nonmissing ages.
- Bootstrap curves use 48 common bins within each figure. Every series sums to 10,000 replicates. Only bins/densities and aggregate means/SDs are exported, not the bootstrap draws.
- Annual USD and variances display two decimals, counts display integer separators, and small p-values use scientific notation. Existing notebook-formatted sensitivity p-values keep their original printed precision. Floating-point underflow is explicitly labelled as nonzero probability below numerical resolution.
- All difference directions match the notebook. Pair-selection and legend controls never recalculate or filter respondents.

## Public bundle policy

The 14-file public allowlist contains `index.html`, `styles.css`, `app.js`, `summary.json`, nine PNG figures and bundled `vendor/plotly.min.js`. No CSV, notebook, respondent row, credential, local path or raw-data download is included. The source repository contains the aggregate extraction script and documentation, but not its input files.

## Updated population and report reconciliation

- [x] Original 20,407; DevType Retired 2; Age >80 93; overlap 0; selected 20,312. Six respondents aged 80 retained.
- [x] Employment categories are audited; the sample is not described as exclusively employed.
- [x] Remote/Hybrid n=6,888/7,776; US/Canada 5,413; degree groups 2,954/1,067/295.
- [x] Latest PDF checked against 34 displayed numerical values, with no mismatches.
- [x] Corrected the older dashboard’s stale sample and ranking-reversal statement. The latest notebook and report instead show the IQR Professional–Master’s mean gap narrowing to $48.17, without reversal.
- [x] Executive KPIs, practical significance, client recommendations and noncausal limitations.
- [x] Full ordinary/Welch/IQR ANOVA results and bootstrap center/SE/skewness tables available in disclosures.
