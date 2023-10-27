# Author: Sonder Merak
# Version: 0.1.2
# Description: plot diff between tpwt and ant results.

from .gmt_make_data import make_topos, diff_make
from .gmt_fig import fig_tomos

import pandas as pd
from pathlib import Path
import pygmt


def gmt_plot_diff(grds, region, cpt, fname):
    sta = pd.read_csv(
        "src/txt/station.lst",
        usecols=[1, 2],
        names=["x", "y"],
        header=None,
        delim_whitespace=True,
    )
    topo = make_topos("ETOPO1", region)
    # gmt plot
    fig = pygmt.Figure()
    # define figure configuration
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        MAP_TITLE_OFFSET="0.25p",
        MAP_DEGREE_SYMBOL="none",
        FONT_TITLE="18",
    )

    with fig.subplot(
        nrows=2,
        ncols=2,
        figsize=("15c", "15.5c"),
        autolabel=True,
        margins="0.5c",
    ):
        region = topo["region"]
        kws = {"tect": 0, "sta": sta, "projection": "M?", "clip": True}
        # ant
        with fig.set_panel(panel=0):
            # tomos = [{"grid": sta_clip(grds["ant"], region), "cmap": cpt}]
            tomo = {"grid": grds["ant"], "cmap": cpt}
            fig = fig_tomos(fig, topo, [tomo], **kws)
        # tpwt
        with fig.set_panel(panel=1):
            # tomos = [{"grid": sta_clip(grds["tpwt"], region), "cmap": cpt}]
            tomo["grid"] = grds["tpwt"]
            fig = fig_tomos(fig, topo, [tomo], **kws)
        # diff
        with fig.set_panel(panel=2):
            cdf = "src/txt/cptfiles/vs_dif.cpt"
            tomo = {"grid": grds["diff"], "cmap": cdf}
            kws["sta"] = None
            fig = fig_tomos(fig, topo, [tomo], **kws)
            fig.colorbar(
                cmap=cdf,
                position="jBC+w7c/0.4c+o0c/-1.5c+m",
                frame="xa30f30",
            )
        # statistics
        with fig.set_panel(panel=3):
            per = Path(grds["tpwt"]).stem.split("_")[-1]
            # use "X?" as projection
    # vel colorbar
    fig.shift_origin(yshift="9c")
    fig.colorbar(cmap=cpt, position="jBC+w8c/0.4c+o0c/-1.5c+m", frame="xa")
    fig.savefig(fname)


def plot_diff(grid_tpwt, grid_ant, region, fig_name):
    # cpt file
    cpt = "temp/tomo.cpt"
    # grd file
    grds = {
        "ant": "temp/vel_ant.grd",
        "tpwt": "temp/vel_tpwt.grd",
        "diff": "temp/vel_diff.grd",
    }

    diff_make(grid_ant, grid_tpwt, region, cpt, grds)
    # topo_gradient(topo_gra, region, "t", data=topo_data)

    gmt_plot_diff(grds, region, cpt, fig_name)
