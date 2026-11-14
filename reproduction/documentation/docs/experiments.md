# Experimental protocol and reproduction

This document records the protocol behind the MATRO manuscript's fixed
147-instance comparison and its shape-mechanism figures. It accompanies the
v14.1 manuscript and source distribution. The manuscript retains the scientific
comparisons, mathematical definitions, and conclusions; this document supplies
initialization, software, data, and plotting details.

The solver in the Research/matro repository is `src/matro`, with API
`matro.minimize` and configuration `matro-official-python-fullq-001`. The
historical `codes/experiments/paper/` scripts belong to earlier experiments.
The current 147-instance records and the commands below use the compact
evidence included in this manuscript source archive, under `data/` and
`statistics/`. The Research/matro repository maintains the manuscript in
`paper/` and the original experiment archives at their recorded locations. Current
solver source is in `src/matro`, and experiment programs are in `codes/`.

## 1. Fixed comparison

There are 147 instances, twenty starts per instance, and six methods: MATRO,
full-interpolation NEWUOA, NEWUOA with `2*n+1` points, unconstrained COBYQA,
Nelder–Mead, and CMA-ES. The 2940 paired tasks produce 17640 runs. All twenty
starts of every retained instance enter every profile. The collection contains
41 Moré–Wild configurations and 106 CUTEst configurations evaluated through
S2MPJ. Dimensions 2 through 12 have counts
`46, 22, 15, 4, 17, 7, 18, 2, 6, 1, 9`, respectively. Moré–Wild identifiers retain
the collection's distinct dimensions and author starting scales.

The collection was assembled according to the distribution of functions in
the source test sets, with interest in anisotropic and ill-conditioned
objectives. The saved candidate table has 211 configurations: 158 CUTEst/S2MPJ
and 53 Moré–Wild. Exactly 147 configurations satisfy the recorded eligibility
checks, and all 147 are retained. The performance score in the saved analysis
orders these configurations; it does not truncate the eligible collection.
The eligibility checks use numerical validity, target attainment by any
compared method, and triviality/discrimination diagnostics. Per-function
initialization calibration and the later selection of illustrative curves
are separate operations. The statistical documentation and compact records in
[the statistical documentation](../../statistics/README.md) give the exact counts, rules, and mapping.

### Coordinates and paired starts

For an instance, let `c` be its physical center, `A` its fixed invertible
coordinate matrix, `Delta0` its initial scalar radius, and `d` its perturbation
scale vector. Start `j`, for `j = 0,...,19`, is

$$
x_0^{(j)}=c+0.1\,2^{-b_j}\operatorname{diag}(d)\xi_j,
\qquad \xi_j\sim N(0,I).
$$

The solver starts at `z = 0` on

$$F_j(z)=f(x_0^{(j)}+Az).$$

All methods receive the same map, physical start, and scalar initial radius.
`b_j` is the first nonnegative backtracking index for which the initial value
is finite with magnitude below `2**100`; indices 0 through 20 are tried. The
check uses objective validity alone. A repeated physical start caused by
floating-point resolution raises an error. The selected 2940 starts are stored
explicitly, so reproduction can read them without regenerating random draws.

The frozen protocol constructs positive integer seeds as follows:

```python
import hashlib

def stable_seed(*parts):
    payload = "|".join(map(str, parts)).encode()
    value = int.from_bytes(hashlib.sha256(payload).digest()[:4], "little")
    return value % (2**31 - 2) + 1

start_seed = stable_seed("start", 20261030, instance_id, start_id)
algorithm_seed = stable_seed("cma", 20261030, instance_id, start_id)
```

`numpy.random.default_rng(start_seed).normal(size=n)` generates the start
perturbation. The second seed is supplied to CMA-ES. The stored start file
contains both seeds and the backtracking index.

The input-coordinate Hessian and physical metric satisfy

$$H_z=A^T H_x A,\qquad M_x=A^{-T}M_zA^{-1}.$$

The model and adaptive metric are constructed in the supplied variable `z`.
The internal NEWUOA coordinates provide a further changing representation of
this same supplied objective.

### Per-instance initialization

Fifty-four retained instances use settings from earlier development runs;
ninety-three use the following calibration. For a generic author start
`x_author`, candidate centers are `x_author`, `0.5*x_author`, and
`1.5*x_author`, with duplicate or invalid centers removed. If documented
physical parameter scales are available, the centers are instead the author
center and two displacements

