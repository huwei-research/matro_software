"""Independently reconstruct the two fixed-model steps; run no optimizer trajectory.

Run: python fixed_state_reconstruction.py
Requires NumPy and SciPy. Physical displacements are s = x - center.
The quadratic basis is [1, s1, s2, s1**2/2, s1*s2, s2**2/2].
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform

import numpy as np
import scipy
from scipy.optimize import brentq


def basis(displacements):
    z = np.atleast_2d(displacements)
    return np.column_stack([np.ones(len(z)), z, z[:, 0] ** 2 / 2,
                            z[:, 0] * z[:, 1], z[:, 1] ** 2 / 2])


def reconstruct(state):
    center = np.array(state["center"])
    points = np.array(state["points"])
    values = np.array(state["values"])
    offsets = points - center
    delta = state["delta"]
    design = basis(offsets)
    coefficients = np.linalg.solve(design, values)
    inverse = np.linalg.inv(design)
    gradient = coefficients[1:3]
    hessian = np.array([[coefficients[3], coefficients[4]],
                        [coefficients[4], coefficients[5]]])
    objective_calls = 0

    def objective(x):
        nonlocal objective_calls
        objective_calls += 1
        return float((1 - x[0]) ** 2 + 100 * (x[1] - x[0] ** 2) ** 2)

    def taylor_remainder(displacements):
        z = np.atleast_2d(displacements)
        return (400 * center[0] * z[:, 0] ** 3
                - 200 * z[:, 0] ** 2 * z[:, 1] + 100 * z[:, 0] ** 4)

    independently_evaluated_values = np.array([objective(p) for p in points])
    center_value = objective(center)
    residuals = basis(offsets) @ coefficients - values
    results = []
    for name, metric in [("sphere", np.eye(2)),
                         ("learned_ellipse", np.array(state["metric"]))]:
        eigenvalues, eigenvectors = np.linalg.eigh(metric)
        transform = (eigenvectors * eigenvalues ** -0.5) @ eigenvectors.T
        induced_hessian = transform.T @ hessian @ transform
        induced_gradient = transform.T @ gradient
        b, u = np.linalg.eigh(induced_hessian)
        g = u.T @ induced_gradient

        def secular(multiplier):
            return np.linalg.norm(g / (b + multiplier)) - delta

        lower = max(0.0, -min(b)) + 1e-10
        upper = max(1.0, 2 * lower)
        while secular(upper) > 0:
            upper *= 2
        multiplier = brentq(secular, lower, upper, xtol=1e-12)
        induced_step = -u @ (g / (b + multiplier))
        step = transform @ induced_step
        predicted = float(-(gradient @ step + 0.5 * step @ hessian @ step))
        actual = center_value - objective(center + step)
        weights = ((basis(step) - basis(np.zeros(2))) @ inverse)[0]
        sample_term = float(weights @ (residuals + taylor_remainder(offsets)))
        trial_term = float(taylor_remainder(step)[0])
        kkt_residual = float(np.linalg.norm(induced_gradient
                            + induced_hessian @ induced_step
                            + multiplier * induced_step))
        identity_residual = float(actual - predicted - sample_term + trial_term)
        shifted_minimum_eigenvalue = float(min(b) + multiplier)
        assert kkt_residual < 1e-9
        assert shifted_minimum_eigenvalue >= 0
        assert abs(np.linalg.norm(induced_step) - delta) < 1e-10
        assert abs(identity_residual) < 1e-10
        results.append(dict(
            region=name, metric=metric.tolist(), physical_step=step.tolist(),
            predicted_decrease=predicted, actual_decrease=actual,
            acceptance_ratio=actual / predicted,
            absolute_reduction_error=abs(actual - predicted),
            lagrange_differences=weights.tolist(),
            lambda_dec=float(sum(abs(weights))),
            weighted_sample_residual_and_remainder=sample_term,
            trial_taylor_remainder=trial_term,
            exact_identity_residual=identity_residual,
            kkt_multiplier=multiplier, kkt_residual=kkt_residual,
            shifted_hessian_minimum_eigenvalue=shifted_minimum_eigenvalue,
            relative_sample_radius=float(max(np.linalg.norm(
                offsets @ np.linalg.cholesky(metric), axis=1)) / delta)))
    return dict(
        question="Same six-point quadratic, center and radius; compare two equal-area domains.",
        coordinate_convention="Physical s=x-center; induced y=M**(1/2)s; L=M**(-1/2).",
        objective="f(x)=(1-x1)^2+100*(x2-x1^2)^2",
        taylor_remainder="R(s)=400*center1*s1^3-200*s1^2*s2+100*s1^4",
        exact_identity="ared-pred=sum_i((ell_i(s)-ell_i(0))*(r_i+R(s_i)))-R(s)",
        optimizer_trajectories_started=0,
        offline_objective_evaluations=objective_calls,
        offline_objective_evaluation_breakdown=dict(sample_validation=6, center=1, candidates=2),
        subproblem_method="Secular root above -lambda_min; boundary norm, stationarity and positive shifted Hessian checked.",
        model_coefficients=coefficients.tolist(), gradient=gradient.tolist(),
        hessian=hessian.tolist(), hessian_eigenvalues=np.linalg.eigvalsh(hessian).tolist(),
        maximum_sample_value_discrepancy=float(max(abs(independently_evaluated_values-values))),
        maximum_interpolation_residual=float(max(abs(residuals))), results=results)


def main():
    here = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, default=here / "fixed_state_input.json")
    parser.add_argument("--output", type=Path, default=here / "fixed_state_recheck.json")
    args = parser.parse_args()
    data = args.state.read_bytes()
    state = json.loads(data)
    result = reconstruct(state)
    result.update(input_path=args.state.name,
                  input_sha256=hashlib.sha256(data).hexdigest(),
                  input_state=state,
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  environment=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__))
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
