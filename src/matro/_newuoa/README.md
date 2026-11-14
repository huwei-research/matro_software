# Local Python NEWUOA and MATRO core

This directory contains a scalar Python translation of the **maintained PDFO
2.2.0 NEWUOA** sources, with an optional state callback at `NEWUOB` label 100.
It implements full and underdetermined interpolation. The core does not call
PDFO, an optimizer DLL, Fortran, a compiler, or any external executable.

```python
from matro._newuoa import PythonNewuoa

core = PythonNewuoa("plain")
result = core.run(objective, x0, npt=(n + 1) * (n + 2) // 2,
                  rhobeg=0.5, rhoend=1e-8, maxfun=500 * (n + 1))
```

The signature and result fields match the earlier native `NativeNewuoa` adapter.
`PythonNewuoa("hooked")` accepts the existing `OfficialMetricController` callback,
so the metric, model transport, geometry transport, and all tuning values can
be held fixed between native and local Python MATRO. For example:

```python
from matro._controller import solve_official_matro

result = solve_official_matro(
    objective, x0, native=PythonNewuoa("hooked"), mode="adaptive",
    rhobeg=0.5, rhoend=1e-8, max_eval=500 * (len(x0) + 1),
)
```

## Exactness and scope

The compatibility target is the project's pinned **Windows x86_64 gfortran
build of PDFO 2.2.0**, binary64, ordinary round-to-nearest CPU mode. Bitwise
agreement is checked using complete queries and returned states, not final
objective tolerances. The solver preserves Fortran scalar accumulation order,
integer division, integer-power multiplication, workspace aliases, and original
control flow. Neither array dot products nor vectorized sums replace these
operations. `iprint=0` is the supported silent interface; print formatting is
omitted. All six original routines and license are retained for inspection.

`x87_math.py` is a small, explicitly disclosed CPU math compatibility layer.
The pinned gfortran `-O2` build combines all six paired sine/cosine sites in
`TRSAPP`, `BIGLAG`, and `BIGDEN` into x87 `FSINCOS`. Separate `FSIN` / `FCOS`
can differ from `FSINCOS` by one ulp, as found in the saved Watson n=12 state
at NF=3185. Version 002 uses the paired instruction, including the reference
large-argument reduction. Python's Windows math library and NumPy also return
different final bits for some inputs. The layer uses Python's standard `ctypes`
and Windows executable-memory APIs to expose that CPU primitive. It contains no optimizer logic and
load no official optimizer library. They need no compiler and are inspected
through `math_metadata()`. The package therefore uses Python optimizer code
with a local CPU primitive, not a claim that every arithmetic operation is
implemented by the Python interpreter. In this standalone release candidate,
the public API selects portable libm on other platforms and explicitly records
that it does not provide bitwise reference compatibility. Explicit `reference`
selection on an unsupported platform raises an error.

The mathematical NEWUOA algorithm is portable; identical floating-point
trajectories across arbitrary CPUs, compilers, math libraries, or objective
implementations are a separate requirement and are not claimed here.

## Source generation and review

`generate.py` is a deliberately limited translator for the six pinned source
files. It emits `generated.py`, using explicit basic-block control flow.
`source_map.json` links instruction blocks and labels to original Fortran
statements. `provenance.json` records exact input hashes and generated-code hash.
`reference_source/` preserves the input source and is the default regeneration
input, making this folder self-contained. The original project's vendored PDFO
archive is used only when initially creating the folder; runtime reads neither.

`runtime.py` supplies one-based Fortran-order arrays with shared tail views and
scalar IEEE arithmetic. `__init__.py` supplies objective accounting, PDFO's
`2**100` extreme barrier, callback exception handling, and mutable hook views.
Every objective query, including a nonfinite result, is accounted. Hook calls
do not query the objective. Callback exceptions are preserved as the exception
cause, and subsequent internal barrier calls do not invoke the failing user
callback again.

This is an independent research implementation. The existing frozen MATRO-v2
algorithm and previous results are not modified by importing or using it.

## Attribution

The optimization routines originate in M. J. D. Powell's NEWUOA and the
maintained PDFO 2.2.0 source distribution. See the preserved source comments,
`LICENSE.txt`, and `provenance.json`. This translation adds no new claim of
authorship over the original algorithms.
