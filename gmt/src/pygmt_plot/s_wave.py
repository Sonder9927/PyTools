import numpy as np
from src.info_filter import GridVsv

from .gmt import plot_vs_vplane


def gmt_plot_vs(grid: str):
    vs = GridVsv("src/txt/vs.csv")
    r = vs.region
    # plot lon=val
    for x in np.arange(int(r[0]) + 1, r[1]):
        grid, fn = vs.grid("x", x)
        plot_vs_vplane(grid, [r[2], r[3]], fn)
    # plot lat=val
    for y in np.arange(int(r[2]), r[3]):
        grid, fn = vs.grid("y", y)
        plot_vs_vplane(grid, [r[0], r[1]], fn)
    # plot deep=val
    # for z in ...
