# Author: Sonder Merak
# Version: 0.1.0
# Description: plot diff between 2 grid files.

from .gmt_make_data import make_topo, make_grd, diff_inner

# from icecream import ic
import pandas as pd
import pygmt


def fig_sta(fig, sta):
    # station
    fig.plot(
        data = sta,
        style = "t0.1c",
        fill = "blue",
        pen = "black",
    )
    # fig.plot(data="ncc_lv.xy", pen="0.8p,black")
    fig.plot(data="src/txt/China_tectonic.dat", pen="thick,black,-")

    return fig


def fig_tomo(fig, grid, region, scale, title, cpt, topo_gra, sta):
    """
    plot single fig of tpwt or ant
    """
    fig.basemap(
            projection = scale,
            region = region,
            frame = [f'WSne+t"{title}"', "xa2f2", "ya2f2"]
        )

    fig.coast(shorelines="", resolution="l", land="white", area_thresh=10_000)
    # grdimage
    # ==================================================================
    fig.grdimage(
        grid = grid,
        cmap = cpt,
        shading = topo_gra,
    )

    fig = fig_sta(fig, sta)

    return fig


def fig_diff(fig, diff, region, scale, cpt, topo_gra, sta):
    fig.coast(
        region = region,
        projection = scale,
        frame = ["WSne", "xa2f2", "ya2f2"],
        shorelines = "",
        resolution = "l",
        land = "white",
        area_thresh = 10_000
    )

    # cut vel_diff_grd by the boundary of stations
    diff = diff_inner(diff, region, sta)
    fig.grdimage(grid=diff, cmap=cpt, shading=topo_gra)

    fig = fig_sta(fig, sta)

    # colorbar
    fig.colorbar(cmap=cpt, position="jBC+w8c/0.4c+o0c/-1.5c+m", frame="xa30f30")

    return fig


def gmt_plot_diff(region, cpt, tpwt_grd, ant_grd, diff_grd, topo_gra, fname):
    fig = pygmt.Figure()

    # projection
    x = (region[0] + region[1]) / 2
    y = (region[2] + region[3]) / 2
    SCALE = f"m{x}/{y}/0.3i"
    # position of stations 
    sta = pd.read_csv("src/txt/station.lst",
        usecols=[1, 2], index_col=None, header=None, delim_whitespace=True)

    # calculate boundary points for grdimage
    # gmt plot
    # define figure configuration
    pygmt.config(MAP_FRAME_TYPE="plain", MAP_TITLE_OFFSET="0.25p",
        MAP_DEGREE_SYMBOL="none", FONT_TITLE="18")

    # plot tpwt fig
    fig = fig_tomo(fig, tpwt_grd, region, SCALE, "tpwt", cpt, topo_gra, sta)
    # shift plot origin of the second fig by 12 cm in x direction
    fig.shift_origin(xshift="10c")
    # plot ant fig
    fig = fig_tomo(fig, ant_grd, region, SCALE, "ant", cpt, topo_gra, sta)
    # plot colorbar
    fig.colorbar(cmap=cpt, position="jBC+w5c/0.4c+o0c/-1.5c+m", frame="xa0.2f0.2")

    # plot diff
    fig.shift_origin(xshift="-10c", yshift="-8c")
    cpt_diff = "src/txt/vs_dif.cpt"
    fig = fig_diff(fig, diff_grd, region, SCALE, cpt_diff, topo_gra, sta)
    # plot average vel info

    fig.savefig(fname)


def plot_diff(grid_tpwt, grid_ant, region, fig_name):

    # cpt file
    cptfile = "temp/test.cpt"
    # grd file
    ant_grd = "temp/vel_ant.grd"
    tpwt_grd = "temp/vel_tpwt.grd"
    # diff grid which can be used to calculate standard deviation
    diff_grd = "temp/vel_diff.grd"

    make_grd(grid_ant, grid_tpwt, region, cptfile, ant_grd, tpwt_grd, diff_grd)
    # topo file
    TOPO = "src/txt/ETOPO1.grd"
    TOPO_GRA = "temp/topo.gradient"
    make_topo(TOPO, region, TOPO_GRA)

    gmt_plot_diff(region, cptfile, tpwt_grd, ant_grd, diff_grd, TOPO_GRA, fig_name)

