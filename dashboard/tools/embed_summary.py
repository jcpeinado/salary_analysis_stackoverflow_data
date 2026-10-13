"""Bundle the aggregate summary into HTML so no separate data request is needed."""
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1]
page = root / 'dist/index.html'
html = page.read_text(encoding='utf-8')
html = re.sub(r'<script id="dashboard-data" type="application/json">.*?</script>', '', html, flags=re.S)
data = (root / 'dist/summary.json').read_text(encoding='utf-8').replace('<', r'\u003c')
html = html.replace('<script src="app.js"></script>', '<script src="app.js?v=20261012-2"></script>')
html = html.replace('<script src="app.js?v=20261012-2"></script>', '<script id="dashboard-data" type="application/json">'+data+'</script><script src="app.js?v=20261012-2"></script>')
if 'id="load-status"' not in html:
    html = html.replace('<main', '<div id="load-status" role="status">Loading verified charts and results…</div><noscript><p>This interactive dashboard requires JavaScript to display its charts and results.</p></noscript><main', 1)
page.write_text(html, encoding='utf-8')
