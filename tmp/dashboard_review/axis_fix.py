from pathlib import Path
p=Path('tmp/dashboard_site/dist/app.js');s=p.read_text(encoding='utf-8');s=s.replace("const promise=Plotly.react", "for(const axis of ['xaxis','yaxis'])if(typeof layout[axis]?.title==='string')layout[axis].title={text:layout[axis].title};\n const promise=Plotly.react");p.write_text(s,encoding='utf-8')
