import pandas as pd
from pathlib import Path
import pygmt

from .gmt_make_data import make_topos, tomo_grid_data, area_clip
from .gmt_fig import fig_tomos


def gmt_plot_vel(topo, grd, cptinfo, fname, sta=None):
    # gmt plot
    fig = pygmt.Figure()
    # define figure configuration
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        MAP_TITLE_OFFSET="0.25p",
        MAP_DEGREE_SYMBOL="none",
        FONT_TITLE="18",
    )

    tomo = {"grid": grd, "cmap": cptinfo["cmap"]}
    fig = fig_tomos(fig, topo, [tomo], tect=0, clip=True)
    per = Path(fname).stem.split("_")[-1]
    fig.text(
        x=topo["region"][0],
        y=topo["region"][-1],
        fill="white",
        justify="LT",
        font="9p",
        text=f"{per}s",
        offset="j0.1",
    )
    fig.colorbar(
        cmap=cptinfo["cmap"],
        position="jBC+w4.5c/0.3c+o0c/-1c+m",
        frame=cptinfo["frame"],
    )

    fig.savefig(fname)


def plot_vel(grid, region, fig_name, cptconfig={}) -> None:
    # sourcery skip: default-mutable-arg
    # position of stations
    sta = pd.read_csv(
        "src/txt/station.lst",
        usecols=[1, 2],
        names=["x", "y"],
        header=None,
        delim_whitespace=True,
    )
    # make vel grid and get vel grid generated by `surface`
    vel_grd = "temp/vel_tpwt.grd"
    tomo_grid_data(grid, vel_grd, region)

    # cpt file
    cptinfo = {
        "cmap": "temp/temp.cpt",
        "series": _series(grid),
        "frame": "xa",
    }
    cptinfo |= cptconfig
    # make cpt file
    pygmt.makecpt(
        cmap="src/txt/cptfiles/Vc_1.8s.cpt",
        series=cptinfo["series"],
        background=True,
        continuous=True,
        output=cptinfo["cmap"],
    )

    topo = make_topos("ETOPO1", region)

    # gmt plot
    gmt_plot_vel(topo, vel_grd, cptinfo, fig_name, sta)


def plot_as(velf, stdf, region, fn) -> None:
    grd = pd.read_csv(
        velf, delim_whitespace=True, names=["x", "y", "z"], header=None
    )
    grd_clip = area_clip(grd)
    mm = grd_clip["z"].mean()
    grd["z"] = (grd["z"] - mm) / mm * 100
    vel_grd = "temp/temp_vel.grd"
    tomo_grid_data(grd, vel_grd, region)
    std_grd = "temp/temp_std.grd"
    tomo_grid_data(stdf, std_grd, region)
    sta = pd.read_csv(
        "src/txt/station.lst",
        usecols=[1, 2],
        names=["x", "y"],
        header=None,
        delim_whitespace=True,
    )
    # gmt plot
    gmt_plot_as(region, vel_grd, std_grd, fn, sta=sta)


def gmt_plot_as(region, vel, std, fn, sta=None):
    per = Path(fn).stem.split("_")[-1]
    # if int(per) < 120:
    #     return
    topo = make_topos("ETOPO1", region)
    cpt = "temp/temp.cpt"
    fig = pygmt.Figure()
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        MAP_TITLE_OFFSET="0.25p",
        MAP_DEGREE_SYMBOL="none",
        FONT_TITLE="18",
    )
    with fig.subplot(
        nrows=1, ncols=2, figsize=("15c", "8c"), autolabel=True, margins="0.5c"
    ):
        kws = {"tect": 0, "sta": None, "projection": "M?"}
        with fig.set_panel(panel=0):
            pygmt.makecpt(
                cmap="src/txt/cptfiles/Vc_1.8s.cpt",
                series=[-2, 2],
                output=cpt,
            )
            tomos = [{"grid": vel, "cmap": cpt}]
            fig = fig_tomos(fig, topo, tomos, clip=True, **kws)
            fig.text(
                x=region[0],
                y=region[-1],
                fill="white",
                justify="LT",
                font="15p",
                text=f"{per}s",
                offset="j0.1",
            )
            fig.colorbar(
                frame=["a1f1", 'x+l"TPWT Phase velocity anomaly"', "y+l%"]
            )
        with fig.set_panel(panel=1):
            pygmt.makecpt(
                cmap="hot", series=[0, 121], reverse=True, output=cpt
            )
            tomos = [{"grid": std, "cmap": cpt}]
            fig = fig_tomos(fig, topo, tomos, **kws)
            fig.colorbar(
                frame=["a20f20", 'x+l"TPWT standard deviation"', "y+lm/s"]
            )
    fig.savefig(fn)


def _series(grid):
    # from src.info_filter import vel_info_per, points_boundary

    # boundary = points_boundary(sta[["x", "y"]])
    # info = vel_info_per(grid, boundary)
    # avg = info["vel_avg"]
    # dev = min([avg - info["vel_min"], info["vel_max"] - avg])
    if type(grid) is str or Path:
        grid = pd.read_csv(
            grid, delim_whitespace=True, names=["x", "y", "z"], header=None
        )
    grid = area_clip(grid)
    avg = grid["z"].mean()
    dev = min([avg - grid["z"].min(), grid["z"].max() - avg])
    return [avg - dev + 0.02, avg + dev - 0.02, 0.01]
