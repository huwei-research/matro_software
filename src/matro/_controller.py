"""Research candidate: PDFO's full-q NEWUOA core with coherent metric transport.

The frozen MATROMainlineSolver is unchanged. This candidate inherits the
official center, radius, geometry and subproblem decisions; it does not claim
the old MATRO criticality/fully-quadratic convergence theorem unchanged.
"""
from __future__ import annotations

import numpy as np
import scipy.linalg as la

from matro._metric import hessian_to_metric, clip_metric_relative, metric_to_transforms
from matro._transport import prepare_transport, unpack_hessian


METRIC_OPTIONS = dict(metric_model_kind="abs_eig", metric_sigma=1e-8,
    metric_m_max=1e8, metric_power=1., metric_cond_cap=1e4,
    metric_cap_mode="clip_high", metric_normalize="gmean")


def _scalar(state, key):
    return np.asarray(state[key]).reshape(-1)[0].item()


class OfficialMetricController:
    """Atomic changes at the completed-model boundary before official TRSAPP."""

    def __init__(self, n, *, adaptive=True, relative_clip=.5, diagnostics=True):
        self.n = n
        self.adaptive = bool(adaptive)
        self.relative_clip = float(relative_clip)
        if self.relative_clip <= 0 or not np.isfinite(self.relative_clip):
            raise ValueError("relative_clip must be finite and positive")
        self.diagnostics = diagnostics
        self.anchor = np.zeros(n)
        self.transform = np.eye(n)
        self.metric = np.eye(n)
        self.events = []
        self.last_nf = -1
        self.last_seen_best = np.inf
        self.updates = 0
        self.identity_mapping = True

    def physical_point(self, coordinates):
        # This branch is also the exact official-sphere recovery path.
        if self.identity_mapping:
            return np.asarray(coordinates, dtype=float).copy()
        return self.anchor + self.transform @ coordinates

    def hook(self, state):
        nf = int(_scalar(state, "nf"))
        if nf == self.last_nf:
            return
        self.last_nf = nf
        q = (self.n + 1) * (self.n + 2) // 2
        if int(_scalar(state, "npt")) != q:
            raise ValueError("metric transport requires full quadratic interpolation")
        # Native callback exports the original Fortran 1-based index.
        kopt = int(_scalar(state, "kopt")) - 1
        values = np.asarray(state["fval"])
        best = float(values[kopt])
        improved = best < self.last_seen_best
        self.last_seen_best = min(self.last_seen_best, best)
        if not self.adaptive or not improved:
            return
        event = dict(nfev=nf, status="proposed", best=best,
            delta=float(_scalar(state,"delta")), rho=float(_scalar(state,"rho")),
            metric_before=self.metric.copy(), reason="initial_model_or_improved_best")
        try:
            hessian_y = unpack_hessian(state["hq"],state["pq"],state["xpt"])
            inverse_transform = la.solve(self.transform,np.eye(self.n),check_finite=False)
            hessian_x = inverse_transform.T @ hessian_y @ inverse_transform
            target = hessian_to_metric(hessian_x,"abs_eig",METRIC_OPTIONS)
            if target is None:
                event["status"] = "no_nonidentity_target"
                return
            next_metric, before, after = clip_metric_relative(
                self.metric,target,self.relative_clip,kappa_max=1e4)
            event.update(relative_log_before=before,relative_log_after=after)
            if after <= 1e-10:
                event["status"] = "unchanged_metric"
                return
            _, next_transform = metric_to_transforms(next_metric)
            candidate = prepare_transport(xbase=state["xbase"], xopt=state["xopt"],
                xnew=state["xnew"], last_x=state["x"], points=state["xpt"],
                values=values,gq=state["gq"],hq=state["hq"],pq=state["pq"],kopt=kopt,
                anchor=self.anchor,transform=self.transform,next_transform=next_transform)
            event.update(candidate["stats"])
            # Refuse a transformation of an already inaccurate full model.
            if candidate["stats"]["old_interpolation_residual"] > 1e-7:
                event["status"] = "inaccurate_source_model"
                return
            if self.diagnostics:
                event.update(center=candidate["anchor"].copy(),
                    hessian_physical=hessian_x.copy(),metric_after=next_metric.copy(),
                    old_points=np.asarray(state["xpt"]).copy(),
                    new_points=candidate["points"].copy(),
                    old_transform=self.transform.copy(),new_transform=next_transform.copy())
            # Every fallible operation precedes this joint commit.
            for native, prepared in (("xbase","xbase"),("xopt","xopt"),
                    ("xnew","xnew"),("x","last_x"),("xpt","points"),
                    ("gq","gq"),("hq","hq"),("pq","pq"),
                    ("bmat","bmat"),("zmat","zmat")):
                state[native][...] = candidate[prepared]
            state["idz"][...] = 1
            state["xoptsq"][...] = 0.
            state["itest"][...] = 0
            self.anchor = candidate["anchor"]
            self.transform = next_transform
            self.metric = next_metric
            self.identity_mapping = False
            self.updates += 1
            event["status"] = "committed"
        except (ValueError, np.linalg.LinAlgError, AssertionError) as exc:
            event.update(status="transport_rejected",error=str(exc))
        finally:
            self.events.append(event)


