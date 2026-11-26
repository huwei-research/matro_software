"""Draw the manuscript's first three figures in the specified directory."""
import argparse
from pathlib import Path

import redraw_figures as paper
import matplotlib.pyplot as plt

draw_intro = paper.draw_intro


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    out = parser.parse_args().output
    out.mkdir(parents=True, exist_ok=True)
    paper.style()

    def save_pdf(fig, name):
        fig.savefig(out / f"{name}.pdf")
        plt.close(fig)

    save_pdf(draw_intro(), "interpolation_coverage")
    paper.draw_profiles(save_figure=save_pdf)
