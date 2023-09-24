from pathlib import Path

from icecream import ic
import numpy as np
import pandas as pd
import pygmt

from .gmt_fig import fig_htomo, fig_htopo, fig_vtomo, fig_vtopo
from .gmt_make_data import tomo_grid_data, topo_gradient
from .plane import vplane_clip_data, vplane_makecpt


# plot v plane
def plot_vs_vplane(
    vs, *, idt, moho, line, path, hregion, fname, dep=-250, ave=False
):
    """
    gmt plot vplane of vs contain abso and ave.
    The abscissa is determined by `idt` which should be x or y.
    """
    ic(line, idt)
    if idt == "x":
        idtn = 0
    elif idt == "y":
        idtn = 1
    else:
        raise KeyError("Please select `x` or `y` for abscissa of vplane")
    # vregion = [hregion[idtn * 2], hregion[idtn * 2 + 1], -250, 0]
    lregion = sorted([r[idtn] for r in line]) + [dep, 0]
    temp = Path("temp")
    # moho
    promoho = moho[[idt, "z"]]
    promoho.columns = ["x", "y"]
    # protopo
    topo = "ETOPO1"
    topo_data = f"src/txt/{topo}.grd"
    protopo: pd.DataFrame = pygmt.grdtrack(
        points=path,
        grid=topo_data,
        newcolname="newz",
        verbose="w",
        coltypes="g",
    )  # pyright: ignore
    protopo.columns = ["x", "y", "n", "z"]
    protopo = protopo[[idt, "z"]]
    # topo gradient
    topo_gra = temp / f"topo_{topo}.gradient"
    topo_grd = temp / f"topo_{topo}.grd"
    topo_gradient(topo_gra, hregion, "t", data=topo_data, grd=topo_grd)

    # make cpt files
    cptfiles = [
        str(temp / c)
        for c in ["crust.cpt", "lithos.cpt", "topo_gray.cpt", "Vave.cpt"]
    ]
    vplane_makecpt(*cptfiles)
    targets = ["crust", "lithos", "topo", "ave"]
    cpts = dict(zip(targets, cptfiles))

    # vs grid
    grid = vs[[idt, "z", "v"]]
    grid.columns = ["x", "y", "z"]
    vs_grd = temp / "vs.grd"
    tomo_grid_data(grid, vs_grd, lregion, blockmean=[0.5, 1])
    tomos = dict(zip(["lithos", "topo"], [vs_grd, topo_grd]))
    suffix = "_ave"
    if not ave:
        ic("Clipping moho from vs.grd...")
        # cut tomo_moho from vs_grd
        tomos["crust"] = vplane_clip_data(vs_grd, promoho, lregion)
        ic("Maked crust data!")
        suffix = "_vel"

    fname = f"{fname}_{idt}{suffix}.png"
    gmt_plot_vs_vplane(
        tomos,
        cpts,
        areas={"v": lregion, "h": hregion},
        # TODO
        # borders={"moho": promoho, "lab": lab_by_vel_gra(vs_grd)},
        borders={"moho": promoho},
        topo=protopo,
        gra=topo_gra,
        line=line,
        fn=fname,
        ave=ave,
    )


def plot_vs_hplane(grid, region, fname, *, ave):
    """
    gmt plot hplane of vs
    """
    # topo file
    topo = "ETOPO1"
    topo_data = f"src/txt/{topo}.grd"
    topo_gra = f"temp/topo_{topo}.gradient"
    topo_gradient(topo_gra, region, "t", data=topo_data)

    # make cpt file
    cptfile = "temp/vs_temp.cpt"
    cmap = "src/txt/cptfiles/seismic.cpt"
    if ave:
        pygmt.makecpt(
            cmap="polar",
            series=[-15, 15, 0.1],
            output=cptfile,
            continuous=True,
            background=True,
            reverse=True,
        )
    else:
        series = [2.5, 5.5, 0.1]
        pygmt.makecpt(
            cmap=cmap,
            series=series,
            output=cptfile,
            continuous=True,
            background=True,
        )

    # make tomo grid data
    tomo_grd = "temp/tomo.grd"
    tomo_grid_data(grid, tomo_grd, region)

    # gmt plot hplane
    gmt_plot_vs_hplane(tomo_grd, cptfile, region, topo_gra, fname)


