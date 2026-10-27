from pathlib import Path
p=Path('tmp/dashboard_site/dist/styles.css');s=p.read_text();s=s.replace('#sat-chart svg,#salary-chart svg{min-width:570px}','');s+='\n.section-head>div{min-width:0}select{max-width:100%}@media(max-width:620px){h1{font-size:clamp(44px,12.8vw,58px)}}\n';p.write_text(s)
