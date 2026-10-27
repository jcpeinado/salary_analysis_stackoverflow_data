from pathlib import Path
import re
root=Path('tmp/dashboard_site/dist')
p=root/'app.js';s=p.read_text(encoding='utf8')
a=s.index('function svgWrap');b=s.index('async function init',a)
funcs=r'''
const plotJobs=[];
const config={responsive:true,displaylogo:false,scrollZoom:false,modeBarButtonsToRemove:['select2d','lasso2d'],toImageButtonOptions:{format:'png',scale:2}};
function draw(id,traces,layout={}){
 const base={font:{family:'system-ui, sans-serif',size:12,color:'#304c55'},paper_bgcolor:'#ffffff',plot_bgcolor:'#ffffff',margin:{l:60,r:20,t:25,b:80},height:360,hovermode:'closest',legend:{orientation:'h',y:-.28,x:0},colorway:COLORS,xaxis:{gridcolor:'#e4eae7',zerolinecolor:'#788a8c',automargin:true},yaxis:{gridcolor:'#e4eae7',automargin:true}};
 const promise=Plotly.react(id,traces,{...base,...layout},config);plotJobs.push(promise);return promise;
}
function bars(id,rows,limit,salary){
 rows=[...rows].sort((a,b)=>b.mean-a.mean);if(limit!=='all')rows=rows.slice(0,+limit);rows.reverse();
 const labels=rows.map(r=>{let x=r.Group.replace('Developer, ','Dev: ');return x.length>29?x.slice(0,27)+'…':x;});
 const traces=[{type:'bar',orientation:'h',y:labels,x:rows.map(r=>r.mean),name:salary?'Mean salary':'Mean satisfaction',marker:{color:COLORS[0]},customdata:rows.map(r=>[r.Group,r.n]),hovertemplate:'%{customdata[0]}<br>n=%{customdata[1]:,}<br>Mean: '+(salary?'$':'')+'%{x:,.2f}<extra></extra>'}];
 if(salary)traces.push({type:'scatter',mode:'markers',name:'Median',x:rows.map(r=>r.median),y:labels,marker:{color:COLORS[1],size:8},hovertemplate:'Median: $%{x:,.2f}<extra></extra>'});
 draw(id,traces,{height:Math.max(390,rows.length*33+110),margin:{l:175,r:20,t:15,b:75},xaxis:{title:salary?'Annual compensation (USD)':'Mean rating (0–10)',range:salary?undefined:[0,10],rangemode:'tozero',tickprefix:salary?'$':'',automargin:true},yaxis:{automargin:true,tickfont:{size:11}},showlegend:salary});
}
function hist(id,data,filter='all'){
 const rows=filter==='all'?data.series:data.series.filter(s=>s.name===filter);
 const traces=rows.map(s=>({type:'scatter',mode:'lines',line:{shape:'hv',width:2,color:COLORS[data.series.indexOf(s)]},fill:'tozeroy',opacity:.7,name:s.name,x:data.edges,y:[...s.density,0],customdata:[...s.counts,0],hovertemplate:'%{fullData.name}<br>Bin start: %{x:,.2f}<br>Density: %{y:.5f}<br>Draws in bin: %{customdata:,}<extra></extra>'}));
 draw(id,traces,{xaxis:{title:data.unit==='USD thousands'?'USD thousands':'Centered difference / SD',automargin:true},yaxis:{title:'Probability density',automargin:true},shapes:data.edges[0]<0&&data.edges.at(-1)>0?[{type:'line',x0:0,x1:0,y0:0,y1:1,yref:'paper',line:{color:'#52666a',dash:'dot'}}]:[]});
}
function ageChart(a){
 const x=a.age_edges.slice(0,-1).map((v,i)=>(v+a.age_edges[i+1])/2),y=a.log_salary_edges.slice(0,-1).map((v,i)=>(v+a.log_salary_edges[i+1])/2);
 draw('age-chart',[{type:'heatmap',x,y,z:y.map((_,j)=>x.map((_,i)=>a.counts[i][j]||null)),colorscale:[[0,'#e8f1f2'],[1,'#00728a']],colorbar:{title:{text:'Respondents'},thickness:14},hoverongaps:false,hovertemplate:'Age-bin center: %{x} years<br>log10 salary-bin center: %{y}<br>Respondents: %{z:,}<extra></extra>'}],{height:420,xaxis:{title:'Recorded age (5-year bins)',range:[0,85]},yaxis:{title:'Annual USD (logarithmic scale)',tickvals:[2,3,4,5,6,7],ticktext:['$100','$1k','$10k','$100k','$1m','$10m']},margin:{l:70,r:45,t:20,b:65}});
}
function ciChart(rows){draw('ci-chart',rows.map((r,i)=>({type:'scatter',mode:'markers',name:r.Group,x:[DATA.scalars.mean_difference],y:[r.Group],error_x:{type:'data',symmetric:false,array:[r['Upper USD']-DATA.scalars.mean_difference],arrayminus:[DATA.scalars.mean_difference-r['Lower USD']],thickness:4,width:9},marker:{color:COLORS[i],size:9},customdata:[[r['Lower USD'],r['Upper USD']]],hovertemplate:'%{y}<br>Gap: $%{x:,.2f}<br>95% CI: $%{customdata[0]:,.2f} to $%{customdata[1]:,.2f}<extra></extra>'})),{height:240,showlegend:false,margin:{l:165,r:25,t:25,b:65},xaxis:{title:'Remote − Hybrid mean salary (USD)',rangemode:'tozero',tickprefix:'$'},yaxis:{automargin:true}});}
'''
s=s[:a]+funcs+s[b:]
s=s.replace('Age and satisfaction issues do not exclude salaries from Q2 or Q3.', 'The retirement and age >80 selection rules apply to every analysis; satisfaction validity and other age diagnostics cause no further Q2/Q3 exclusions.')
s=s.replace("The Master's and Professional mean ordering reverses after restriction; that ranking is sensitive to the salary tail.","The Professional-minus-Master’s mean gap narrows to $48.17 after restriction; the apparent separation is sensitive to the salary tail.")
s=s.replace("document.documentElement.dataset.ready='true';", "await Promise.all(plotJobs); document.documentElement.dataset.ready='true';")
s=s.replace("put('sat-diagnostic',", "table('selection-table',T.selection_flow);table('employment-table',T.employment_audit);put('selection-copy',`The original ${integer(m.original_n)} respondents lose ${m.retired_n} explicit retired classifications and ${m.over_80_n} recorded ages above 80, with ${m.overlap_n} overlap, leaving ${integer(m.rows)}. Age 80 remains eligible (${m.age80_n} respondents). These researcher-defined scope decisions precede every analysis and are distinct from data cleaning or salary-outlier removal. Retirement is explicitly recorded in DevType, although both excluded records also say Employed. Transitioning to retirement alone is not excluded. The ${m.missing_age} missing ages remain outside the age plot; eligibility against the ceiling cannot be verified for them. Students and respondents marked Not employed remain: this is not a verified employed-only sample.`);put('sat-diagnostic',",1)
s=s.replace('This is the cleaned assignment dataset, not the entire survey.','This is the selected population from the cleaned assignment dataset, not the entire survey.')
s=s.replace('${esc(m.notebook_sha256)}</code></p>','${esc(m.notebook_sha256)}</code><br>Final report SHA-256: <code>${esc(m.report_sha256)}</code></p>')
p.write_text(s,encoding='utf8')
p=root/'index.html';h=p.read_text(encoding='utf8')
h=h.replace('RESEARCH NOTE / 01','SELECTED POPULATION / 2026')
h=h.replace('<a href="#methods">Methods</a>','<a href="#methods">Client decisions</a>')
h=h.replace('<div class="two-up"><article class="panel"><div class="figure-head">','<details open><summary>Study population and sample selection</summary><p id="selection-copy"></p><div id="selection-table"></div><details><summary>Employment categories retained</summary><div id="employment-table"></div></details></details><div class="two-up"><article class="panel"><div class="figure-head">',1)
h=h.replace('<div id="age-chart"></div>', '<img class="notebook-figure" src="figures/figure-3.png" alt="Exact notebook Figure 3: annual salary versus recorded age, after population selection"><details><summary>Explore an aggregated density view</summary><div id="age-chart"></div></details>')
h=h.replace('Arithmetic means retain every positive salary.','Arithmetic means retain every positive salary within the selected population.')
h=h.replace('Keeping it preserves the question about the full salary distribution.','Keeping it preserves the question about the salary distribution within the selected population.')
# Include the exact nine saved figures so public aggregation cannot obscure the required views.
for i,anchor in [(1,'<p id="sat-diagnostic">'),(2,'<p id="salary-diagnostic">')]:
 h=h.replace(anchor,f'<details><summary>View exact notebook Figure {i}</summary><img loading="lazy" class="notebook-figure" src="figures/figure-{i}.png" alt="Exact notebook Figure {i}"></details>'+anchor)
