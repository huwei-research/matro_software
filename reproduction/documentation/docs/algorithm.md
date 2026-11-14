# Fixed algorithm and model-state transport

The algorithm identifier is `matro-official-python-fullq-001`. The
[implementation reference](implementation.md) gives the exact radius rules,
state transformation, interpolation-factor algebra, acceptance thresholds,
evaluation accounting, and arithmetic backend.

The solver uses q=(n+1)(n+2)/2 interpolation points and the translated PDFO
2.2.0 NEWUOA control flow (initialization, model/geometry update, TRSAPP,
radius resolution and native stopping). At a completed-model boundary,
the first model or a strictly improved incumbent may trigger a metric update.

The signed physical Hessian H is reconstructed from HQ, PQ and XPT. Its absolute
eigenvalues are clipped to [1e-8,1e8], high eigenvalues are capped at 1e4 times
the smallest, and the resulting matrix is normalized by its geometric mean.
The actual metric update is clipped to a relative logarithmic spectral distance
of 0.5. A near-identity target retains the old metric.

The metric only defines the region. The optimization model retains negative
curvature. If x=a+L w, the physical trust region is the image of the core's ball
under L=M^(-1/2). A metric change keeps already paid physical sample locations and
values. It transforms the polynomial, reconstructs the full quadratic
interpolation geometry, and jointly commits state only after all preparation
checks have succeeded. Source-model relative interpolation residual above 1e-7
or unacceptable transport conditioning causes rejection of the metric proposal.
This does not restart NEWUOA or buy pilot samples.

Sphere mode bypasses this controller's changes, preserving the original scalar
operations. Exact reference arithmetic is platform-specific as described in
[SOLVER.md](../SOLVER.md). Complete interpolation algebra alone does not establish uniform
poisedness or the earlier MATRO fully-quadratic/criticality assumptions.

Implementation correspondence: `_controller.py` selects/commits the metric;
`_metric.py` and `_metric_utils.py` form and clip SPD matrices; `_transport.py`
changes polynomial/interpolation coordinates; `_newuoa/generated.py` contains the
translated official numerical routines; `_api.py` validates the public API and
reports the best finite observation and paid-query history.