$$c\pm0.25\operatorname{diag}(d)\eta,$$

where `eta` is a normal draw seeded with
`stable_seed("calibration_anchor", instance_id)`.
Candidate radii are `0.1, 0.25, 0.5, 1, 2`. Identity coordinates are always
included. A diagonal physical-scale map is also considered for documented
parameter scales or nonzero parameter magnitudes whose ratio is at least 100.

Each candidate is run with MATRO and full NEWUOA at budget `250*(n+1)`.
Selection first requires stable completed runs, then favors MATRO target
attainment and a larger full-NEWUOA/MATRO first-hit ratio. These inputs are
fixed before generating the twenty fresh paired starts. Earlier settings can
have radii outside this grid; the exact saved values govern reproduction.

### Retained-instance rules

The fixed collection requires complete six-method records, no terminal errors,
no nonfinite model states, and no nonfinite or extreme objective queries
(`abs(f) >= 2**100`). At relative target `1e-7`:

- At least 20% of starts must be solved by some method.
- At most 80% may be solved within `max(5, n+1)` queries.
- At least 20% must discriminate through unequal success or a ratio of at least
  1.2 between the largest and smallest successful first-hit counts.

For eligible instances the saved score is

```text
4*(MATRO_success - full_NEWUOA_success)
+ mean(log(full_capped / MATRO_capped))
+ 0.15*mean(log(best_other_capped / MATRO_capped))
+ 0.15*min(6, log10(max(1, curvature_dispersion)))
```

Success terms are fractions. The curvature dispersion is an offline diagnostic:
a finite-difference absolute-Hessian spectral ratio when available, otherwise
declared structural evidence or axial central-second-difference dispersion
from full NEWUOA's first-start initialization. The diagnostic is recorded with
its source. Distinct author-start configurations are retained; verified
cross-library duplicate entries with an explicit `duplicate_of` marker are
excluded. `selection_rules.json` is the machine-readable specification and
`selected147_instances.csv.gz` records the actual selection.

### Reference values and target counts

Reference values are unified by base-objective identity across author starting
scales, methods, calibration runs, and saved attempts. Each reference is the
minimum of the declared values and all finite saved observations for that
identity. There are 136 objective identities among the 147 instances. The
reference is used only in analysis.

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
counts assign `B` to failures. The archived analysis chooses the first completed
attempt, or otherwise the latest terminal attempt; all attempt expenditures
are separately retained in the original records.

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
eligibility and acceptance rules. No solver rule changes were made in the
editorial revisions.

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

The displayed coordinates use one common orthogonal rotation and divide both
axes by `0.1`. The absolute-error heatmap uses square-root color normalization
and saturates above `0.4`. Area fractions use equal-area quadrature. The
root-mean-square error is

$$\operatorname{RMS}(E)=
\left(|E|^{-1}\int_E|f(x_k+s)-m_k(s)|^2\,ds\right)^{1/2}.$$

The disk and ellipse values are `0.1848557` and `0.0245556`; the area fractions
with absolute error at most `0.1` are `70.906%` and `99.392%`. This state was
selected for a readable axis ratio and a clear coverage difference.

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
from the display curves. The nine examples were selected for favorable MATRO
behavior across different function structures; all twenty starts enter each
example.

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

The configuration search covered ten function families and 5242 distinct inputs.
The displayed examples were chosen for evaluation advantage at multiple targets,
different structures, and readable actual regions. After fixing them, eight
new start perturbations per function were crossed with radius multipliers
`0.8, 1, 1.25`, giving 24 neighboring comparisons per function. Base-coordinate
perturbations have independent uniform coordinates at amplitude
`0.01*max(1, norm(u0-u_star))`, using seed `2026110917`. Both methods reach
`1e-7` in every comparison. MATRO uses fewer evaluations in `24,16,24,24`
cases, with median full-NEWUOA/MATRO ratios `2.624,1.130,2.068,1.900`.
`trajectory_neighbors.csv` retains these grouped summaries.

Spatial curves connect recorded trust-region centers through the first
attainment of relative gap `1e-9`, ending at the best evaluated point at that
time. The lower panels mark `1e-7` for the count comparison. Up to nine actual
regions are chosen at equal increments of cumulative center travel. Regions
with long semiaxis below 2.2% or above 170% of the common view width are omitted
from the display. Retained regions keep their recorded sizes and are clipped
at the common window. Background objective grids are computed offline and
never supplied to the optimizers. The figure inputs retain the histories,
displayed states, and selected indices.