def solve_official_matro(fun, x0, *, native, mode="adaptive", max_eval=3000,
                         rhobeg=.5, rhoend=1e-8, diagnostics=True):
    """Run one uninterrupted official core, with every real request charged.

    native is an explicitly constructed NativeNewuoa binding. No compiler,
    package installation or source download is triggered by this function.
    """
    x0 = np.asarray(x0,dtype=float)
    if x0.ndim != 1 or len(x0) < 2 or not np.all(np.isfinite(x0)):
        raise ValueError("official NEWUOA requires a finite x0 and n>=2")
    if mode not in ("sphere","adaptive"):
        raise ValueError("mode must be sphere or adaptive")
    n=len(x0); q=(n+1)*(n+2)//2
    controller=OfficialMetricController(n,adaptive=mode=="adaptive",diagnostics=diagnostics)
    calls=[]

    def objective(z):
        x=controller.physical_point(z)
        # Record all requests, including nonfinite values and exceptions.
        record=dict(nfev=len(calls)+1,x=x.copy(),core_x=np.asarray(z).copy(),
                    metric_id=controller.updates)
        calls.append(record)
        try:
            value=float(fun(x))
            record["f"]=value
            return value
        except Exception as exc:
            record["error"]=repr(exc)
            raise

    result=native.run(objective,x0.copy(),npt=q,rhobeg=rhobeg,rhoend=rhoend,
                      maxfun=max_eval,hook=controller.hook)
    finite=[r for r in calls if np.isfinite(r.get("f",np.inf))]
    best=min(finite,key=lambda r:r["f"]) if finite else None
    return dict(native_result=result,native_physical_x=controller.physical_point(result["x"]),
        calls=calls,actual_calls=len(calls),
        best_x=None if best is None else best["x"],
        best=np.inf if best is None else best["f"],
        metric_events=controller.events,metric_updates=controller.updates,
        final_metric=controller.metric,mode=mode,
        algorithm_id="matro-official-fullq-experimental-001",
        specification=dict(npt=q,rhobeg=rhobeg,rhoend=rhoend,max_eval=max_eval,
            metric_options=METRIC_OPTIONS,relative_clip=.5,
            metric_trigger="initial full model then strictly improved best at TR boundary",
            geometry="official NEWUOA; full-q algebra is not the old MATRO FQ quality predicate",
            state_transport="preserve physical paid points and signed model; no restart or pilot",
            source_residual_limit=1e-7,transport_condition_limit=1e10,
            stationary_certificate=False))
