# MATRO implementation

This document specifies the local release candidate
`matro-official-python-fullq-001`, exposed by `matro.minimize`. It complements
the [algorithm description](algorithm.md) and [solver contract](../SOLVER.md).
The installed solver uses the scalar Python translation of the maintained
PDFO 2.2.0 NEWUOA core with complete quadratic interpolation. It requires
NumPy and SciPy; optimization does not load PDFO, compile Fortran, or call
an external optimizer.

## Fixed algorithm and source map

All source paths below are relative to the Research/matro repository root.
The source tree is maintained separately from this manuscript archive.

For dimension $n\geq2$, the interpolation size is
$q=(n+1)(n+2)/2$. The quadratic model retains its signed Hessian. The metric
is formed from the physical Hessian $H_x=V\operatorname{diag}(\lambda_i)V^T$:

$$
a_i=\min\{10^8,\max\{10^{-8},|\lambda_i|\}\},\qquad
\bar a_i=\min\{a_i,10^4\min_j a_j\},\qquad
S=V\operatorname{diag}(\bar a_i/\bar a_g)V^T,
\quad \bar a_g=\Bigl(\prod_i\bar a_i\Bigr)^{1/n}.
$$

Starting at $M=I$, the proposed update is

$$
C=M^{-1/2}SM^{-1/2},\qquad d=\|\log C\|_2,\qquad
\omega=\begin{cases}1,&d=0,\\\min\{1,0.5/d\},&d>0,\end{cases}
\qquad M_+=M^{1/2}C^\omega M^{1/2}.
$$

The controller considers the initial complete model, then models associated
with a strict improvement of the best sampled value. It acts at the
completed-model event corresponding to `NEWUOB` label 100, before `TRSAPP`,
at most once for each function-evaluation count. A numerically identity
target retains the current metric. The same applies to a negligible update
or a failed transport check. After a rejected proposal, another strict
improvement is required before a later proposal. The metric settings above
are fixed in the candidate; the public API exposes the initial point,
radii, evaluation budget, mode, and arithmetic backend.

| Operation | Source |
|---|---|
| Public inputs, return value, and evaluation callback | `src/matro/_api.py` |
| Algorithm identifier and local core | `src/matro/_solver.py` |
| Proposal timing, physical Hessian, and joint state update | `src/matro/_controller.py` |
| Relative geodesic update and matrix roots | `src/matro/_metric.py` |
| Spectral regularization, cap, normalization, and identity test | `src/matro/_metric_utils.py` |
| Polynomial transport and full interpolation factors | `src/matro/_transport.py` |
| Scalar NEWUOA routines | `src/matro/_newuoa/generated.py` |
| Core interface and extreme barrier | `src/matro/_newuoa/__init__.py` |
| Arithmetic compatibility | `src/matro/_newuoa/x87_math.py` |

## Initialization, radius, and termination

The initial interpolation set contains $x_0$, the $2n$ points
$x_0\pm r_{\mathrm{beg}}e_i$, and one point
$x_0+r_{\mathrm{beg}}(\epsilon_i e_i+\epsilon_j e_j)$ for each unordered
pair $i\neq j$. Here $\epsilon_i=-1$ when the negative axial point has a
smaller value than the positive axial point, and $\epsilon_i=1$ otherwise.
The query order is the one in the retained
`src/matro/_newuoa/reference_source/newuob.f`. Once all $q$
values are available, their minimum determines the initial model center
and the first metric proposal can be considered. A smaller budget can end
the run during this initialization.

Write $\Delta$ for the trust-region radius and $r$ for the resolution
scale (`DELTA` and `RHO` in NEWUOA). The symbol $\rho$ below denotes the
actual-to-predicted reduction ratio. Initially $\Delta=r=r_{\mathrm{beg}}$.
For a trust-region step $y$, let $d=\min\{\Delta,\|y\|\}$. After a trial
with positive predicted reduction, the radius rule is

