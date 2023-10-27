from pathlib import Path

import numpy as np
import pandas as pd
import pygmt

from .gmt_fig import fig_tomos
from .gmt_make_data import tomo_grid_data, make_topos


def plot_area_map(regions, fig_name):
    cpt = "temp/temp.cpt"
    pygmt.makecpt(cmap="globe", series=[-6000, 3000], output=cpt)
    grd = pygmt.datasets.load_earth_relief(resolution="01m", region=regions[0])
    vicinity = {
        "topo": {"region": regions[0]},
        "tomos": [{"grid": grd, "cmap": cpt}],
    }
    area = make_topos("ETOPO1", regions[1])
    sta = pd.read_csv(
        "src/txt/station.lst",
        usecols=[1, 2],
        index_col=None,
        header=None,
        delim_whitespace=True,
    )
    _gmt_fig_area(vicinity, area, fig_name, sta)


def _gmt_fig_area(vici, area, fn, sta=None):
    # lines = [ll for _, ll in lines_generator(area["region"])]
    fig = pygmt.Figure()
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        MAP_TITLE_OFFSET="0.25p",
        MAP_DEGREE_SYMBOL="none",
        FONT_TITLE="18",
        FONT="10",
    )
    with fig.subplot(
        nrows=1, ncols=2, figsize=("15c", "8c"), autolabel=True, margins="0.5c"
    ):
        kwgs = {"projection": "M?", "tect": 0, "sta": sta}
        with fig.set_panel(panel=0):
            fig = fig_tomos(fig, **vici, **kwgs)
            # fig.grdimage(
            #     grid=vici["grd"],
            #     projection="M?",
            #     region=vici["region"],
            #     frame="a",
            # )
            # fig = fig_tect_and_sta(fig, 0, sta)
            fig.text(
                textfiles="src/txt/tects/viciTectName.txt",
                angle=True,
                font=True,
                justify=True,
            )
            fig = _plot_area_boundary(fig, area["region"])
            cpt = vici["tomos"][0]["cmap"]
            fig.colorbar(cmap=cpt, frame=["a2000", "x+lElevation", "y+lm"])
        with fig.set_panel(panel=1):
            fig = fig_tomos(fig, area, [], projection="M?", tect=2, sta=sta)
            fig.text(
                textfiles="src/txt/tects/areaTectName.txt",
                angle=True,
                font=True,
                justify=True,
            )
    fig.savefig(fn)


def plot_rays(regions, df, fig_name):
    topo = make_topos("ETOPO1", regions[0])
    tr = _read_coord(df, sta=True)
    tr["evt"] = tr.apply(lambda r: [r["ex"], r["ey"]], axis=1)
    tr["sta"] = tr.apply(lambda r: [r["sx"], r["sy"]], axis=1)
    lines = df[["evt", "sta"]].values.tolist()
    fig = pygmt.Figure()
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        MAP_TITLE_OFFSET="0.25p",
        MAP_DEGREE_SYMBOL="none",
        FONT_TITLE="18",
        FONT="10",
    )
    # fig = fig_htopo(fig, topos, lines, "0.1p")
    fig = fig_tomos(fig, topo, [], lines=lines, line_pen="0.1p")
    fig = _plot_area_boundary(fig, regions[1], pen="red")
    fig.savefig(fig_name)


def _plot_area_boundary(fig, region, pen="red"):
    [x1, x2, y1, y2] = region
    data = np.array(
        [
            [[x1, y1], [x2, y1]],
            [[x2, y1], [x2, y2]],
            [[x2, y2], [x1, y2]],
            [[x1, y2], [x1, y1]],
        ]
    )
    for ll in data:
        fig.plot(data=ll, pen=pen)
    return fig


