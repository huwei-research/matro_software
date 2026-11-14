"""Local Python MATRO on the pinned official NEWUOA control flow.

The optimizer does not load PDFO or an official NEWUOA DLL. The translated
core preserves scalar evaluation order and uses a documented local CPU math
compatibility layer where needed to reproduce the reference build.
The original frozen MATROMainlineSolver remains a distinct algorithm.
"""
from __future__ import annotations

from matro._controller import solve_official_matro
from matro._newuoa import PythonNewuoa


def solve_python_matro(fun, x0, *, mode="adaptive", max_eval=3000,
                       rhobeg=1., rhoend=1e-8, diagnostics=True):
    """Solve with fixed MATRO metric settings and the local Python core.

    mode='sphere' skips all metric/state changes and recovers full-q NEWUOA.
    The objective receives physical coordinates. Every call is charged.
    """
    result = solve_official_matro(fun, x0, native=PythonNewuoa("hooked"),
        mode=mode, max_eval=max_eval, rhobeg=rhobeg, rhoend=rhoend,
        diagnostics=diagnostics)
    result["algorithm_id"] = "matro-official-python-fullq-001"
    result["implementation"] = "local_python_scalar_official_control_flow"
    return result
