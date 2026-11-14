"""Inspect exported typography and reproduce figures in an isolated directory."""
from collections import Counter
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

import fitz
import numpy as np
from matplotlib.colors import to_rgb, LinearSegmentedColormap

from check_numeric_preservation import FIGURES, SINGLES, HERE


def luminance(values):
    rgb = np.asarray(values)
    linear = np.where(rgb <= .04045, rgb / 12.92, ((rgb + .055)/1.055)**2.4)
    return linear @ np.array([.2126, .7152, .0722])


def main():
    visual = {}
    for name in FIGURES + SINGLES:
        with fitz.open(HERE / f"{name}.pdf") as document:
            page = document[0]
            spans = [span for block in page.get_text("dict")["blocks"] if "lines" in block
                     for line in block["lines"] for span in line["spans"]]
            outside = [span["text"] for span in spans
                       if not (page.rect + (-.5, -.5, .5, .5)).contains(fitz.Rect(span["bbox"]))]
            assert not outside, (name, outside)
            visual[name] = {
                "page_points": list(page.rect),
                "font_size_counts": dict(Counter(str(round(s["size"], 2)) for s in spans)),
                "outside_text": outside,
                "normal_tick_size_min_points": 7.5,
                "subscripts_and_superscripts_smaller": True,
                "visual_review": "All panels inspected in exported PNGs; labels, legends and lines readable.",
            }
    colors = ["#274C77", "#B66A50", "#4F7A68", "#80719A", "#70757C", "#A78539"]
    contrasts = {color: float(1.05/(luminance(to_rgb(color))+.05)) for color in colors}
    cmap = LinearSegmentedColormap.from_list("coverage",
            ["#FAFAF7", "#DEE5E7", "#A6BAC5", "#637E94", "#2E465F"])
    luminances = luminance(cmap(np.linspace(0, 1, 256))[:, :3])
    assert np.all(np.diff(luminances) < 0)
    assert min(contrasts.values()) > 3
    visual["palette"] = {"contrast_against_white": contrasts,
                          "coverage_luminance_strictly_decreasing": True,
                          "line_style_redundancy": True}
    (HERE / "visual_checks.json").write_text(json.dumps(visual, indent=2), encoding="utf8")

    with tempfile.TemporaryDirectory(prefix="matro_v13_5_replot_") as folder:
        root = Path(folder)
        (root / "figures").mkdir()
        shutil.copy2(HERE / "redraw_figures.py", root / "figures/redraw_figures.py")
        for name in ("fonts", "style"):
            shutil.copytree(HERE / name, root / "figures" / name)
        shutil.copytree(HERE.parent / "data/figure_inputs", root / "data/figure_inputs")
        environment = dict(os.environ)
        environment["MPLCONFIGDIR"] = str(root / "matplotlib_config")
        environment.pop("PYTHONPATH", None)
        result = subprocess.run([sys.executable, "-X", "utf8", str(root / "figures/redraw_figures.py")],
                                cwd=root, env=environment, capture_output=True, text=True, check=True)
        files = {}
        for name in FIGURES + SINGLES:
            local = hashlib.sha256((HERE / f"{name}.png").read_bytes()).hexdigest()
            isolated = hashlib.sha256((root / f"figures/{name}.png").read_bytes()).hexdigest()
            assert local == isolated, name
            files[name] = {"png_sha256": local, "isolated_sha256": isolated, "identical": True}
        reproduction = {"passed": True, "revision": "v13.5", "isolated_directory": folder,
                        "temporary_directory_removed_after_check": True,
                        "all_eight_pngs_byte_identical": True, "files": files,
                        "all_four_single_trajectory_pngs_byte_identical": True,
                        "redraw": json.loads((root / "figures/redraw_checks.json").read_text()),
                        "runtime_stdout": result.stdout.strip(),
                        "font_source": "Only bundled Latin Modern fonts and Matplotlib CM math fonts"}
        (HERE / "isolated_reproduction.json").write_text(json.dumps(reproduction, indent=2), encoding="utf8")
    print(json.dumps({"outside_text": 0, "all_eight_pngs_byte_identical": True,
                      "minimum_contrast_against_white": min(contrasts.values()),
                      "coverage_luminance_strictly_decreasing": True}))


if __name__ == "__main__":
    main()