for i,id in [(4,'q2means'),(5,'q2difference'),(6,'q2standardized'),(7,'q3means'),(8,'q3differences'),(9,'q3standardized')]:
 h=h.replace(f'<div id="{id}"></div>',f'<div id="{id}"></div><details><summary>Exact notebook figure</summary><a href="figures/figure-{i}.png" target="_blank" rel="noopener">Open full-size Figure {i}</a><img loading="lazy" class="notebook-figure" src="figures/figure-{i}.png" alt="Exact notebook Figure {i}"></details>')
h=h.replace('<h3>What this means for a technology company</h3>','<h3>From evidence to a better policy question</h3>')
h=h.replace('Compare like-for-like roles, seniority, experience and location before changing policy. Treat that as a next analytical question—not a result established here.', 'Before changing remote-work pay bands, compare like-for-like roles, seniority, experience and location in internal compensation data. For hiring, assess job-relevant skills rather than treating degree-group averages as a screening rule. These are proposed next steps, not effects demonstrated by this survey.')
h=h.replace('The dashboard contains summary tables, title-level averages, histogram bins and a suppressed age–salary count grid.', 'The dashboard contains summary tables, title-level averages, histogram bins, a suppressed age–salary count grid, and rendered notebook figures. The exact age scatterplot is supplied as an image; its respondent coordinates are not exposed as interactive records.')
h=h.replace('<script src="app.js?v=20261012-2"></script>','<script src="vendor/plotly.min.js"></script><script src="app.js?v=20261015"></script>')
h=h.replace('<script src="app.js"></script>','<script src="vendor/plotly.min.js"></script><script src="app.js?v=20261015"></script>')
p.write_text(h,encoding='utf8')
p=root/'styles.css';s=p.read_text(encoding='utf8');s+='''
.notebook-figure{width:100%;height:auto;display:block;margin:18px auto;max-width:1100px}.js-plotly-plot{width:100%;min-width:0}.chart-grid figure:last-child{max-width:none}.plotly .modebar{z-index:2}.panel{box-shadow:0 2px 12px #122e3505}details details{background:#fff}.chart-grid{gap:24px}.chart-wrap:after{display:none!important}@media(max-width:620px){.panel{padding:18px 10px}.metric strong{font-size:24px}h1{font-size:58px}.js-plotly-plot{max-width:100%}}
''';p.write_text(s,encoding='utf8')
print('Upgraded Plotly charts, selection accounting, client narrative and exact notebook figures.')