$$
\Delta_+=
\begin{cases}
d/2,&\rho\leq0.1,\\
\max\{\Delta/2,d\},&0.1<\rho\leq0.7,\\
\max\{\Delta/2,2d\},&\rho>0.7.
\end{cases}
$$

If $\Delta_+\leq1.5r$, it is replaced by $r$. Every improved function
value updates the best point, including improvements at geometry points.
`TRSAPP` solves the subproblem; `BIGLAG`, `BIGDEN`, and `UPDATE` provide
the retained point-replacement, geometry, and factor updates.

For a short step $d<r/2$, the core first divides $\Delta$ by ten, subject
to the same reset to $r$. Recent model prediction errors and sample
distances determine whether to improve the geometry or reduce the
resolution. In the distance test, a sample farther than $2\Delta$ from
the best point can be replaced by a geometry step of length

$$
d_{\mathrm{geom}}
=\max\{\min\{0.1d_{\mathrm{far}},\Delta/2\},r\},
$$

where $d_{\mathrm{far}}$ is measured in current core coordinates. At a
new resolution stage, with $u=r/r_{\mathrm{end}}$, the update is

$$
r_+=\begin{cases}
r_{\mathrm{end}},&u\leq16,\\
\sqrt{r r_{\mathrm{end}}},&16<u\leq250,\\
0.1r,&u>250,
\end{cases}
\qquad \Delta_+=\max\{r/2,r_+\}.
$$

The core's original tests determine when a resolution stage is complete.
The run ends at the requested final resolution, the evaluation budget,
or a numerical termination reported by the core. The API defaults are
`initial_radius=1.0`, `final_radius=1e-8`, and `maxfev=3000`. Final
resolution is a length parameter. The native status and best finite
observed value are returned separately. Experiment-specific inputs belong
to [the experiment records](experiments.md).

## Model representation and coordinate transport

The physical coordinate map is $x=a+Lw$, where $L=M^{-1/2}$. Let $b$ be
the core base point, $c$ the displacement of its best point from that
base, and $Z$ the matrix whose rows are the sample displacements $z_i^T$.
In storage these are `xbase`, `xopt`, and `xpt`. Thus

$$
x_i=a+L(b+z_i),\qquad x_c=a+L(b+c).
$$

In the mathematical description, $T=M^{1/2}$ maps physical displacements
to induced coordinates, so $L=T^{-1}$. The controller's `transform` and
the transport routine's `transform` argument store $L$. The helper
`metric_to_transforms` returns the pair $(T,L)$.

The core Hessian has the explicit-plus-implicit representation

$$
H=H_Q+Z^T\operatorname{diag}(p)Z.
$$

`hq` stores the upper triangle of $H_Q$ by columns; `pq` stores $p$.
`unpack_hessian` reconstructs this signed matrix and symmetrizes it. If
$g$ (`gq`) is the gradient at the core base, then the center gradient is
$g_c=g+Hc$, and the physical Hessian is $L^{-T}HL^{-1}$.

For a proposed $L_+=M_+^{-1/2}$, define

$$
A=L_+^{-1}L,\qquad a_+=x_c,\qquad w_+=A(w-b-c),\qquad
Z_+=(Z-\mathbf1c^T)A^T,\qquad
g_+=A^{-T}g_c,\qquad H_+=A^{-T}HA^{-1}.
$$

The implementation uses linear solves for the coordinate changes. The new
base and best displacement are zero. It stores the full $H_+$ in `hq`
and sets `pq` to zero; sampled values and the best-sample index are retained.
The affine translation explicitly accounts for the old internal base and best-point
displacement. A mismatch between the retained best sample and the transformed
origin causes rejection by the existing center check; no separate incumbent-state
repair is performed.

To verify polynomial preservation, write the old model about its best
point as $f_b+g_c^Tu+\tfrac12u^THu$, where $u=w-b-c$. Substituting
$u=A^{-1}v$ gives $f_b+g_+^Tv+\tfrac12v^TH_+v$. Physical samples are
also unchanged, since

$$
a_++L_+A(z_i-c)=a+L(b+c)+L(z_i-c)=a+L(b+z_i).
$$