# gmt plot v plane
def gmt_plot_vs_vplane(tomos, cpts, areas, borders, topo, gra, line, fn, ave):
    ic("figing...")
    # gmt plot
    fig = pygmt.Figure()
    title = Path(fn).stem
    # define figure configuration
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        MAP_TITLE_OFFSET="0.25p",
        MAP_DEGREE_SYMBOL="none",
        FONT_TITLE="18",
    )
    fig = fig_vtopo(fig, topo, areas["v"][:2] + [0, 2000], title)
    fig.shift_origin(yshift="-5.5")
    if ave:
        tms = [tomos["lithos"]]
        fig = fig_vtomo(fig, tms, [cpts["ave"]], areas["v"], borders)
        fig.shift_origin(yshift="-2")
        fig.colorbar(
            cmap=cpts["ave"],
            position="JBC+w3i/0.10i+o0c/-0.5i+h",
            frame="xa5f5",
        )
    else:
        tms = [tomos[i] for i in ["lithos", "crust"]]
        cs = [cpts[i] for i in ["lithos", "crust"]]
        fig = fig_vtomo(fig, tms, cs, areas["v"], borders)
        fig.shift_origin(yshift="-2")
        fig.colorbar(
            cmap=cpts["crust"],
            position="JBC+w3i/0.10i+o0c/-0.5i+h",
            frame="xa0.2f0.2",
        )
        fig.shift_origin(yshift="-1")
        fig.colorbar(
            cmap=cpts["lithos"],
            position="JBC+w3i/0.10i+o0c/-0.5i+h",
            frame="xa0.2f0.2",
        )
    fig.shift_origin(yshift="-4.5", xshift="3")
    fig = fig_htopo(fig, tomos["topo"], cpts["topo"], areas["h"], gra, line)

    fig.savefig(fn)


def gmt_plot_vs_hplane(grd, cpt, region, gra, fname):
    fig = pygmt.Figure()

    # define figure configuration
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        # MAP_TITLE_OFFSET="0.25p",
        # MAP_DEGREE_SYMBOL="none",
        MAP_FRAME_WIDTH="0.1c",
        FONT_ANNOT_PRIMARY="10p,Times-Roman",
        FONT_TITLE="13p,Times-Roman",
        # FONT="10",
    )

    # plot vel fig
    title = Path(fname).stem
    sta = pd.read_csv(
        "src/txt/station.lst",
        usecols=[1, 2],
        index_col=None,
        header=None,
        delim_whitespace=True,
    )
    fig = fig_htomo(fig, grd, region, title, cpt, gra, sta=sta)
    fig.colorbar(cmap=cpt, position="jBC+w5c/0.3c+o0i/-1c+h+m", frame="x5f5")
    # plot colorbar
    # fig.colorbar(
    #     cmap=cpt, position="jMR+v+w10c/0.3c+o-1.5c/0c+m", frame="xa0.2f0.2"
    # )
    # fig.colorbar(
    #     cmap=cpt, position="jTC+w10c/0.3c+o0i/-4c+h", frame="xa0.2f0.2"
    # )
    # fig.colorbar(
    #     cmap=cpt, position="jML+w10c/0.3c+o-1.5i/0i+v", frame="xa0.2f0.2"
    # )

    fig.savefig(fname)


def lab_by_vel_gra(grd):
    df: pd.DataFrame = pygmt.grd2xyz(grd)  # pyright: ignore
    dfx = df.x.unique()
    xmin = df.x.min()
    df["x"] = (df["x"] - xmin) * 111
    z_matrix = df.pivot(index="y", columns="x", values="z").to_numpy()
    gra = np.gradient(z_matrix, axis=0)
    gra_df = pd.DataFrame(gra, index=df.y.unique(), columns=df.x.unique())
    deps = gra_df.idxmax()
    return pd.DataFrame({"x": dfx, "y": deps})