def plot_evt_sites(df, region: list, fn: str):
    cen = [sum(region[:2]) / 2, sum(region[-2:]) / 2]
    tr = _read_coord(df, hn=4, sta=None)
    sites = tr[["ex", "ey", "ez", "em"]]
    sites["em"] = sites["em"] * 0.08
    tr["evt"] = tr.apply(lambda r: [r["ex"], r["ey"]], axis=1)
    tr["sta"] = tr["evt"].apply(lambda _: cen)
    lines = df[["evt", "sta"]].values.tolist()

    fig = pygmt.Figure()
    pygmt.config(
        FORMAT_GEO_MAP="+D",
    )
    fig.coast(
        projection=f"E{cen[0]}/{cen[1]}/130/8i",
        region="g",
        shorelines="0.25p,black",
        land="yellow",
        water="white",
        area_thresh=10_000,
        frame="a",
    )
    fig.plot("src/txt/tects/PB2002_plates.dig.txt", pen="1.5p,darkred,.")
    cen = np.array(cen)
    for line in lines:
        fig.plot(data=line, pen="thick,black")
    pygmt.makecpt(
        cmap="src/txt/cptfiles/rainbow.cpt",
        series=[0, 200, 0.01],
        output=(cc := "temp/temp.cpt"),
        background=True,
        reverse="c",
        continuous=True,
    )
    fig.plot(data=sites, style="c", cmap=cc, pen="white")
    fig.plot(data=[cen], style="t0.6c", fill="red", pen="white")

    for dd in range(60, 300, 60):
        fig.plot(data=[cen], style=f"E{dd}d", pen="0.3p,black")
    for y in [60, 90, 120]:
        fig.text(
            text=y,
            x=cen[0],
            y=cen[1] - y,
            font="15.0p",
            offset="0c/0c",
            fill="white",
        )
    fig.colorbar(
        cmap=cc,
        frame='xa40f20+l"Depth (km)"',
        position="jBC+w20c/0.5c+o0c/-2c+m+h",
        shading=True,
    )

    fig.savefig(fn)


def _read_coord(df, hn=2, sta=None):
    txt = Path("src/txt")
    header = ["x", "y", "z", "m"]
    evt = pd.read_csv(
        txt / "event_mag.lst",
        header=None,
        delim_whitespace=True,
        names=["evt"] + header,
        index_col="evt",
    )
    for i in header[:hn]:
        df[f"e{i}"] = df["evt"].apply(lambda en: evt[i][en])
    if sta:
        sta = pd.read_csv(
            "src/txt/station.lst",
            header=None,
            delim_whitespace=True,
            names=["sta"] + header,
            index_col="sta",
        )
        df["sx"] = df["sta"].apply(lambda sn: sta["x"][sn])
        df["sy"] = df["sta"].apply(lambda sn: sta["y"][sn])

    return df


def plot_misfit(grid, region, fig_name) -> None:
    # make cpt file
    cptfile = "temp/temp.cpt"
    pygmt.makecpt(
        cmap="hot",
        series=[-0, 2, 0.05],
        output=cptfile,
        background=True,
        reverse=True,
        continuous=True,
    )
    # make vel grid and get vel grid generated by `surface`
    tomo_grd = "temp/tomo.grd"
    tomo_grid_data(grid, tomo_grd, region)
    # topo file
    topo = make_topos("ETOPO1", region)

    # gmt plot
    _gmt_fig_misfit(topo, {"grid": tomo_grd, "cmap": cptfile}, fig_name)


def _gmt_fig_misfit(topo, tomo, fname):
    # gmt plot
    fig = pygmt.Figure()
    # define figure configuration
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        # MAP_TITLE_OFFSET="0.25p",
        # MAP_DEGREE_SYMBOL="none",
        # FONT_TITLE="18",
        FONT="10",
    )

    title = Path(fname).stem
    sta = pd.read_csv(
        "src/txt/station.lst",
        usecols=[1, 2],
        index_col=None,
        header=None,
        delim_whitespace=True,
    )

    fig = fig_tomos(fig, topo, [tomo], [f"+t{title}", "a"], tect=0, sta=sta)
    # plot colorbar
    fig.colorbar(cmap=tomo["cmap"], position="JRM", frame="xa")

    fig.savefig(fname)


def lines_generator(region, linetype):
    xx = region[:2]
    yy = region[-2:]
    d = 0.5
    hlines = [[[xx[0], y], [xx[1], y]] for y in np.arange(yy[0] + d, yy[1], d)]
    vlines = [[[x, yy[0]], [x, yy[1]]] for x in np.arange(xx[0] + d, xx[1], d)]
    if linetype == "decline":
        l0 = [[116, 34.5], [122, 32.5]]
        yield from _incline(l0, xx, yy, "x", [3, 4])
    elif linetype == "raise":
        l0 = [[116, 30], [119.5, 34]]
        yield from _incline(l0, xx[::-1], yy, "y", [6, 8])
    elif linetype == "xline":
        for ll in hlines:
            yield "x", ll
    elif linetype == "yline":
        for ll in vlines:
            yield "y", ll


def _incline(l0, xx, yy, idt, bias):
    dd = 0.5
    k = (l0[0][1] - l0[1][1]) / (l0[0][0] - l0[1][0])
    b_min = yy[0] - k * xx[0]
    b_max = yy[1] - k * xx[1]

    for b in np.arange(b_min + dd * bias[0], b_max - dd * bias[1], dd):
        xxxx = sorted(xx + [(t - b) / k for t in yy])

        def round_point(x):
            return [round(x, 1), round(k * x + b, 1)]

        ll = [round_point(xxxx[1]), round_point(xxxx[2])]
        yield idt, ll