Consequently the transformation preserves the signed quadratic and its
physical sample locations in exact arithmetic, without new function
values. The scalar radius $\Delta$ and resolution $r$ are unchanged.
The transformed state is prepared before any current arrays are replaced.

The successful commit updates `xbase`, `xopt`, `xnew`, the last `x`,
`xpt`, `gq`, `hq`, `pq`, `bmat`, and `zmat`, together with the physical
anchor, transform, and metric. It sets `idz=1`, `xoptsq=0`, and `itest=0`.
`xnew` is scratch at this event and is zeroed; the core overwrites it
before its next use. The last core point becomes
$A(w_{\mathrm{last}}-b-c)$.

## Reconstructing the complete interpolation factors

The reconstruction applies to a full set of $q$ points. For the new rows
$z_i^T$, form $P=[\mathbf1,Z]$ and the quadratic block $Q$ whose columns
are $u_j^2/\sqrt2$ and $u_i u_j$ for $i<j$, evaluated at the samples.
`quadratic_design` orders these columns by $j=1,\ldots,n$, with
$i=1,\ldots,j$ within each $j$. Then

$$
QQ^T=\tfrac12(ZZ^T)\circ(ZZ^T),\qquad F=[P,Q],
$$

where $\circ$ is entrywise multiplication. If $F$ is nonsingular, write

$$
F^{-1}=\begin{bmatrix}U\\V\end{bmatrix},
\qquad U\in\mathbb R^{(n+1)\times q}.
$$

The augmented interpolation inverse is

$$
\begin{bmatrix}QQ^T&P\\P^T&0\end{bmatrix}^{-1}
=\begin{bmatrix}V^TV&U^T\\U&0\end{bmatrix}.
$$

Here is the full algebra. The identity $F^{-1}F=I$ gives
$UP=I$, $UQ=0$, $VP=0$, and $VQ=I$. In the product of the two displayed
block matrices, the upper-left block is
$QQ^TV^TV+PU=QV+PU=FF^{-1}=I$. The upper-right block is zero because
$Q^TU^T=0$; the lower-left block is zero because $P^TV^T=0$; and the
lower-right block is $P^TU^T=I$. This proves the inverse formula.

Under NEWUOA's storage convention, `ZMAT` is $V^T$ and `IDZ` is one.
The first $q$ rows of `BMAT` are the transpose of the linear-coefficient
rows of $U$; its remaining $n$ rows are zero. The constant row of $U$
is omitted.

For numerical reconstruction, let $h=\max_{i,j}|Z_{ij}|>0$. Construct
$\widehat F$ from $Z/h$ and solve
$\widehat F W=I$ with `scipy.linalg.solve`. If
$W=[\widehat U^T,\widehat V^T]^T$, store

$$
\mathrm{ZMAT}=h^{-2}\widehat V^T,\qquad
\mathrm{BMAT}_{1:q,:}=h^{-1}\widehat U_{2:n+1,:}^T.
$$

This rescaling applies only to the interpolation solve. The physical
prediction region and radius retain their intended values.

## Numerical acceptance of a metric update

Let $f_b$ be the best sample value and
$D_f=\max\{1,\max_i|f_i-f_b|\}$. If $\pi_i$ and $\pi_i^+$ denote the old
and transformed predictions at sample $i$, each measured relative to its
model value at the center, define

$$
R_{\mathrm{old}}=\frac{\max_i|f_b+\pi_i-f_i|}{D_f},\qquad
R_{\mathrm{new}}=\frac{\max_i|f_b+\pi_i^+-f_i|}{D_f},\qquad
R_{\mathrm{change}}=\frac{\max_i|\pi_i-\pi_i^+|}{D_f}.
$$

`prepare_transport` checks finite source data used by the transformation,
including sample values and the old model arrays, and requires finite
rebuilt factors. The numerical conditions are:

