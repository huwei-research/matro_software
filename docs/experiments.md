# Experimental protocol and reproduction

The tables and figures in manuscript v15.6 use the paired benchmark records
and plotting inputs included with the solver. The reproduction guide lists
the programs for regenerating them.

## 1. Fixed comparison

There are 147 instances, twenty starts per instance, and six methods: MATRO,
full-interpolation NEWUOA, NEWUOA with `2*n+1` points, unconstrained COBYQA,
Nelder–Mead, and CMA-ES. The 2940 paired tasks produce 17640 runs. All twenty
starts of every instance enter every profile. The collection contains
41 Moré–Wild configurations and 106 CUTEst configurations evaluated through
S2MPJ. Dimensions 2 through 12 have counts
`46, 22, 15, 4, 17, 7, 18, 2, 6, 1, 9`, respectively. Moré–Wild identifiers retain
the collection's distinct dimensions and author starting scales.

Observed MATRO and full NEWUOA performance informed the development of the
benchmark settings. The reported comparisons describe performance on these 147
configurations.

### Coordinates and paired starts

For each paired task, all six solvers start at `z = 0` on the same objective

$$F_j(z)=f(x_0^{(j)}+Az).$$

The 147 final instance identifiers and objective identities are recorded in
`instances.csv.gz`. Each instance fixes the invertible matrix $A$ and the initial
scalar radius.
The twenty physical starts $x_0^{(j)}$ are recorded in `starts.csv.gz`.
Of the 147 coordinate maps, 126 are identities, 19 are nonidentity diagonal
maps, and two are rotated scalings with condition number 100.

The input-coordinate Hessian and physical metric satisfy

$$H_z=A^T H_x A,\qquad M_x=A^{-T}M_zA^{-1}.$$

The quadratic model and adaptive metric are constructed in the supplied
variable `z`.

### Reference values and target counts

There are 136 objective identities among the 147 instances. For each
identity, the reference used in the analysis is the minimum of the declared
values and the finite objective values recorded during initial setup and solver
runs. All methods and starts share that reference.

For each run and target `tau` in `1e-3, 1e-5, 1e-7, 1e-9`, the first-hit count
is the first actual query satisfying

$$f_{\min}(N)-f_{\mathrm{ref}}
\le\tau\,[f(x_0)-f_{\mathrm{ref}}].$$

The budget is `B = 500*(n+1)`. Initialization, geometry maintenance, and
repeated queries all count. A target not attained by termination or the budget
has infinite first-hit count; a finite attained target remains credited.
Profiles use exact query-level first-hit records, independently of the
subsampled display curves. Every task has equal weight, including failures.
For a task failed by all methods, every performance ratio is infinite. Capped
counts assign `B` to failures.

## 2. Solver and software settings

The benchmark ran on Windows x86_64 with CPython 3.12.10, NumPy 1.26.4,
SciPy 1.17.1, and pycma 4.5.0. `benchmark_environment.json` records the full
environment. Later mechanism runs use CPython 3.13.6 and NumPy 2.3.2, with
separate archived source and environment records.

MATRO and both NEWUOA variants use the local scalar core translated from the
PDFO 2.2.0 distribution. The run snapshots identify the scalar-access and
objective-evaluation optimizations that preserve the core arithmetic. MATRO
and full NEWUOA begin with identical complete interpolation sets of
`(n+1)*(n+2)//2` points; standard NEWUOA uses `2*n+1`. The final radius is
`1e-8` for trust-region methods.

