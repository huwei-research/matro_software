# Publication style source

`publication.mplstyle` is an unchanged copy of the scientific-visualization
skill asset, copied on 2026-11-13 (Asia/Shanghai) from:

`C:/Users/huwei/.codex/skills/scientific-visualization/assets/publication.mplstyle`

The style is actually loaded by `../redraw_figures.py::style()` before the
paper-specific overrides. The overrides use Latin Modern Roman and Computer
Modern mathematics, 7.5–9.5 pt figure text, muted dark colors, restrained bands
and grids, and the final A4 article text width. The base source hash is recorded
in `../../checks/figure_checks.json`.

The Research Harness contributors' MIT terms are in [LICENSE.md](LICENSE.md).
The upstream K-Dense MIT license is preserved in
[LICENSE_upstream.txt](LICENSE_upstream.txt).

The Latin Modern Roman 10 regular, italic and bold font files are copied without
modification from TeX Live 2024's `fonts/opentype/public/lm` directory. Font
version and authorship are preserved in
[the original font README](../fonts/README-Latin-Modern.TXT), with the
[GUST Font License](../fonts/GUST-FONT-LICENSE.TXT). They are registered locally
at runtime; no operating-system font installation is needed. Mathematical
glyphs use Matplotlib's bundled Computer Modern fonts.