| Quantity | Requirement |
|---|---|
| Full interpolation size | $q=(n+1)(n+2)/2$ |
| Scaling factor | $h>0$, finite |
| Normalized design condition number | $\operatorname{cond}_2(\widehat F)\leq10^{10}$ |
| Inverse residual | $\|\widehat F W-I\|_\infty\leq10^{-7}$ |
| Old interpolation residual | $R_{\mathrm{old}}\leq10^{-7}$ |
| New interpolation residual | $R_{\mathrm{new}}\leq\max\{10^{-7},10R_{\mathrm{old}}\}$ |
| Change of sample predictions | $R_{\mathrm{change}}\leq10^{-8}$ |
| Physical sample displacement discrepancy | Componentwise maximum at most $10^{-10}\max\{1,\max_{ij}|((Z-\mathbf1c^T)L^T)_{ij}|\}$ |
| Transformed best sample | Euclidean norm at most $10^{-10}\max\{1,h\}$ |

The inverse residual uses the matrix infinity norm, the largest absolute
row sum. The source-model residual is checked by the controller after
transport preparation. A failed check retains the preceding metric and
all model and interpolation arrays.

The spectral routines also check the relative metric bounds and the
condition-number cap with relative allowance $10^{-8}$, and require
$\det(M_+)>0$ and $|\log\det(M_+)|\leq10^{-7}$. These allowances arise from
the internal default `tol=1e-10`. An identity target is detected by
`numpy.allclose` with `rtol=1e-10`, `atol=1e-12`; a relative logarithmic
change at most $10^{-10}$ is skipped.

The matrix-root, normalization, and cap utilities use a numerical
eigenvalue floor $10^{-14}$ where specified in the source. The geodesic
logarithm requires strictly positive relative eigenvalues. The SPD helper
first symmetrizes its input, tries Cholesky factorization, and adds
$10^{-10}I$ after each failed attempt, for at most eight attempts. If all
fail, it adds a further $10^{-6}I$. These numerical corrections belong to
the stated implementation; the exact metric formulas above describe the
mathematical construction.

## Evaluation accounting and arithmetic

Every physical objective request is recorded, including initialization,
geometry, and nonfinite observations. The internal PDFO extreme barrier
replaces NaN and values larger than $2^{100}$ by $2^{100}$. The raw value
remains in the evaluation history; negative infinity is passed through
the barrier. The result's incumbent is selected among finite observed
values. An objective or user-callback exception propagates through the
core as a `RuntimeError` whose cause retains the original exception.

With `mode='sphere'`, the controller keeps $a=0$, $L=I$ and bypasses all
metric changes. It calls the same scalar core with full interpolation.
The translation preserves scalar accumulation order, integer division,
integer-power multiplication, workspace aliases, and control flow.

The arithmetic backend is selected by `math_backend`:

- `auto` uses the reference primitive on Windows x86-64 and Python's
  platform math library elsewhere.
- `reference` uses a 58-byte local CPU routine for paired x87 `FSINCOS`,
  including its large-argument reduction, through executable memory.
  It requires Windows x86-64.
- `portable` uses Python `math.sin` and `math.cos` on every platform.

The reference target is the pinned Windows x86-64 gfortran PDFO 2.2.0 build
in binary64 and round-to-nearest mode. All six paired trigonometric sites
in `TRSAPP`, `BIGLAG`, and `BIGDEN` use the compatibility primitive. Its
machine bytes and hash are available from the backend metadata. Exact
query-sequence comparisons use this recorded arithmetic environment;
the portable backend records `bitwise_reference_parity=False`.

The retained `src/matro/_newuoa/reference_source`,
`src/matro/_newuoa/source_map.json`,
`src/matro/_newuoa/provenance.json`, and
`src/matro/_newuoa/README.md` identify the scalar
translation. The `release_files` entries in
`kernel_provenance.json` give the hashes of
the installed candidate; the inner provenance manifest records the earlier
translation before namespace and backend integration. The translated kernel retains its
`src/matro/_newuoa/LICENSE.txt`. General API and
release instructions are in [SOLVER.md](../SOLVER.md).
