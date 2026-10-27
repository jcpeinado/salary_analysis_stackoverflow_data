from pathlib import Path
import shutil
src=Path('tmp/dashboard_site');dst=Path('dashboard')
for name in ['dist','tools']:
 shutil.copytree(src/name,dst/name,dirs_exist_ok=True)
for name in ['README.md','COVERAGE.md','VALIDATION.md','requirements.txt']:
 shutil.copy2(src/name,dst/name)
