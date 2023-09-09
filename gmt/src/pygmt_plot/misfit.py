import pandas as pd

from .gmt import plot_misfit


def gmt_plot_misfit(mm_file):
    region = [115, 122.5, 27.9, 34.3]
    grid = pd.read_csv(mm_file)[["x", "y", "misfit"]]
    grid.rename(columns={"misfit": "z"}, inplace=True)
    plot_misfit(grid, region, "images/mc_figs/misfit.png")
