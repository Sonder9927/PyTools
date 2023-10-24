# Author: Sonder Merak
# Version: 0.1.2
# Description: plot diff between tpwt and ant results.

from .gmt_make_data import make_topos, diff_make
from .gmt_fig import fig_htomo, fig_diff

import pandas as pd
from pathlib import Path
import pygmt


def gmt_plot_diff(region, cpt, tpwt_grd, ant_grd, diff_grd, topo_gra, fname):
    fig = pygmt.Figure()

    # gmt plot
    # define figure configuration
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        MAP_TITLE_OFFSET="0.25p",
        MAP_DEGREE_SYMBOL="none",
        FONT_TITLE="18",
    )

    sta = pd.read_csv(
        "src/txt/station.lst",
        usecols=[1, 2],
        index_col=None,
        header=None,
        delim_whitespace=True,
    )
    # plot tpwt fig
    fig = fig_htomo(fig, tpwt_grd, region, "tpwt", cpt, topo_gra, sta)
    # shift plot origin of the second fig by 12 cm in x direction
    fig.shift_origin(xshift="6c")
    # plot ant fig
    fig = fig_htomo(fig, ant_grd, region, "ant", cpt, topo_gra, sta)
    # plot colorbar
    fig.colorbar(
        cmap=cpt, position="jBC+w5c/0.4c+o0c/-1.5c+m", frame="xa0.2f0.2"
    )

    # plot diff
    fig.shift_origin(xshift="-6c", yshift="-7c")
    cpt_diff = "src/txt/cptfiles/vs_dif.cpt"
    diff_title = Path(fname).stem
    fig = fig_diff(fig, diff_grd, region, diff_title, cpt_diff, topo_gra, sta)

    fig.savefig(fname)


def plot_diff(grid_tpwt, grid_ant, region, fig_name):
    # cpt file
    cptfile = "temp/diff_temp.cpt"
    # grd file
    ant_grd = "temp/vel_ant.grd"
    tpwt_grd = "temp/vel_tpwt.grd"
    # diff grid which can be used to calculate standard deviation
    diff_grd = "temp/vel_diff.grd"

    diff_make(
        grid_ant, grid_tpwt, region, cptfile, ant_grd, tpwt_grd, diff_grd
    )
    # topo file
    topos = make_topos("ETOPO1", region)
    # topo_gradient(topo_gra, region, "t", data=topo_data)

    gmt_plot_diff(
        region, cptfile, tpwt_grd, ant_grd, diff_grd, topos["gra"], fig_name
    )
