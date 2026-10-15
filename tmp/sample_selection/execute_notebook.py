import nbformat
from nbclient import NotebookClient
from pathlib import Path
p=Path('notebooks/peinado_1012953314_assignment1.ipynb')
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
NotebookClient(n,timeout=1200,startup_timeout=60,on_cell_start=lambda cell, cell_index: print('Executing cell',cell_index,flush=True),kernel_name='python3',resources={'metadata':{'path':str(Path.cwd())}}).execute()
n.cells.pop()
nbformat.write(n,p)
print('Executed',sum(c.cell_type=='code' for c in n.cells),'code cells')

