# Benchmark statistics and reference-value analysis

The main manuscript contains the solver comparison on 147 instances and its
mechanism experiments. This document gives the detailed benchmark distribution,
objective-level aggregation, and reference-value calculations used to check those
results. It is a reproducibility document; no separate supplementary PDF is needed.

## Benchmark distribution

The 147 instances span 136 distinct objective functions: 125 functions have one
configuration and eleven have two. Each instance has twenty starts. The data
therefore contain 2940 instance–start pairs and 17640 runs of six methods.

| Dimension | Moré–Wild | CUTEst/S2MPJ |
|---:|---:|---:|
| 2 | 5 | 41 |
| 3 | 5 | 17 |
| 4 | 5 | 10 |
| 5 | 3 | 1 |
| 6 | 4 | 13 |
| 7 | 5 | 2 |
| 8 | 6 | 12 |
| 9 | 1 | 1 |
| 10 | 4 | 2 |
| 11 | 1 | 0 |
| 12 | 2 | 7 |
| **Total** | **41** | **106** |

The instance identifiers and objective identities are in
`configuration_mapping.csv.gz`; coordinate maps and initial radii are in
`../data/initialization.csv.gz`, and all starts are in `../data/starts.csv.gz`.

## Equal weight for each objective

Let $\mathcal P_j$ contain the twenty or forty instance–start pairs belonging to
objective $j$. For method $s$, let $t_{p,s}(\tau)$ be its first-hit count at relative
accuracy $\tau$, with $t_{p,s}=\infty$ for an unreached target. Each budget is
$N_{\max,p}=500(n_p+1)$. Define

$$
S_{j,s}(\tau)=\frac{1}{|\mathcal P_j|}\sum_{p\in\mathcal P_j}
\mathbf 1\{t_{p,s}(\tau)<\infty\},
\qquad
Q_{j,s}(\tau)=\frac{1}{|\mathcal P_j|}\sum_{p\in\mathcal P_j}
\frac{\min\{t_{p,s}(\tau),N_{\max,p}\}}{N_{\max,p}}.
$$

We average $S_{j,s}$ and $Q_{j,s}$ equally over the 136 objectives. The displayed
success percentage is $100\overline S_s$ and the mean normalized capped count is
$500\overline Q_s$. In contrast, the main Table 1 averages all 2940 instance–start
pairs equally. Failed runs contribute their full budget under both aggregations.

## Main reference values

The main reference is the minimum of the declared values and all finite benchmark observations for an objective, shared across methods and starts.

### Success rate (%)

| Method | $10^{-3}$ | $10^{-5}$ | $10^{-7}$ | $10^{-9}$ |
|---|---:|---:|---:|---:|
| MATRO | 96.67 | 95.90 | 94.43 | 90.72 |
| NEWUOA (full) | 96.56 | 95.64 | 86.08 | 78.84 |
| NEWUOA (2n+1) | 97.02 | 93.12 | 83.16 | 76.91 |
| COBYQA | 96.76 | 93.75 | 87.65 | 78.82 |
| Nelder–Mead | 95.64 | 93.51 | 87.11 | 80.18 |
| CMA-ES | 91.32 | 88.68 | 83.09 | 78.31 |

### Mean normalized capped evaluations

| Method | $10^{-3}$ | $10^{-5}$ | $10^{-7}$ | $10^{-9}$ |
|---|---:|---:|---:|---:|
| MATRO | 29.7 | 41.6 | 60.4 | 80.8 |
| NEWUOA (full) | 33.6 | 55.0 | 111.0 | 143.1 |
| NEWUOA (2n+1) | 35.6 | 82.7 | 129.6 | 157.2 |
| COBYQA | 37.5 | 75.5 | 120.4 | 153.6 |
| Nelder–Mead | 50.7 | 88.9 | 133.6 | 166.5 |
| CMA-ES | 89.1 | 145.2 | 198.2 | 239.6 |

## Declared reference values

This calculation uses the declared reference alone, with the same runs, budgets and objective weights. The two references coincide for 91 objectives; 45 have lower pooled values. All initial gaps are positive under both definitions.

### Success rate (%)

| Method | $10^{-3}$ | $10^{-5}$ | $10^{-7}$ | $10^{-9}$ |
|---|---:|---:|---:|---:|
| MATRO | 97.41 | 96.64 | 95.24 | 91.60 |
| NEWUOA (full) | 97.30 | 96.38 | 86.93 | 79.80 |
| NEWUOA (2n+1) | 97.65 | 93.75 | 83.82 | 77.54 |
| COBYQA | 97.39 | 94.38 | 88.27 | 79.49 |
| Nelder–Mead | 96.23 | 94.14 | 88.07 | 81.32 |
| CMA-ES | 91.84 | 89.19 | 83.82 | 79.45 |

### Mean normalized capped evaluations

| Method | $10^{-3}$ | $10^{-5}$ | $10^{-7}$ | $10^{-9}$ |
|---|---:|---:|---:|---:|
| MATRO | 26.0 | 38.0 | 56.5 | 76.5 |
| NEWUOA (full) | 30.0 | 51.4 | 107.3 | 139.3 |
| NEWUOA (2n+1) | 32.6 | 79.6 | 126.3 | 154.2 |
| COBYQA | 34.5 | 72.4 | 117.4 | 150.5 |
| Nelder–Mead | 47.8 | 85.8 | 129.7 | 161.6 |
| CMA-ES | 86.6 | 142.6 | 194.9 | 235.3 |

## Comparison of reference definitions

The six methods have the same ordering by mean normalized capped count under
both reference definitions at every target accuracy. At $\tau=10^{-7}$, MATRO
has a smaller mean normalized capped count than full NEWUOA on 106 objectives,
an equal count on 3 and a larger count on 27 using the main references; the
corresponding numbers are 107, 2 and 27 using the declared references. Equality
uses an absolute tolerance of $10^{-12}$ on the mean budget fractions $Q_{j,s}$.

## Reproduction

From the project directory:

```powershell
python -X utf8 paper/revisions/v14_1/statistics/analyze_statistics.py
```

The program reads the compact inputs in this directory and `../data/` and checks
147 configurations, 136 identities, 17640 runs and 70560 run–target records. It
produces the tables and `objective_summary.csv`, `objective_level_results.csv.gz`,
`matro_full_objective_wtl.csv`, and reference-sensitivity outputs. All values above
come from these files. No objective evaluation or optimizer run is required.
