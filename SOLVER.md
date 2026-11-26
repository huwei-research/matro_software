# MATRO solver

Release candidate **0.1.0rc3**. Install with `python -m pip install .`.
The installed package depends only on NumPy and SciPy. It does not import the
research workspace, download code, compile Fortran, or load PDFO.

```python
import numpy as np
from matro import minimize

result = minimize(lambda x: (x[0]-1)**2 + 100*(x[1]-x[0]**2)**2,
                  np.array([-1.2, 1.]), maxfev=1500)
print(result.x, result.fun, result.nfev, result.message)
```

The fixed algorithm is `matro-official-python-fullq-001`, not the older
`MATROMainlineSolver`/`matro-fq-v2` under `codes/`. The old programs remain as
historical experiment implementations; installing this package does not install
them. Current implementation uses a scalar Python translation of PDFO 2.2.0
NEWUOA with full quadratic interpolation and coherent metric transport.

## Numerical contract

- Unconstrained scalar minimization, dimension >= 2, finite starting vector.
- Every objective request counts, including interpolation initialization and
  nonfinite values. A positive integer `maxfev` is a hard call limit.
- `mode='sphere'` bypasses metric changes and follows full-q NEWUOA.
- Default `initial_radius=1`, `final_radius=1e-8`; the latter is a length
  resolution, not a gradient tolerance or optimality certificate.
- Signed curvature is retained in the quadratic model. Only the positive
  trust-region metric uses the absolute Hessian spectrum; settings remain fixed.
- Native barriers replace NaN/large positive values internally; raw observations
  remain in `history`. The returned incumbent is the best finite observation.
- `callback` runs after every objective evaluation, not just successful steps.
  Its data are copies. User exceptions are raised with their original cause.
- `return_history=False` omits returned histories and detailed matrix diagnostics;
  the current kernel still internally retains the call journal.

## Arithmetic and portability

`math_backend='auto'` uses the pinned FSINCOS primitive on Windows x86-64, and
portable Python libm elsewhere. `reference` requires Windows x86-64 and executable
memory for a documented 58-byte local CPU routine. `portable` avoids executable
memory on every platform. The Python optimization operations are unchanged.
Bitwise agreement with the pinned Windows reference is claimed only for the
reference backend and verified trajectories, not across platforms or libm builds.
This version is a public release candidate.

## Development and provenance

Run `python -m pip install '.[test]'`, `python -m pytest`, and
`python -m build`. See `kernel_provenance.json` for source hashes and
`src/matro/_newuoa/provenance.json` for translated routine provenance.
MATRO code retains the root MIT license. The translated PDFO kernel and bundled
reference source retain their BSD-3-Clause license in
`src/matro/_newuoa/LICENSE.txt`; it is included in distributions.
No claim is made that the former fully-quadratic/criticality theorem directly
applies to the official-core maintenance rules.
