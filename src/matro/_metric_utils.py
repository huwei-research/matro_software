# Copyright 2026 huwei@amss.ac.cn. All rights reserved.

"""Shared metric pipeline for ellipsoidal trust-region solvers.

Functions here are solver-agnostic: they convert a symmetric (possibly
indefinite) Hessian into an SPD metric suitable for an ellipsoidal
trust region, applying spectral processing, power scaling, condition
capping, normalisation, and gating.

Extracted from ``solvers.ew_newuoa.ew_newuoa`` so that any solver
(EW-NEWUOA, DFO-ETR adaptive instance, etc.) can reuse the same
metric construction pipeline.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import numpy as np
import numpy.typing as npt


# ------------------------------------------------------------------
# Low-level SPD helpers
# ------------------------------------------------------------------

def symmetrise_spd(
    M: npt.NDArray[np.float64],
    jitter: float = 1e-10,
) -> npt.NDArray[np.float64]:
    """Symmetrise and jitter until Cholesky-factorisable."""
    M = 0.5 * (M + M.T)
    n = M.shape[0]
    for _ in range(8):
        try:
            np.linalg.cholesky(M)
            return M
        except np.linalg.LinAlgError:
            M = M + jitter * np.eye(n)
    return M + 1e-6 * np.eye(n)


def is_identity_metric(
    M: Optional[npt.NDArray[np.float64]],
    n: int,
    *,
    rtol: float = 1e-10,
    atol: float = 1e-12,
) -> bool:
    """True if *M* is absent or numerically the identity."""
    if M is None:
        return True
    A = np.asarray(M, dtype=np.float64).reshape(n, n)
    return bool(np.allclose(A, np.eye(n), rtol=rtol, atol=atol))


def diag_spd_power(
    M: npt.NDArray[np.float64],
    power: float,
) -> npt.NDArray[np.float64]:
    """Apply ``Q diag(lam**power) Q^T``."""
    if abs(power - 1.0) < 1e-14:
        return M
    evals, evecs = np.linalg.eigh(symmetrise_spd(M))
    evals = np.maximum(evals, 1e-14)
    return evecs @ np.diag(evals ** power) @ evecs.T


def cap_metric_condition(
    M: npt.NDArray[np.float64],
    cond_cap: float,
    *,
    mode: str = "clip_high",
) -> npt.NDArray[np.float64]:
    """Cap the SPD spectrum by clipping its top or raising its bottom.

    The default preserves the historical high-end clipping rule. The two
    rules share a conditioning bound but generally produce different shapes.
    A cap of one produces a scalar matrix, hence identity after normalization.
    """
    if np.isnan(cond_cap) or cond_cap < 1.0:
        raise ValueError("cond_cap must be at least one.")
    if mode not in ("clip_high", "raise_low"):
        raise ValueError(f"Unknown metric cap mode: {mode!r}")
    if np.isinf(cond_cap):
        return M
    evals, evecs = np.linalg.eigh(symmetrise_spd(M))
    evals = np.maximum(evals, 1e-14)
    if mode == "clip_high":
        evals = np.minimum(evals, float(np.min(evals)) * float(cond_cap))
    else:
        evals = np.maximum(evals, float(np.max(evals)) / float(cond_cap))
    return evecs @ np.diag(evals) @ evecs.T


def normalize_spd_metric(
    M: npt.NDArray[np.float64],
    *,
    method: str = "gmean",
) -> npt.NDArray[np.float64]:
    """Normalize so the metric encodes shape rather than arbitrary scale."""
    method = method.lower().strip()
    A = symmetrise_spd(np.asarray(M, dtype=np.float64))
    if method in ("none", "", "off"):
        return A
    evals, evecs = np.linalg.eigh(A)
    evals = np.maximum(evals, 1e-14)
    if method == "gmean":
        scale = float(np.exp(np.mean(np.log(evals))))
    elif method == "trace":
        scale = float(np.mean(evals))
    elif method == "median":
        scale = float(np.median(evals))
    else:
        raise ValueError(f"Unknown normalize method={method!r}")
    scale = max(scale, 1e-14)
    return evecs @ np.diag(evals / scale) @ evecs.T


# ------------------------------------------------------------------
# High-level pipeline
# ------------------------------------------------------------------

def hessian_to_raw_metric(
    H: npt.NDArray[np.float64],
    *,
    model_kind: str = "abs_eig",
    min_curv: float = 1e-8,
    max_curv: float = 1e8,
) -> npt.NDArray[np.float64]:
    """Convert a (possibly indefinite) symmetric Hessian to a raw SPD metric.

    First step of the pipeline: ``H -> |lambda| -> clip``.
    """
    H = 0.5 * (H + H.T)
    kind = str(model_kind).lower().strip()
    if kind == "diag_abs":
        diag = np.clip(np.abs(np.diag(H)), min_curv, max_curv)
        return np.diag(diag)
    if kind != "abs_eig":
        raise ValueError(f"Unknown model_kind={model_kind!r}")
    evals, evecs = np.linalg.eigh(H)
    evals = np.clip(np.abs(evals), min_curv, max_curv)
    return evecs @ np.diag(evals) @ evecs.T


def process_raw_metric(
    M_raw: npt.NDArray[np.float64],
    opts: Dict[str, Any],
) -> Optional[npt.NDArray[np.float64]]:
    """Full pipeline: ``symmetrise -> power -> cap -> normalize -> gate``.

    Returns ``None`` when the processed metric is effectively the identity.
    """
    n = M_raw.shape[0]
    M = symmetrise_spd(np.asarray(M_raw, dtype=np.float64).reshape(n, n))
    M = diag_spd_power(M, float(opts.get("metric_power", 1.0)))
    M = cap_metric_condition(
        M, float(opts.get("metric_cond_cap", np.inf)),
        mode=str(opts.get("metric_cap_mode", "clip_high")),
    )
    M = normalize_spd_metric(M, method=str(opts.get("metric_normalize", "gmean")))

    gate_cond = float(opts.get("metric_gate_cond", 1.0))
    if gate_cond > 1.0:
        evals = np.linalg.eigvalsh(M)
        cond = float(np.max(evals) / max(np.min(evals), 1e-14))
        if cond < gate_cond:
            return None
    if is_identity_metric(M, n):
        return None
    return M


def metric_to_transform(
    M: npt.NDArray[np.float64],
) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
    """Compute ``(eigvals, V)`` and ``T_inv = V diag(1/sqrt(d)) V^T``.

    Returns ``(M_eig_tuple, T_inv)`` where ``M_eig_tuple = (d, V)``
    from ``eigh(M)`` and ``T_inv = M^{-1/2}``.
    """
    d, V = np.linalg.eigh(M)
    d = np.maximum(d, 1e-14)
    sqrt_inv = 1.0 / np.sqrt(d)
    T_inv = V @ np.diag(sqrt_inv) @ V.T
    return (d, V), T_inv
