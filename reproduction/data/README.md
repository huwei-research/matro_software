# Numerical inputs

The benchmark comprises 147 configurations of 136 objectives, with 20 starts
per configuration. Six methods use the same starts, coordinate maps and
evaluation budgets. The following files describe the comparisons reported in
the manuscript.

| File | Contents |
|---|---|
| `instances.csv.gz` | Instance identifier, source collection, function name, dimension and objective identity. |
| `initialization.csv.gz` | Physical center, coordinate matrix, initial radius, perturbation scale, reference and coordinate condition for each instance. |
| `starts.csv.gz` | Physical and solver coordinates, scalar radius, evaluation budget and seeds for each of the 2940 instance–start pairs. |
| `runs.csv.gz` | One record per run and accuracy, with the initial value, empirical reference, number of calls, first-hit count and success indicator. The 17640 runs give 70560 records at four accuracies. |
| `references.csv.gz` | Declared and observed reference values by objective identity. |
| `benchmark_environment.json` | Software versions, operating system and numerical backend for the benchmark. |

The main reference is shared by all methods and starts for a given objective.
Its definition and the corresponding reference-sensitivity calculation are
described in [the statistical analysis](../statistics/analysis.md).

## Fixed model and figures

`fixed_state_input.json` contains the center, radius, metric, six physical
sample points and their function values for the Rosenbrock example in Table 2.
From this directory, run `python -X utf8 fixed_state_reconstruction.py` with
NumPy and SciPy installed. The program fits the quadratic, solves the two
trust-region subproblems and evaluates the known objective at the sample
points, center and two trial points. It writes `fixed_state_recheck.json`.
The manuscript figure uses the stored reconstruction in
`fixed_state_reconstruction.json`.

`figure_inputs/` holds the plot grids, four profile datasets, descent curves,
conditioning summaries and trajectory records. Its manifest lists paths,
sizes and SHA-256 digests relative to `reproduction/`. The data used for the
four displayed trajectories include the recorded centers, regions and
function values. Additional numerical summaries for the mechanism experiments
and the metric-transport diagnostics accompany these plot inputs.

## Verification

Run `python -X utf8 verify_data.py` in this directory. It checks the benchmark
dimensions, matched starts and budgets, success counts, diagnostic summaries
and the data files listed in `input_hashes.json`. The compressed CSV inputs
can be read row by row with Python's standard library. The compact plot
inputs occupy about 5.4 MB, and the largest input file is 1.2 MB. Both figures
use decimal units. See [the reproduction instructions](../README.md) for
the manuscript tables and figure PDFs.
