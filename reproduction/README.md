# Computational materials

These materials reproduce Tables 1 and 2 and the eight figure PDFs in v15.6 of
*Metric-Aware Trust Regions for Derivative-Free Optimization with Full
Quadratic Interpolation*, by Wei Hu, Pengcheng Xie, Ya-Xiang Yuan and Li Zhang.

The development benchmark contains 147 configurations and 20 starts per
configuration. Solver performance informed the initial configurations during
development. The comparisons in the paper describe these 2940 tasks.
The archive includes the final inputs, the four target records for each of
17640 runs, the data for the fixed-model example, and the plotting inputs.

## Reproduce the tables and figures

Use Python 3.13 for the tested environment. From this directory run

```sh
python -m pip install -r data/requirements_figures.txt scipy==1.16.1
python -X utf8 data/verify_data.py
python -X utf8 statistics/analyze_statistics.py
python -X utf8 data/fixed_state_reconstruction.py --output fixed_state_recheck.json
python -X utf8 figures/redraw_figures.py
```

- Table 1 uses the success rates and mean normalized capped counts in
  `statistics/table_paired_summary.tex`. The statistical analysis reads saved
  target hits and evaluation budgets.
- Table 2 uses the results for the disk and the ellipse in
  `fixed_state_recheck.json`. Divide the ellipse value by the disk value
  before rounding to obtain the last column.
- Figures 1–8 are written to `figures/`. The data and the fonts used to draw
  them are included.

See [data](data/README.md) for the files, [statistics](statistics/README.md)
for the calculations, and [the experimental protocol](../docs/experiments.md)
for the settings and interpretation. The [manifest](source_manifest.json)
lists the files in this reproduction package with their sizes and SHA-256 hashes.