| Method | Recorded settings |
| --- | --- |
| MATRO | `matro-official-python-fullq-001`; spectral floor `1e-8`, ceiling `1e8`, metric condition cap `1e4`, determinant normalization, relative log-metric update bound `0.5`; initial metric identity |
| Full NEWUOA | Same complete-interpolation core, metric updates disabled, `M = I` |
| COBYQA | `scipy.optimize.minimize`, no bounds or constraints, `scale=False`, shared initial/final radii, `maxfev=B`, `maxiter=max(1000*n, 10*B)` |
| Nelder–Mead | Initial simplex `{0, Delta0*e_1, ..., Delta0*e_n}`, `adaptive=False`, `xatol=1e-8`, `fatol=1e-12`; evaluation budget set with no additional iteration limit |
| CMA-ES | Mean zero, isotropic covariance, initial standard deviation `Delta0`, default population and updates, saved positive algorithm seed, no restarts |

MATRO recomputes its target after the first full model and after strict
incumbent improvement at a completed-model boundary. See
[algorithm documentation](algorithm.md) and the solver source for the exact
update and acceptance rules.

CMA-ES evaluates and charges the common start before its first population.
The final mean is evaluated when budget remains; a final partial population
is charged without exceeding the budget.

## 3. Anisotropy and metric comparisons

The four instances and original initial radii are:

| Instance | Function | Dimension | Initial radius | Budget |
| --- | --- | ---: | ---: | ---: |
| MW 07 | Rosenbrock | 2 | 0.1 | 1500 |
| MW 12 | Powell singular | 4 | 8 | 2500 |
| MW 19 | Watson | 6 | 0.25 | 3500 |
| MW 27 | Brown–Dennis | 4 | 8 | 2500 |

For each of the twenty benchmark physical starts, the coordinate scan uses

$$A_{\kappa,r}=Q_r\operatorname{diag}(\kappa^{a_i})Q_r^T,
\qquad a_i=-\tfrac12+\frac{i-1}{n-1}.$$

Both orthogonal orientations remain fixed across
`1, 2, 3, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000,
100000`. These maps have determinant one and condition number `kappa`.
Rosenbrock's first orientation recovers its benchmark map at `kappa=100`;
the other three original benchmark maps are identities. At `kappa=1` the
coincident orientations have equal statistical weight without duplicate runs.

Pointwise 95% bootstrap intervals use 2000 resamples of twenty starting-point
blocks. Each block retains both methods, both orientations, and all condition
values. The success ordinate is the mean target-attainment indicator; the
budget ordinate is the mean capped first-hit count, on a linear scale from zero.
The horizontal coordinate is the map condition number, not a measured Hessian
condition number.

The shape comparison retains the original benchmark maps and twenty starts.
All four variants share the full-interpolation core and radius rules. The
diagonal variant applies magnitude, clipping, determinant normalization, and
bounded updates to the model Hessian diagonal in solver coordinates. The
frozen variant stores the first complete-model target and continues bounded
updates toward that target. It therefore permits metric changes until the
stored target is reached. The sphere and dynamic-full variants use full
NEWUOA and MATRO unchanged.

## 4. Fixed-state interpolation and decrease

The coverage figure uses
`f(x) = (1-x1)**2 + 100*(x2-x1**2)**2` from a development trajectory starting
at `(2,4)` with initial radius `1`. After sixteen function evaluations the
center is approximately `(1.90557688, 3.63205861)` and the current radius is
`0.1`. Six fixed points define one quadratic model. The metric has determinant
one to floating-point precision and ellipse axis ratio `4.448339`. The two
prediction domains have equal area `pi*0.1**2`.

Figure 1 shows the objective contours and the two regions in physical
displacements, with $s_2/\Delta$ horizontal and $s_1/\Delta$ vertical. The absolute-error heatmap uses square-root color normalization
and saturates above `0.4`. Area fractions use equal-area quadrature. The
root-mean-square error is

$$\operatorname{RMS}(E)=
\left(|E|^{-1}\int_E|f(x_k+s)-m_k(s)|^2\,ds\right)^{1/2}.$$

The disk and ellipse values are `0.1848557` and `0.0245556`; the area fractions
with absolute error at most `0.1` are `70.906%` and `99.392%`.

