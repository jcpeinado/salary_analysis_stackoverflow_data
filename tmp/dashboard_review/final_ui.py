from pathlib import Path
p=Path('tmp/dashboard_site/dist/app.js'); s=p.read_text(encoding='utf-8')
s=s.replace("/\\bn\\b|count|replications/i.test(k)?integer(v):num(v)","/\\bn\\b|count|replications|Excluded|Remaining/i.test(k)?integer(v):/^(t|F)$/.test(k)?num(v,5):/df$/.test(k)&&Number.isInteger(v)?integer(v):num(v)")
s=s.replace("modeBarButtonsToRemove:['select2d','lasso2d']","modeBarButtons:[['toImage'],['zoom2d','pan2d','zoomIn2d','zoomOut2d','autoScale2d','resetScale2d']]")
s=s.replace("table('selection-table',T.selection_flow)","table('selection-table',T.selection_flow,['Stage','Excluded at stage','Remaining'])")
s=s.replace("put('q2-bootstrap-method',", "table('bootstrap-summary',T.q2_boot_summary);table('anova-table',T.q3_anova_results);put('q2-bootstrap-method',")
s=s.replace("await Promise.all(plotJobs);", "document.querySelectorAll('details').forEach(el=>el.addEventListener('toggle',()=>{if(el.open)el.querySelectorAll('.js-plotly-plot').forEach(p=>Plotly.Plots.resize(p));}));await Promise.all(plotJobs);")
p.write_text(s,encoding='utf-8')
p=Path('tmp/dashboard_site/dist/index.html'); s=p.read_text(encoding='utf-8'); s=s.replace('<p id="q2-bootstrap-method"></p>','<p id="q2-bootstrap-method"></p><details><summary>Bootstrap estimates and standard errors</summary><div id="bootstrap-summary"></div></details>'); s=s.replace('<p id="anova-assumptions"></p>','<p id="anova-assumptions"></p><div id="anova-table"></div>'); s=s.replace('Each label shows its group size.','Hover over a bar to inspect its group size.');p.write_text(s,encoding='utf-8')
for root in [Path('dashboard'),Path('tmp/dashboard_site')]:
 p=root/'tools/validate.py';s=p.read_text();s=s.replace('four-file allowlist','14-file public allowlist');p.write_text(s)
