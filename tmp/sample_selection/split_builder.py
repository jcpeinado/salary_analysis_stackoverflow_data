from pathlib import Path
p=Path('src/build_selected_report.py');s=p.read_text(encoding='utf-8-sig')
s=s.replace('from docx import Document\nfrom docx.shared import Inches, Pt, RGBColor\n','import json\n')
a=s.index("doc=Document(");b=s.index('def usd',a)
s=s[:a]+"replacements={}\ndef setp(i,text): replacements[i]=text\n"+s[b:]
a=s.index('for text,style in selection:');b=s.index('setp(4,',a)
s=s[:a]+s[b:]
a=s.index('for table,rows in zip(doc.tables,tables):');b=s.index('# Recreate compact',a)
s=s[:a]+s[b:]
a=s.index('for i,name,height in [(6,')
s=s[:a]+"(OUT/'report_content.json').write_text(json.dumps({'paragraphs':replacements,'selection':selection,'tables':tables},ensure_ascii=False),encoding='utf-8')\nprint('Prepared report content and charts from notebook results.')\n"
Path('src/prepare_selected_report.py').write_text(s,encoding='utf-8')
