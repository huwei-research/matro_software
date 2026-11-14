# Compact experimental evidence and figure inputs for MATRO v14.1

Version 14.1 preserves the benchmark data, figure inputs, and transport records.
The eight figures use a common palette, typography, and method labels. The
statistical documentation gives the instance distribution and objective-level statistics.
The commands below apply to this revision.
The retained `transport_diagnostics_v13_1.json/.csv` contain per-run counts from
all 2940 MATRO metric-event logs. From this directory, independently check them
with `python ../reviews/analyze_transport_diagnostics.py --verify-only`.
The collection-provenance check, equal-objective statistics, reference
sensitivity, and full-precision reference inputs are in `../statistics/`.
Its README specifies independent reanalysis and archived-query provenance.
The ranking formula retained in `selection_rules.json` is a historical
analysis record: all 147 eligible configurations were retained, so ranking
did not truncate the membership of the final collection.

## Inherited data record

Version 12.7 refines the manuscript narrative and relocates implementation
and reproduction details to accompanying Markdown documents. All benchmark
records, figure inputs, reconstruction files, and verification results are
retained from version 12.6. No numerical experiment or objective reconstruction
was rerun for this revision. The source archive also supplies the implementation
and experimental notes under `../documentation/docs/`.

This directory contains the fixed 147-instance experiment inputs and summary data
used in the paper. It is independent of the raw optimization archives for the
checks performed by `verify_data.py`.

- `selected147_instances.csv.gz`: all 147 selected instances, dimensions,
  numerical-screening fields, per-method target statistics, and selection scores.
- `initialization.csv.gz`: one row per instance; selected physical center,
  coordinate matrix, initial radius, perturbation scale, and calibration source.
- `starts.csv.gz`: all 2940 physical starts, solver starts, radii, budgets, seeds,
  and finite-definition backtracking counts. No starting point is omitted.
  Version 12.1 also supplies `algorithm_seed`, reproduced from the frozen
  protocol: SHA256 of `cma|20261030|instance_id|start_id`, first four bytes
  interpreted as an unsigned little-endian integer, modulo `2**31-2`, plus one.
- `runs.csv.gz`: all 17640 runs at four exact target levels (70560 rows),
  including failures and exact first-hit counts. Profile figures use these
  counts; downsampled descent curves are not used to estimate first hits.
- `references.csv.gz`: the 136 objective identities represented by the 147
  instances, with declared, observed, and unified reference values.
- `selection_rules.json`: original selection thresholds and ranking formula.
- `benchmark_environment.json`: the recorded benchmark Python and dependencies.
- `mechanism_inputs.json`, `conditioning_summary.csv`, `shape_summary.csv`,
  `coverage_metrics.json`: inputs and summary quantities for the mechanism figures.
- `trajectory_cases.json`, `trajectory_neighbors.csv`: the four displayed
  configurations and all neighboring-start summary groups.
- `nine_example_metrics.csv`: exact target counts for the nine displayed examples.
- `source_manifest.json`: original paths, source hashes, destination hashes,
  frozen execution/configuration hashes, and storage/verification budgets.

The statistical verification and figure-redrawing scripts perform no objective queries.
The complete raw query journals, all candidate configurations, full model states,
and plotting data remain in the Research/matro archives identified by the manifest.
The original figure packages are preserved under
`notes/figures_selected147_20261109`, `notes/paper_figures_20261109`,
`notes/mechanism_figures_refined_20261109`, and `notes/trajectory_search_20261109`.
Version 12.1 includes independent regeneration of all eight main figures:
`figure_inputs/` holds the frozen compact profile arrays, nine-example curves,
conditioning summaries, shape curves, coverage field, and four trajectory/state
records and background grids. `../figures/redraw_figures.py` reads only these
local inputs. It does not import the solvers, evaluate an objective, or read the
Research directory. Mathematical selections, domains, curves, target counts,
and axes ranges are unchanged. The inherited vector figures were produced
at 5.125 inches, with normal ticks at 7 points or larger. Version 12.6 places
these same assets at the wider A4 article text width, preserving their aspect
ratios and enlarging their labels proportionally. The redraw script retains
the original export dimensions for reproducibility.

The statistical data occupy approximately 0.93 MB and the added plotting inputs
5,376,817 bytes. The total data budget is 8 MB, the single-file budget is 2 MB,
the statistics-checking memory budget is 256 MiB, and the drawing memory budget
is 768 MiB. The existing largest plot-input file is 1,182,573 bytes, which sets
the 2 MB single-file allowance. Actual byte counts and measured memory are
recorded in the audit, `verification.json`, and the figure checks. CSV files can be read
row-by-row using Python's standard library; no large JSON experiment archive is
loaded by the verification script.

Run from this directory:

```text
python verify_data.py
```

The script checks all counts, paired inputs, budget/target bookkeeping, the
paper's four-precision success table, the extreme-anisotropy counts, and compact
file hashes. It can be run after copying only this directory to another machine.

To regenerate all main figures from the revision directory:

```text
python -m pip install -r data/requirements_figures.txt
python figures/redraw_figures.py
```

Copy both `data/` and `figures/redraw_figures.py`, preserving these relative
paths. The script writes PDF, SVG, and PNG files next to itself. The numerical
statistics were verified in an isolated directory. All eight PNGs were also
redrawn there and were byte-identical in the recorded environment. The peak
working sets were about 48 MB for statistics verification and 312,606,720 bytes
for figure generation. `../figures/isolated_reproduction.json` records this
independent check; `../figures/visual_checks.json` records PDF page dimensions,
font sizes, and the absence of text outside the pages. The eight PNGs were
visually inspected after export.

## Fixed-state reduction-error reconstruction

`fixed_state_input.json`, `fixed_state_reconstruction.py`, and
`fixed_state_reconstruction.json` retain the independently checked six-point
Rosenbrock state, its reconstruction procedure, and the original result.
They were first saved during the November 10 independent manuscript review;
the result includes the input and script SHA-256 digests, environment, original
source path, and the full numerical decomposition.

The input is 852 bytes; the three files together are about 13 KB. The
reconstruction solves one six-by-six interpolation system and two
two-dimensional quadratic trust-region subproblems. It uses no optimization
journal and starts no optimization trajectory. Run from this directory:

```text
python fixed_state_reconstruction.py --output fixed_state_recheck.json
```

The script performs nine offline objective evaluations: six sample checks,
one center evaluation, and two candidate evaluations. It checks the
subproblem optimality conditions and the exact reduction-error identity.
The displayed model and its metric are preserved; no solver receives these
offline evaluations. NumPy and SciPy are required. Use a distinct output
name to preserve the archived reconstruction record.
