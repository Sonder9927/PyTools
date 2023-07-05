import pandas as pd
from pathlib import Path
import pygmt

from .gmt_make_data import make_topo, vel_make
from .gmt_fig import fig_vel


def gmt_plot_vel(region, cpts, topo_grd, vel_grd, topo_gra, fname):
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
        MAP_TITLE_OFFSET="0.25p",
        MAP_DEGREE_SYMBOL="none",
        FONT_TITLE="18",
    )

    # plot vel fig
    title = Path(fname).stem
    fig = fig_vel(
        fig, topo_grd, vel_grd, region, SCALE, title, cpts, topo_gra, sta
    )  # fmt: skip
    # plot colorbar
    fig.colorbar(
        cmap=cpts[1], position="jBC+w5c/0.4c+o0c/-1.5c+m", frame="xa0.1f0.1"
    )  # fmt: skip

    fig.savefig(fname)


def plot_vel(grid, region, fig_name, series=None) -> None:
    # cpt file
    cptfile1 = "temp/g.cpt"
    cptfile2 = "temp/vel.cpt"
    cptfiles = [cptfile1, cptfile2]
    # grd file
    vel_grd = "temp/vel_tpwt.grd"

    vel_make(grid, region, cptfiles, vel_grd, series)

    # topo file
    topo_grd = "temp/topo.grd"
    TOPO_GRA = "temp/topo.gradient"
    if not Path(topo_grd).exists():
        TOPO = pygmt.datasets.load_earth_relief(
            resolution="01m", region=region, registration="gridline"
        )
        make_topo(TOPO, region, TOPO_GRA, "e0.5", topo_grd=topo_grd)

    # gmt plot
    gmt_plot_vel(region, cptfiles, topo_grd, vel_grd, TOPO_GRA, fig_name)
