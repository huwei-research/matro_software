# Computational materials

These materials accompany *Metric-Aware Trust-Region Optimization with Full
Quadratic Interpolation*, by Wei Hu, Pengcheng Xie, Ya-Xiang Yuan and Li Zhang,
manuscript v14.1.

The collection contains the configurations, compact numerical data and analysis
programs underlying the reported results. It contains 147 benchmark instances,
2940 instance-start pairs, and target records for 17640 runs at four accuracies.
The saved inputs also support the eight manuscript figures and the mechanism
comparisons. Full statistical definitions and tables are in
`statistics/analysis.md`.

## Contents and reproduction

- `data/`: initialization, starts, budgets, seeds, target counts, references,
  mechanism quantities and compact plotting inputs.
- `statistics/`: statistical definitions, tables and their generation program.
- `figures/`: the manuscript figures, plotting script, style and fonts.
- `documentation/`: implementation and experiment descriptions.

- `source_manifest.json`: source archive and SHA-256 digests of supplied files.

After extraction, run from the directory containing this README:

```text
python -X utf8 data/verify_data.py
python -X utf8 statistics/analyze_statistics.py
python -X utf8 figures/redraw_figures.py
```

Statistical analysis uses Python 3.10 or later and its standard library.
Plotting additionally uses NumPy, pandas and Matplotlib; the recorded experiment
environment is in `data/benchmark_environment.json`. Font files are supplied.
The verification and plotting programs read the included data without objective
evaluations. Numerical-data storage and analysis-memory measurements are
documented in `data/README.md` and `statistics/README.md`.

The full optimizer implementations, test-function sources and complete raw
evaluation journals are maintained separately in the research repository.
This archive supports reanalysis and figure reproduction from the saved results.

Publication input check: 6,877,715 bytes of numerical input; largest input 1,182,573 bytes. Peak measured Python allocation for per-file reading was 1,295,317 bytes (CSV streamed; NPZ byte-stream check; imported libraries and rendering excluded). Budgets: 20 MiB total, 8 MiB per file, 128 MiB reading allocation.
