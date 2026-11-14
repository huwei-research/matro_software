# MATRO

MATRO minimizes scalar functions without derivatives using quadratic interpolation and Hessian-derived ellipsoidal trust regions.

```sh
python -m pip install .
python examples/rosenbrock.py
```

```python
from matro import minimize
result = minimize(lambda x: (x[0]-1)**2 + 100*(x[1]-x[0]**2)**2,
                  [-1.2, 1.], maxfev=1500)
print(result.x, result.fun, result.nfev)
```

Version 0.1.0rc2 is the software release candidate. The installed solver is
`src/matro`, algorithm `matro-official-python-fullq-001`.

- [API and numerical contract](SOLVER.md)
- [Algorithm and implementation](docs/README.md)
- [147-instance experimental protocol](docs/experiments.md)
- [Kernel source provenance](kernel_provenance.json)

Install test dependencies with `python -m pip install '.[test]'`, run
`python -m pytest tests`, and build with `python -m build`.
The historical `codes/` directory in earlier distributions is retained for
historical research and is outside the installed package.

The MATRO code uses the MIT license. The translated PDFO kernel and bundled
reference sources retain BSD-3-Clause; see `src/matro/_newuoa/LICENSE.txt`.

Compact data and figure reproduction: [reproduction](reproduction/README.md).

Repository: https://github.com/huwei-research/matro_software
