from pathlib import Path
import json, shutil
root=Path('tmp/dashboard_site');d=json.loads((root/'dist/summary.json').read_text(encoding='utf-8'))
p=root/'COVERAGE.md';s=p.read_text(encoding='utf-8');s=s.replace('Figure 3 aggregated heatmap','Exact Figure 3 PNG plus optional aggregated heatmap').replace('All 32 job-title','All 31 job-title');a=s.index('- Age–salary scatter');b=s.index('- Bootstrap curves',a);s=s[:a]+'- All nine exact notebook figures are retained as PNG snapshots. Figure 3 is shown directly; other snapshots expand alongside interactive equivalents. No row-level coordinates are served. The optional age heatmap suppresses cells below five (112 observations); 20,190 are displayed, accounting for all 20,302 nonmissing ages.\n'+s[b:];s=s.replace('Only `dist/index.html`, `dist/styles.css`, `dist/app.js`, and `dist/summary.json` are hosted.','The 14-file public allowlist contains `index.html`, `styles.css`, `app.js`, `summary.json`, nine PNG figures and bundled `vendor/plotly.min.js`.');s+='\n## Updated population and report reconciliation\n\n- [x] Original 20,407; DevType Retired 2; Age >80 93; overlap 0; selected 20,312. Six respondents aged 80 retained.\n- [x] Employment categories are audited; the sample is not described as exclusively employed.\n- [x] Remote/Hybrid n=6,888/7,776; US/Canada 5,413; degree groups 2,954/1,067/295.\n- [x] Latest PDF checked against 34 displayed numerical values, with no mismatches.\n- [x] Corrected the older dashboard’s stale sample and ranking-reversal statement. The latest notebook and report instead show the IQR Professional–Master’s mean gap narrowing to $48.17, without reversal.\n- [x] Executive KPIs, practical significance, client recommendations and noncausal limitations.\n- [x] Full ordinary/Welch/IQR ANOVA results and bootstrap center/SE/skewness tables available in disclosures.\n';p.write_text(s,encoding='utf-8')
(root/'README.md').write_text('''# Workforce Insights — Question 4

Public dashboard: https://developer-compensation-peinado.bronzemoon5.chatgpt.site

A static HTML/CSS/JavaScript dashboard with bundled Plotly 4.1.1. This avoids a Python server, runtime data uploads and external chart dependencies. It uses fixed verified aggregates from the latest notebook and interpretations from Julian_Peinado_1012953314_assignment1.pdf. Ten interactive views accompany all nine original notebook figures.

## Run locally

1. Install Python 3.12 (only the standard library is needed to serve the existing dashboard).
2. From this dashboard directory, run `python -m http.server 8768 --bind 127.0.0.1 --directory dist`.
3. Open http://127.0.0.1:8768 in a modern browser. JavaScript must be enabled.

## Reproduce the results

The source bundle intentionally excludes the CSV and notebook. Place this directory at `dashboard/` within the original assignment repository, keeping the original `notebooks/`, data and `reports/` paths.

1. Optionally create a virtual environment; install `python -m pip install -r dashboard/requirements.txt` from the assignment root.
2. Run `python dashboard/tools/build_summary.py`. It executes the notebook’s own calculations in memory with its seed, assertions, filters and methods, extracts exact saved PNG outputs, and verifies key stored results. It does not edit the inputs.
3. Run `python dashboard/tools/embed_summary.py`.
4. Run `python dashboard/tools/validate.py` and `node --check dashboard/dist/app.js`.
5. Repeat report consistency checks if either source document changes. The published summary records SHA-256 hashes of all three inputs. Do not claim report consistency after an unreviewed source change.

Runtime: local Plotly JavaScript only; requirements.txt covers optional regeneration. The library retains its MIT license notice in its header. https://plotly.com/javascript/getting-started/

## Publish an update

1. Keep the existing Site identity in `.openai/hosting.json`; use its isolated source checkout.
2. Update and validate `dist/`; never publish the parent assignment folder.
3. Use the Sites source-workflow helper to commit, push and package the exact checked source. Pass credentials through hidden stdin only.
4. Save that pushed commit/archive as a Site version, then deploy that saved version. Preserve public access.
5. Wait for deployment status `succeeded`, then test the public URL below. Static hosts can alternatively serve `dist/` directly over HTTPS; no server build or environment secrets are required.

## Submission and public-access check

1. Open a fresh incognito/private browser window, with no ChatGPT session.
2. Paste https://developer-compensation-peinado.bronzemoon5.chatgpt.site directly. No login should be requested.
3. Confirm 20,312 selected respondents and the $17,243.91 mean gap; check all sections, both title selectors, pair selection and figure disclosures.
4. Resize to a phone width; tables scroll within their cards and charts fit the viewport.
5. Put this same URL on the first page of the written report.

Keep the Site public, enabled and undeleted until final grades are released. No shutdown is scheduled and there is no runtime API token or expiring chart CDN dependency; future uptime depends on the hosting service and account. See COVERAGE.md and VALIDATION.md for checks and limitations.
''',encoding='utf-8')
(root/'requirements.txt').write_text('# Optional notebook-based aggregate regeneration; no Python packages needed at runtime.\nnumpy==1.26.4\npandas==2.2.2\nscipy==1.13.1\nmatplotlib==3.9.2\nipython==8.27.0\n',encoding='utf-8')
(root/'VALIDATION.md').write_text('''# Validation — 2026-10-15

- PASS: unchanged notebook calculations executed in memory; all notebook integrity assertions passed. Saved notebook mean gap, sample counts and ANOVA F independently compared with regenerated outputs.
- PASS: 34 numerical values compared with the latest final PDF, including group means, medians, dispersion and confidence endpoints; no mismatch found.
- PASS: sample selection and employment-category audits; exactly age 80 retained.
- PASS: statistical identities, p-values, CI widths, bootstrap density normalization, standardization, age suppression totals and all Q1–Q3 subsections.
- PASS: all nine PNGs extracted directly from saved notebook outputs; aggregate-only JSON and 14-file public allowlist. No CSV, notebook, raw response records or credentials included.
- PASS: JavaScript syntax and local HTTP 200 startup.
- PASS: in-app browser rendered all ten Plotly charts without console warnings/errors. All-title control produced 31 categories; pair selection produced one trace. Technical disclosures and navigation worked.
- PASS: desktop visual inspection and mobile viewport 390×844; document scroll width equalled client width (375px excluding scrollbar). Expanded heatmap resized within its card. Detailed tables scroll horizontally within their containers.
- Public deployment and anonymous HTTP checks are recorded in DELIVERY.md after publishing. A fresh private-window check is documented for the user; an actual incognito browser session was not automated.

Display controls change only visible series/categories, never population filters, statistical calculations or conclusions. Exact figures are available for comparison with the interactive aggregate transformations. Bootstrap simulations are not treated as independent respondent samples.
''',encoding='utf-8')
for p in [root/'tools/validate.py',Path('dashboard/tools/validate.py')]:p.write_text(p.read_text(encoding='utf-8').replace('four-file public allowlist','14-file public allowlist'))

