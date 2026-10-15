"""Execute the notebook and refresh the report's intermediate calculation cache.
Run with a Python environment containing the notebook libraries, nbformat and nbclient.
Then run build_selected_report.py with a Python environment containing python-docx.
"""
from pathlib import Path
import os
import nbformat
from nbclient import NotebookClient
ROOT=Path(__file__).resolve().parents[1]
os.chdir(ROOT)
(ROOT/'tmp/sample_selection').mkdir(parents=True,exist_ok=True)
p=ROOT/'notebooks/peinado_1012953314_assignment1.ipynb'
n=nbformat.read(p,as_version=4)
n.cells.append(nbformat.v4.new_code_cell('''import pickle
_export = {}
for _k, _v in list(globals().items()):
    if not _k.startswith('_') and isinstance(_v, (str, int, float, list, tuple, dict, np.ndarray, pd.DataFrame, pd.Series, np.number)):
        try:
            pickle.dumps(_v)
            _export[_k] = _v
        except Exception:
            pass
with open('tmp/sample_selection/results.pkl', 'wb') as _f:
    pickle.dump(_export, _f)
'''))
NotebookClient(n,timeout=1200,startup_timeout=60,kernel_name='python3',
    on_cell_start=lambda cell,cell_index: print('Executing cell',cell_index,flush=True),
    resources={'metadata':{'path':str(ROOT)}}).execute()
n.cells.pop()
nbformat.write(n,p)
print('Saved fully executed notebook and calculation cache.')
