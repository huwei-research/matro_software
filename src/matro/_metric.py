"""Metric construction and relative-change clipping for MATRO.

Provides:
    hessian_to_metric   – multiple Hessian-to-SPD-metric maps.
    clip_metric_relative – enforce bounded log-ratio between consecutive metrics.
    metric_to_transforms – compute (T, T_inv) = (M^{1/2}, M^{-1/2}).
"""

from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import numpy as np
import numpy.typing as npt

from matro._metric_utils import (
    cap_metric_condition,
    hessian_to_raw_metric,
    metric_to_transform as _mu_metric_to_transform,
    normalize_spd_metric,
    process_raw_metric,
    symmetrise_spd,
)


def hessian_to_metric(
    H_x: npt.NDArray[np.float64],
    metric_map: str,
    opts: Dict[str, Any],
) -> Optional[npt.NDArray[np.float64]]:
    """Convert an x-space Hessian into an SPD metric M.

    Supported *metric_map* values:
        "abs_eig"                 – |eigenvalue| + clip + power + cap + normalize.
        "abs_eig_power"           – explicit synonym for abs_eig with power.
        "detnorm_abs_eig_power"   – same pipeline, guaranteed gmean normalize.
        "square"                  – M = I + beta * H^T H.
    """
    n = H_x.shape[0]
    metric_map = metric_map.lower().strip()

    if metric_map == "square":
        beta = float(opts.get("metric_beta", 1.0))
        sigma = float(opts.get("metric_sigma", 1e-8))
        H = 0.5 * (H_x + H_x.T)
        M_hat = np.eye(n) + beta * (H @ H)
        M_hat = symmetrise_spd(M_hat)
        M_hat = cap_metric_condition(
            M_hat, float(opts.get("metric_cond_cap", 1e6)))
        M_hat = normalize_spd_metric(M_hat, method="gmean")
        evals = np.linalg.eigvalsh(M_hat)
        if float(np.max(evals) / max(np.min(evals), 1e-30)) < 1.0 + 1e-10:
            return None
        return M_hat

    if metric_map in ("abs_eig", "abs_eig_power", "detnorm_abs_eig_power"):
        pipe_opts = dict(opts)
        if metric_map == "detnorm_abs_eig_power":
            pipe_opts["metric_normalize"] = "gmean"
        try:
            M_raw = hessian_to_raw_metric(
                H_x,
                model_kind=str(opts.get("metric_model_kind", "abs_eig")),
                min_curv=float(opts.get("metric_sigma", 1e-8)),
                max_curv=float(opts.get("metric_m_max", 1e8)),
            )
            return process_raw_metric(M_raw, pipe_opts)
        except Exception:
            return None

    raise ValueError(f"Unknown metric_map={metric_map!r}")


def damped_geodesic_metric_update(
    M_prev: npt.NDArray[np.float64],
    S: npt.NDArray[np.float64],
    delta_M: float,
    kappa_max: float,
    tol: float = 1e-10,
) -> npt.NDArray[np.float64]:
    return _damped_geodesic_metric_update(
        M_prev,
        S,
        delta_M,
        kappa_max=kappa_max,
        tol=tol,
    )


