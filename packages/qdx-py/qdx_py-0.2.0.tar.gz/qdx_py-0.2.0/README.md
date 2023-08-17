# QDX-py

Python bindings to qdx-commons, built with [maturin / py03](https://pyo3.rs).

## Usage

``` python
import qdx_py
# get json string of conformer
conformer = qdx_py.pdb_to_conformer(open("../qdx-common/tests/data/6mj7.pdb").read())
# get pdb of conformer
pdb = qdx_py.conformer_to_pdb(conformer)
```

## Developing

``` sh
~ setup venv
maturin develop
python
~ import qdx_py
```
