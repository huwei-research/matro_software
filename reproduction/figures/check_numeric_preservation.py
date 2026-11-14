"""Check data/geometry against v13.4 without writing to the parent revision."""
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
import sys

import fitz
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
REVISION = HERE.parent
PARENT = REVISION.parent / "v13_4"
FIGURES = ["interpolation_coverage", "data_profiles", "performance_profiles",
           "descent_nine", "anisotropy_success", "anisotropy_budget_linear",
           "shape_descent", "four_trajectories"]
SINGLES = ["trajectory_rosenbrock", "trajectory_cubic_valley",
           "trajectory_levy", "trajectory_different_powers"]


def digest(data):
    array = np.asarray(data, dtype="<f8")
    return {"shape": list(array.shape),
            "sha256": hashlib.sha256(array.tobytes()).hexdigest()}


def figure_numbers(fig):
    result = []
    for ax in fig.axes:
        collections = []
        for collection in ax.collections:
            collections.append({
                "offsets": digest(collection.get_offsets()),
                "paths": [digest(path.vertices) for path in collection.get_paths()],
                "array": None if collection.get_array() is None
                         else digest(collection.get_array()),
            })
        result.append({
            "xlim": list(ax.get_xlim()), "ylim": list(ax.get_ylim()),
            "xscale": ax.get_xscale(), "yscale": ax.get_yscale(),
            "lines": [digest(line.get_xydata()) for line in ax.lines],
            "patches": [digest(patch.get_path().vertices) for patch in ax.patches],
            "collections": collections,
            "images": [digest(image.get_array()) for image in ax.images],
        })
    return result


def evaluate(source, name):
    plt.rcdefaults()
    specification = importlib.util.spec_from_file_location(name, source)
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    figures = {}

    def capture(fig, name):
        figures[name] = figure_numbers(fig)
        plt.close(fig)

    module.save = capture
    module.style()
    returns = {}
    for function in ("draw_shape", "draw_trajectories", "draw_profiles",
                     "draw_nine", "draw_conditioning", "draw_coverage"):
        returns[function] = getattr(module, function)()
    return figures, returns


def overview():
    cell_width, row_height = 1050, 1050
    canvas = Image.new("RGB", (2*cell_width, 4*row_height), "#F4F5F6")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(str(HERE / "fonts/lmroman10-regular.otf"), 25)
    for index, name in enumerate(FIGURES):
        image = Image.open(HERE / f"{name}.png").convert("RGB")
        image.thumbnail((cell_width-44, row_height-85), Image.Resampling.LANCZOS)
        left, top = (index % 2)*cell_width, (index // 2)*row_height
        draw.text((left+25, top+18), name.replace("_", " "), fill="#333B44", font=font)
        canvas.paste(image, (left+(cell_width-image.width)//2, top+65))
    canvas.save(HERE / "figure_overview.png")


def main():
    before, before_returns = evaluate(PARENT / "figures/redraw_figures.py", "parent_figures")
    after, after_returns = evaluate(HERE / "redraw_figures.py", "current_figures")
    assert before_returns == after_returns, "Plotted row counts or state indices changed"
    comparisons = {name: before[name] == after[name] for name in FIGURES}
    assert all(comparisons.values()), comparisons
    single_comparisons = {name: before["four_trajectories"][3*i:3*i+3] == after[name]
                          for i, name in enumerate(SINGLES)}
    assert all(single_comparisons.values()), single_comparisons
    input_hashes = {}
    for path in sorted((REVISION / "data/figure_inputs").rglob("*")):
        if path.is_file():
            relative = path.relative_to(REVISION).as_posix()
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            original = hashlib.sha256((PARENT / relative).read_bytes()).hexdigest()
            assert actual == original, relative
            input_hashes[relative] = actual
    exported = {}
    for name in FIGURES:
        with fitz.open(HERE / f"{name}.pdf") as document:
            page = document[0]
            text = page.get_text()
            assert "standard" not in text.lower(), name
            fonts = page.get_fonts(full=True)
            exported[name] = {
                "page_size_inches": [page.rect.width/72, page.rect.height/72],
                "pdf_fonts": [list(font[:6]) for font in fonts],
                "all_fonts_embedded": all(font[1] not in ("n/a", "") for font in fonts),
                "data_geometry_equal": comparisons[name],
                "axes": len(after[name]),
                "line_series": sum(len(ax["lines"]) for ax in after[name]),
                "line_points": sum(line["shape"][0] for ax in after[name] for line in ax["lines"]),
            }
    overview()
    report = {
        "revision": "v13.5", "comparison_revision": "v13.4",
        "optimizer_evaluations": 0, "objective_evaluations": 0,
        "data_files_unchanged": len(input_hashes), "input_sha256": input_hashes,
        "plot_data_geometry_checks": exported,
        "single_trajectory_geometry_equal_to_parent_combined_figure": single_comparisons,
        "comparison_scope": ["all plotted line coordinates", "collection vertices and offsets",
                             "filled polygon vertices", "image field values",
                             "axis limits and scales", "curve counts", "selected state indices"],
        "source_return_values": after_returns,
        "style_base": "figures/style/publication.mplstyle",
        "style_sha256": hashlib.sha256((HERE / "style/publication.mplstyle").read_bytes()).hexdigest(),
        "environment": {"python": platform.python_version(), "numpy": np.__version__,
                        "pandas": pd.__version__, "matplotlib": matplotlib.__version__,
                        "platform": platform.platform()},
    }
    (REVISION / "checks/figure_checks.json").write_text(json.dumps(report, indent=2), encoding="utf8")
    print(json.dumps({"figures": len(exported), "data_files_unchanged": len(input_hashes),
                      "data_geometry_equal": all(comparisons.values()),
                      "line_series": sum(r["line_series"] for r in exported.values()),
                      "line_points": sum(r["line_points"] for r in exported.values())}))


if __name__ == "__main__":
    main()