def _damped_geodesic_metric_update(
    M_prev: npt.NDArray[np.float64],
    S: npt.NDArray[np.float64],
    delta_M: float,
    kappa_max: float,
    tol: float = 1e-10,
) -> npt.NDArray[np.float64]:
    """Return a damped affine-invariant geodesic update from M_prev to S."""
    M_prev = 0.5 * (M_prev + M_prev.T)
    S = 0.5 * (S + S.T)

    evals_M, Q_M = np.linalg.eigh(M_prev)
    if float(np.min(evals_M)) <= 0.0:
        raise ValueError("M_prev must be positive definite.")

    sqrt_M = Q_M @ np.diag(np.sqrt(evals_M)) @ Q_M.T
    inv_sqrt_M = Q_M @ np.diag(1.0 / np.sqrt(evals_M)) @ Q_M.T

    C = inv_sqrt_M @ S @ inv_sqrt_M
    C = 0.5 * (C + C.T)

    mu, P = np.linalg.eigh(C)
    if float(np.min(mu)) <= 0.0:
        raise ValueError("Relative matrix must be positive definite.")

    ell = np.log(mu)
    L = float(np.max(np.abs(ell)))
    omega = 1.0 if L <= tol else min(1.0, float(delta_M) / L)

    M_next = sqrt_M @ P @ np.diag(np.exp(omega * ell)) @ P.T @ sqrt_M
    M_next = 0.5 * (M_next + M_next.T)

    rel = inv_sqrt_M @ M_next @ inv_sqrt_M
    rel = 0.5 * (rel + rel.T)
    rel_eigs = np.linalg.eigvalsh(rel)

    det_next = float(np.linalg.det(M_next))
    cond_next = float(np.linalg.cond(M_next))

    if not np.all(rel_eigs >= np.exp(-delta_M) * (1.0 - 100.0 * tol)):
        raise AssertionError("Relative lower sandwich bound failed.")
    if not np.all(rel_eigs <= np.exp(delta_M) * (1.0 + 100.0 * tol)):
        raise AssertionError("Relative upper sandwich bound failed.")
    if np.isfinite(kappa_max) and cond_next > kappa_max * (1.0 + 100.0 * tol):
        raise AssertionError("Condition-number cap failed.")
    if det_next <= 0.0 or abs(np.log(det_next)) > 1000.0 * tol:
        raise AssertionError("Determinant normalization failed.")

    return M_next


def clip_metric_relative(
    M_old: npt.NDArray[np.float64],
    M_new: npt.NDArray[np.float64],
    delta_M: float,
    m_min: float = 1e-8,
    m_max: float = 1e8,
    kappa_max: Optional[float] = None,
) -> Tuple[npt.NDArray[np.float64], float, float]:
    """Take a damped geodesic metric step with a bounded relative change.

    Returns (M_next, max_log_change_before, max_log_change_after).
    """
    if delta_M <= 0 or not np.isfinite(delta_M):
        return M_new.copy(), 0.0, 0.0

    d_old, V_old = np.linalg.eigh(symmetrise_spd(M_old))
    if float(np.min(d_old)) <= 0.0:
        raise ValueError("M_old must be positive definite.")
    inv_sqrt_old = V_old @ np.diag(1.0 / np.sqrt(d_old)) @ V_old.T

    A = inv_sqrt_old @ symmetrise_spd(M_new) @ inv_sqrt_old
    lam = np.linalg.eigvalsh(0.5 * (A + A.T))
    if float(np.min(lam)) <= 0.0:
        raise ValueError("Relative matrix must be positive definite.")

    log_lam = np.log(lam)
    max_log_before = float(np.max(np.abs(log_lam)))

    if kappa_max is None:
        kappa_max = float(m_max) / max(float(m_min), 1e-300)
    M_next = _damped_geodesic_metric_update(
        M_old,
        M_new,
        delta_M,
        float(kappa_max),
    )

    A_next = inv_sqrt_old @ M_next @ inv_sqrt_old
    lam_next = np.linalg.eigvalsh(0.5 * (A_next + A_next.T))
    max_log_after = float(np.max(np.abs(np.log(lam_next))))

    return M_next, max_log_before, max_log_after


def metric_to_transforms(
    M: npt.NDArray[np.float64],
) -> Tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Compute (T, T_inv) where T = M^{1/2} and T_inv = M^{-1/2}."""
    d, V = np.linalg.eigh(symmetrise_spd(M))
    d = np.maximum(d, 1e-14)
    T = V @ np.diag(np.sqrt(d)) @ V.T
    T_inv = V @ np.diag(1.0 / np.sqrt(d)) @ V.T
    return T, T_inv
