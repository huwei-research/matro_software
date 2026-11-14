"""Full-interpolation state transport for the official NEWUOA core.

These operations buy no function values. They are only valid at full q, not
for NEWUOA's usual underdetermined 2*n+1 models. See docs/algorithm.md in
the source distribution for the fixed algorithm and transport contract.
"""
from __future__ import annotations

import numpy as np
import scipy.linalg as la


def quadratic_design(points):
    """Rows [1, x, x_i**2/sqrt(2), x_i*x_j], upper triangular order."""
    points = np.asarray(points, dtype=float)
    if points.ndim != 2:
        raise ValueError("points must have shape (q, n)")
    q, n = points.shape
    columns = [np.ones(q)] + [points[:, i] for i in range(n)]
    for j in range(n):
        for i in range(j + 1):
            columns.append(points[:, i] * points[:, j] /
                           (np.sqrt(2.) if i == j else 1.))
    return np.column_stack(columns)


def full_geometry_factors(points, *, condition_limit=1e10):
    """Rebuild BMAT/ZMAT for exactly q poised points, with IDZ=1.

    If F=[P,Q], QQ.T=.5*(X@X.T)**2 and F^-1=[L;D], the full
    interpolation KKT inverse is [[D.T@D,L.T],[L,0]]. The affine constant
    column is omitted in NEWUOA's BMAT convention. Scale before solving to
    avoid inverse fourth powers of tiny distances in the linear solve.
    """
    points = np.asarray(points, dtype=float)
    q, n = points.shape
    if q != (n + 1) * (n + 2) // 2 or not np.all(np.isfinite(points)):
        raise ValueError("finite full-q interpolation points required")
    scale = float(np.max(np.abs(points)))
    if not np.isfinite(scale) or scale <= 0:
        raise ValueError("collapsed interpolation geometry")
    normalized = points / scale
    design = quadratic_design(normalized)
    condition = float(np.linalg.cond(design))
    if not np.isfinite(condition) or condition > condition_limit:
        raise ValueError(f"transport design condition {condition} exceeds {condition_limit}")
    inverse = la.solve(design, np.eye(q), assume_a="gen", check_finite=False)
    inverse_residual = float(np.linalg.norm(design @ inverse - np.eye(q), ord=np.inf))
    if inverse_residual > 1e-7:
        raise ValueError(f"transport inverse residual {inverse_residual}")
    bmat = np.zeros((q + n, n), order="F")
    bmat[:q] = inverse[1:n + 1].T / scale
    zmat = np.asfortranarray(inverse[n + 1:].T / scale**2)
    if not (np.all(np.isfinite(bmat)) and np.all(np.isfinite(zmat))):
        raise ValueError("nonfinite interpolation factors")
    return bmat, zmat, dict(scale=scale, design_condition=condition,
                           inverse_residual_inf=inverse_residual)


def unpack_hessian(hq, pq, points):
    """Read Powell's explicit upper triangle plus implicit rank-one terms."""
    points = np.asarray(points, dtype=float)
    n = points.shape[1]
    hessian = np.zeros((n, n))
    k = 0
    for j in range(n):
        for i in range(j + 1):
            hessian[i, j] = hessian[j, i] = hq[k]
            k += 1
    hessian += points.T @ (np.asarray(pq)[:, None] * points)
    return .5 * (hessian + hessian.T)


def pack_hessian(hessian):
    n = hessian.shape[0]
    return np.array([hessian[i, j] for j in range(n) for i in range(j + 1)])


def prepare_transport(*, xbase, xopt, xnew, last_x, points, values, gq,
                      hq, pq, kopt, anchor, transform, next_transform,
                      condition_limit=1e10):
    """Prepare an atomic change from x=a+S*z to x=a_new+S_new*z_new.

    transform is S, mapping core coordinates to physical coordinates, not
    M**.5. Recenter at the existing best interpolation point. Physical
    locations/values and the signed model are preserved. Caller commits
    all arrays plus anchor/S together, or keeps the old state untouched.
    """
    points = np.asarray(points, dtype=float)
    values = np.asarray(values, dtype=float)
    n = points.shape[1]
    q = (n + 1) * (n + 2) // 2
    if points.shape != (q, n) or not 0 <= kopt < q:
        raise ValueError("transport only supports full-q interpolation")
    if not all(np.all(np.isfinite(a)) for a in
               (xbase, xopt, last_x, points, values, gq, hq, pq,
                anchor, transform, next_transform)):
        raise ValueError("nonfinite source state")
    old_hessian = unpack_hessian(hq, pq, points)
    old_center_gradient = np.asarray(gq) + old_hessian @ xopt
    change = la.solve(next_transform, transform, check_finite=False)
    reverse = la.solve(transform, next_transform, check_finite=False)
    new_points = (points - xopt) @ change.T
    new_gradient = reverse.T @ old_center_gradient
    new_hessian = reverse.T @ old_hessian @ reverse
    new_hessian = .5 * (new_hessian + new_hessian.T)
    new_anchor = np.asarray(anchor) + transform @ (xbase + xopt)
    bmat, zmat, stats = full_geometry_factors(
        new_points, condition_limit=condition_limit)
    old_offsets = points - xopt
    old_prediction = old_offsets @ old_center_gradient + .5 * np.einsum(
        "ki,ij,kj->k", old_offsets, old_hessian, old_offsets)
    new_prediction = new_points @ new_gradient + .5 * np.einsum(
        "ki,ij,kj->k", new_points, new_hessian, new_points)
    data_scale = max(1., float(np.max(np.abs(values - values[kopt]))))
    old_residual = float(np.max(np.abs(values[kopt] + old_prediction - values))) / data_scale
    new_residual = float(np.max(np.abs(values[kopt] + new_prediction - values))) / data_scale
    prediction_change = float(np.max(np.abs(old_prediction - new_prediction))) / data_scale
    physical_displacement_error = float(np.max(np.abs(
        old_offsets @ transform.T - new_points @ next_transform.T)))
    location_scale = max(1., float(np.max(np.abs(old_offsets @ transform.T))))
    if prediction_change > 1e-8 or new_residual > max(1e-7, 10 * old_residual):
        raise ValueError("model transport residual too large")
    if physical_displacement_error > 1e-10 * location_scale:
        raise ValueError("physical interpolation points changed")
    if np.linalg.norm(new_points[kopt]) > 1e-10 * max(1., stats["scale"]):
        raise ValueError("best point is not the transformed center")
    stats.update(old_interpolation_residual=old_residual,
                 new_interpolation_residual=new_residual,
                 prediction_change_relative=prediction_change,
                 physical_displacement_error=physical_displacement_error)
    return dict(xbase=np.zeros(n), xopt=np.zeros(n),
                # XNEW is scratch at this hook and is uninitialized directly
                # after the initial model; official code overwrites it before use.
                xnew=np.zeros(n),
                last_x=change @ (last_x - xbase - xopt),
                points=np.asfortranarray(new_points), gq=new_gradient,
                hq=pack_hessian(new_hessian), pq=np.zeros(q),
                bmat=bmat, zmat=zmat, idz=1, xoptsq=0.,
                anchor=new_anchor, transform=np.asarray(next_transform).copy(),
                stats=stats)