## 6. Compact evidence files

The evidence distribution uses the following layout, relative to its revision
directory. CSV files are gzip-compressed and can be read row by row.

| File under `data/` | Content |
| --- | --- |
| `selected147_instances.csv.gz` | 147 identifiers, source suite, dimension, objective identity, numerical validity, paired performance, and selection scores |
| `initialization.csv.gz` | One row per instance: `center`, `matrix`, `radius`, `perturbation_scale`, reference, source, condition, and candidate identifier |
| `starts.csv.gz` | 2940 starts: instance/start identifiers, `physical_start`, `solver_start`, radius, budget, `start_seed`, `start_backtracks`, initialization source, and `algorithm_seed` |
| `runs.csv.gz` | 70560 run–target rows: `job_id`, `instance_id`, `start_id`, `method`, `n`, `budget`, `radius`, `f0`, `reference`, `actual_calls`, `target`, `hit`, and `success` |
| `references.csv.gz` | 136 objective identities and declared, observed, and unified reference values |
| `selection_rules.json` | Eligibility, ranking formula, duplicate handling, target and reference definitions |
| `benchmark_environment.json` | Recorded benchmark interpreter and dependency versions |
| `mechanism_inputs.json` | Full-precision shared mechanism starts, coordinate maps, radii, and budgets |
| `conditioning_summary.csv`, `shape_summary.csv`, `coverage_metrics.json` | Numerical summaries of the mechanism comparisons |
| `nine_example_metrics.csv` | Exact target counts for the nine descent examples |
| `trajectory_cases.json`, `trajectory_neighbors.csv` | Four displayed configurations and neighboring-start summary groups |
| `fixed_state_input.json`, `fixed_state_reconstruction.py`, `fixed_state_reconstruction.json` | Independent fixed-six-point calculation |
| `figure_inputs/` | Frozen compact profile arrays, descent curves, coverage field, trajectory states, and background grids for all eight main figures |
| `source_manifest.json` | Original source locations, source/output SHA-256 digests, frozen configuration and execution hashes, and storage budgets |

The compact distribution preserves all comparison denominators, pair identities,
failures, exact target counts, selected inputs, and plotting data. Complete raw
query journals, every candidate configuration, and full model-state histories
remain in the research archives identified by the manifest. Absolute historical
paths in the manifest document provenance; the checks below read local compact
files and do not require those historical paths.

The source collections include the received November 4 benchmark analysis
(`received_selection_20261104`, experiment `MATRO_selection_20261030`), and the
November 9 profile, mechanism, and trajectory figure archives. The raw data
remain preserved. This document relocates explanation only.

The compact data budget is 8 MB, with a 2 MB per-file bound. Statistical
verification has a 256 MiB memory budget and figure regeneration a 768 MiB
budget. The inherited evidence records approximately 0.93 MB of statistics
and 5,376,817 bytes of plotting inputs, with a largest plotting file of
1,182,573 bytes. Recorded isolated checks used about 48 MB for statistics and
312,606,720 bytes for drawing. Actual file hashes, byte counts, and checks are
recorded next to their versioned artefacts.

## 7. Verified reproduction entry points

Use the compact evidence distribution matching the manuscript version. The
following commands apply to the v14.1 distribution. The paths below are
relative to its revision directory, containing `data/` and `figures/`:

```text
python data/verify_data.py
python -m pip install -r data/requirements_figures.txt
python figures/redraw_figures.py
```

The first command checks paired inputs, counts, target bookkeeping, success
tables, anisotropy summaries, and compact-file hashes. The plotting script
reads only `data/figure_inputs/`, writes PDF/SVG/PNG outputs alongside itself,
and performs no objective queries. Copy both the data directory and plotting
script while preserving their relative paths. These commands reproduce the
existing analysis and figures from their retained numerical inputs.

For the fixed-state calculation, with NumPy and SciPy available:

```text
python data/fixed_state_reconstruction.py --output fixed_state_recheck.json
```

Use a new output name so that the archived reconstruction remains intact.
This command performs the nine offline evaluations described above. It is
separate from figure redrawing and statistical verification.

Fresh optimization runs require the archived experiment source, problem
sources, and full configuration identified by `source_manifest.json`.
The historical public `codes/experiments/paper` entry points do not themselves
implement this frozen 147-instance campaign. The versioned compact evidence
supports independent reanalysis without launching that campaign.
