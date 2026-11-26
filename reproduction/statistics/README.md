# Benchmark statistics

Run `python -X utf8 analyze_statistics.py` from this directory. The program
uses the Python 3.10+ standard library and the published records in this
directory and `../data/`. It ran with a peak working set of about 61 MB on
Windows with Python 3.13.5. All statistical inputs and outputs together
occupy less than 0.5 MB in this directory.

`table_paired_summary.tex` contains the success rates and mean normalized
capped counts in Table 1, grouped by target. Each of the 2940 instance–start
pairs has equal weight. Unsuccessful runs receive the full budget
`500(n+1)`. The statistics describe the benchmark configurations used in
method development.

| Files | Contents |
|---|---|
| `configuration_mapping.csv.gz`, `instance_distribution.csv` | Instance-to-objective mapping and counts by collection and dimension. |
| `canonical_run_values.csv.gz`, `reference_hit_checks.csv.gz` | Full-precision initial and reference values, plus first-hit counts under both reference definitions for distinct thresholds. |
| `objective_level_results.csv.gz`, `objective_summary.csv` | Results by objective and summaries with equal weight per objective. |
| `matro_full_objective_wtl.csv` | Objective-level comparisons of MATRO and full NEWUOA. |
| `reference_sensitivity.csv`, `reference_changes_by_identity.csv.gz` | Changes in first hits, successes and capped counts when the declared reference is used alone. |
| `statistics_receipt.json` | Record counts, input hashes and aggregation conventions. |

[Analysis](analysis.md) gives the formulas, reference definitions and numerical
results. The five generated TeX tables are written alongside the CSV outputs.