The offline candidates globally minimize this fixed quadratic over their
respective domains. The original two-dimensional computation compares all
boundary stationary points and feasible interior stationary points. The
independent reconstruction solves the trust-region secular equation and checks
the boundary norm, stationarity, and positive semidefiniteness of the shifted
Hessian. Solver trajectories continue to use the inherited NEWUOA subproblem
routine.

For the exact Rosenbrock Taylor remainder,

$$\mathcal R_x(s)=400x_{k,1}s_1^3-200s_1^2s_2+100s_1^4,$$

the reconstruction checks the Lagrange-difference reduction-error identity
with residual below `2.3e-14`. Full-precision samples and metric are in
`fixed_state_input.json`; `fixed_state_reconstruction.json` records the
decomposition, conditions, hashes, and environment. The script uses nine
offline objective evaluations: six sample checks, one center evaluation, and
two candidate evaluations. It starts no optimization trajectory and supplies
no additional values to any compared solver.

## 5. Descent and trajectory plotting

Benchmark descent curves use pointwise medians over all twenty starts, with
interquartile bands for MATRO and full NEWUOA. Incumbent values are step
functions and are carried forward after termination. Gaps below `1e-10` are
shown at the lower axis limit. Exact first-hit counts are read independently
from the display curves. The nine examples illustrate favorable MATRO runs.
Each example includes all twenty starts.

The four spatial examples have the following definitions and inputs:

| Example | Function or transform | Start | Initial radius |
| --- | --- | --- | ---: |
| Rosenbrock | `(1-x1)**2 + 1e4*(x2-x1**2)**2` | `x0=(1.5,2.45)` | 0.4 |
| Cubic valley | `(1-x1)**2 + 1e3*(x2-x1**3)**2` | `x0=(-1,-1.3)` | 0.8 |
| Lévy | `g(x)=f(A*x)`, `kappa=30`, `theta=pi/4` | `u0=A*x0=(-1,0.5)` | 2 |
| Different Powers | `g(x)=u1**2+u2**6`, `u=A*x`, `kappa=3`, `theta=pi/6` | `u0=(-3,0.3)` | 0.025 |

Here

$$A=Q_\theta\operatorname{diag}(\sqrt\kappa,1/\sqrt\kappa)Q_\theta^T,$$

where `Q_theta` is the standard planar rotation. Lévy uses `w_i=1+(u_i-1)/4`
and

$$f(u)=\sin^2(\pi w_1)+(w_1-1)^2[1+10\sin^2(\pi w_1+1)]
 +(w_2-1)^2[1+\sin^2(2\pi w_2)].$$

All four examples use six interpolation points, budget `1500`, and final radius
`1e-8`. Unrounded inputs are stored in `trajectory_cases.json`.

The four examples illustrate cases in which the metric produced earlier
target attainment. The neighborhood check uses eight other starts per
function, each paired with three radius multipliers (0.8, 1, 1.25).
MATRO uses fewer evaluations to reach the target in 24, 16, 24 and 24 of
these 24 comparisons for the four examples in table order. The grouped
summaries are in `trajectory_neighbors.csv`.

Spatial curves connect recorded trust-region centers through the first
attainment of relative gap `1e-9`, ending at the best evaluated point at that
time. The lower panels mark `1e-7` for the count comparison. Up to nine actual
regions are chosen at equal increments of cumulative center travel. Regions
with long semiaxis below 2.2% or above 170% of the common view width are omitted
from the display. Retained regions keep their recorded sizes and are clipped
at the common window. Background objective grids are computed offline and
never supplied to the optimizers. The figure inputs retain the histories,
displayed states, and selected indices.

## 6. Reproduce the manuscript results

The [reproduction instructions](../reproduction/README.md) list the Python
dependencies and commands. Table 1 is computed from the compact run records.
Table 2 uses the six fixed interpolation samples. The plotting program reads
the archived inputs to generate the eight manuscript figures.
