from pathlib import Path

import pandas as pd

from .gmt import plot_misfit


def gmt_plot_misfit(misfit: str):
    region = [115, 122.5, 27.9, 34.3]
    # # collect misfit from `Litmod_output.log`
    # misfits = Path(mc_dir).glob("*/Litmod_output.log")
    # data = []
    # for f in misfits:
    #     [lo, la] = f.parent.name.split("_")
    #     with f.open("r") as f:
    #         lines = f.readlines()
    #         misfit = lines[-1].split(" ")[7]
    #     data.append([float(i) for i in [lo, la, misfit]])
    # grid = pd.DataFrame(data, columns=["x", "y", "z"])
    plot_misfit(misfit, region, "images/mc_figs/misfit.png")
