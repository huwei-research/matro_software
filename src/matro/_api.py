"""Public API. The numerical controller and fixed metric settings are unchanged."""
from __future__ import annotations
import copy
import numbers
import numpy as np
from scipy.optimize import OptimizeResult
from ._solver import solve_python_matro
from ._newuoa.x87_math import backend, metadata

_MESSAGES = {0: 'Final trust-region resolution reached (not a stationarity certificate).',
             1: 'Target function value reached.',
             2: 'Trust-region subproblem failed to reduce the model.',
             3: 'Maximum number of function evaluations reached.',
             5: 'Invalid interpolation set size.',
             -1: 'NaN encountered in the optimization variables.',
             -2: 'Nonfinite objective values prevented progress.',
             -3: 'Nonfinite numerical model encountered.'}

def minimize(fun, x0, *, args=(), maxfev=3000, initial_radius=1.0,
             final_radius=1e-8, mode='adaptive', math_backend='auto',
             callback=None, return_history=True):
    """Minimize a scalar objective without derivatives or constraints.

    Parameters
    ----------
    fun : callable
        ``fun(x, *args)`` receives an independent finite-dimensional array.
    x0 : array_like
        Finite vector of dimension at least two.
    maxfev : int
        Hard objective-call budget, including interpolation initialization.
    initial_radius, final_radius : float
        Require ``0 < final_radius <= initial_radius``.
    mode : {'adaptive', 'sphere'}
        Fixed MATRO, or unchanged full-interpolation NEWUOA control flow.
    math_backend : {'auto', 'reference', 'portable'}
        Auto uses the pinned reference CPU arithmetic on Windows x86-64 and
        Python libm elsewhere. Portable arithmetic is not bitwise reference parity.
    callback : callable, optional
        Called after every paid objective evaluation with a copied dictionary
        containing ``nfev, x, fun``. It is an evaluation callback, not an accepted
        iteration callback. Exceptions propagate (wrapped by the numerical core).
    return_history : bool
        Include all queried points/values and metric-update events in the result.

    Returns
    -------
    scipy.optimize.OptimizeResult
        ``x, fun`` are the best finite observed point/value; ``nfev`` is the paid
        count; ``status`` retains the native status. ``success`` means normal
        native termination with a finite result, not proven optimality.
    """
    if not callable(fun):
        raise TypeError('fun must be callable')
    if np.iscomplexobj(x0):
        raise ValueError('x0 must be a finite real vector')
    if isinstance(maxfev, bool) or not isinstance(maxfev, numbers.Integral) or maxfev < 1:
        raise ValueError('maxfev must be a positive integer')
    if callback is not None and not callable(callback):
        raise TypeError('callback must be callable')
    count = 0
    def objective(x):
        nonlocal count
        point = np.array(x, dtype=float, copy=True)
        value = np.asarray(fun(point.copy(), *args))
        if value.ndim != 0:
            raise ValueError('fun must return a scalar')
        value = float(value)
        count += 1
        if callback is not None:
            callback(dict(nfev=count, x=point, fun=value))
        return value
    with backend(math_backend):
        raw = solve_python_matro(objective, x0, mode=mode, max_eval=int(maxfev),
                                 rhobeg=initial_radius, rhoend=final_radius,
                                 diagnostics=return_history)
        arithmetic = metadata()
    native = raw['native_result']
    status = int(native['status'])
    result = OptimizeResult(x=raw['best_x'], fun=raw['best'], nfev=raw['actual_calls'],
        success=status in (0, 1) and np.isfinite(raw['best']), status=status,
        message=_MESSAGES.get(status, f'Native NEWUOA status {status}.'),
        algorithm_id=raw['algorithm_id'] if mode == 'adaptive' else 'newuoa-official-python-fullq-001',
        implementation_id=native['implementation'], math_backend=arithmetic,
        metric=raw['final_metric'].copy(), metric_updates=raw['metric_updates'],
        specification=copy.deepcopy(raw['specification']),
        native_x=raw['native_physical_x'].copy(), native_fun=native['fun'])
    if return_history:
        result.history = raw['calls']
        result.metric_history = raw['metric_events']
    return result
