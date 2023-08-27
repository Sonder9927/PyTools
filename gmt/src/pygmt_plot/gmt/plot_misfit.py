import pandas as pd
from pathlib import Path
import pygmt

from .gmt_make_data import topo_hplane, tomo_grid_data
from .gmt_fig import fig_tomo


def plot_misfit(grid, region, fig_name) -> None:
    # make cpt file
    # cpt file
    cptfile = "temp/temp.cpt"
    pygmt.makecpt(
        cmap="hot",
        series=[-0, 2, 0.05],
        continuous=True,
        output=cptfile,
    )
    # make vel grid and get vel grid generated by `surface`
    tomo_grd = "temp/tomo.grd"
    tomo_grid_data(grid, tomo_grd, region)
    # misfit_make(grid, region, cptfile, tomo_grd)

    # topo file
    topo = "ETOPO1.grd"
    topo_data = f"src/txt/{topo}"
    topo_grd = f"temp/topo_{topo}"
    topo_gra = topo_hplane(topo_grd, region, "t", data=topo_data)

    # gmt plot
    gmt_plot_misfit(region, cptfile, tomo_grd, topo_gra, fig_name)


def gmt_plot_misfit(region, cpt, tomo_grd, topo_gra, fname):
    fig = pygmt.Figure()

    # projection
    x = (region[0] + region[1]) / 2
    y = (region[2] + region[3]) / 2
    SCALE = f"m{x}/{y}/0.3i"
    # position of stations
    sta = pd.read_csv(
        "src/txt/station.lst",
        usecols=[1, 2],
        index_col=None,
        header=None,
        delim_whitespace=True,
    )

    # gmt plot
    # define figure configuration
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        # MAP_TITLE_OFFSET="0.25p",
        # MAP_DEGREE_SYMBOL="none",
        # FONT_TITLE="18",
        FONT="16",
    )

    # plot vel fig
    title = Path(fname).stem
    fig = fig_tomo(
        fig, tomo_grd, region, SCALE, title, cpt, topo_gra, sta
    )  # fmt: skip
    # plot colorbar
    fig.colorbar(
        cmap=cpt, position="jBC+w5c/0.4c+o0c/-1.5c+m", frame="xa0.1f0.1"
    )  # fmt: skip

    fig.savefig(fname)
