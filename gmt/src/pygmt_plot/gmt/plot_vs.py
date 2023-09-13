from pathlib import Path

from icecream import ic
import pandas as pd
import pygmt

from .gmt_fig import fig_htomo, fig_htopo, fig_vtomo, fig_vtopo
from .gmt_make_data import tomo_grid_data, topo_gradient
from .plane import vplane_clip_data, vplane_makecpt


# plot v plane
def plot_vs_vplane(
    vs, idt, *, moho, line, path, hregion, fname, dep=-250, ave=False
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
        for c in ["crust.cpt", "lithos.cpt", "topo_gray.cpt", "ave.cpt"]
    ]
    vplane_makecpt(*cptfiles)
    targets = ["crust", "lithos", "topo", "ave"]
    cpts = dict(zip(targets, cptfiles))

    # vs grid
    grid = vs[[idt, "z", "v"]]
    grid.columns = ["x", "y", "z"]
    vs_grd = temp / "vs.grd"
    tomo_grid_data(grid, vs_grd, lregion, blockmean=[0.5, 1])
    tomos = dict(zip(["vs", "topo"], [vs_grd, topo_grd]))
    suffix = "_ave"
    if not ave:
        ic("Clipping moho from vs.grd...")
        # cut tomo_moho from vs_grd
        tomos["moho"] = vplane_clip_data(vs_grd, promoho, lregion)
        ic("Maked moho data!")
        suffix = "_vel"

    fname = f"{fname}_{idt}{suffix}.png"
    ic("figing...")
    gmt_plot_vs_vplane(
        tomos,
        cpts,
        hregion=hregion,
        vregion=lregion,
        moho=promoho,
        topo=protopo,
        gra=topo_gra,
        line=line,
        fname=fname,
        ave=ave,
    )


def plot_vs_hplane(grid, region, fname):
    """
    gmt plot hplane of vs
    """
    # topo file
    topo = "ETOPO1"
    topo_data = f"src/txt/{topo}.grd"
    topo_gra = f"temp/topo_{topo}.gradient"
    topo_gradient(topo_gra, region, "t", data=topo_data)

    # make cpt file
    cmap = "seis"
    cptfile = "temp/temp.cpt"
    pygmt.makecpt(
        cmap=cmap,
        series=[2, 4, 0.05],
        output=cptfile,
        continuous="",
        background=True,
    )

    # make tomo grid data
    tomo_grd = "temp/tomo.grd"
    tomo_grid_data(grid, tomo_grd, region)

    # gmt plot hplane
    gmt_plot_vs_hplane(region, cptfile, tomo_grd, topo_gra, fname)


# gmt plot v plane
def gmt_plot_vs_vplane(
    tomos, cpts, hregion, vregion, moho, topo, gra, line, fname, ave
):
    # gmt plot
    fig = pygmt.Figure()
    title = Path(fname).stem
    # define figure configuration
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        MAP_TITLE_OFFSET="0.25p",
        MAP_DEGREE_SYMBOL="none",
        FONT_TITLE="18",
    )
    fig = fig_vtopo(fig, topo, vregion[:2] + [0, 6000], title)
    fig.shift_origin(yshift="-5.5")
    if ave:
        cmap = cpts["ave"]
        fig = fig_vtomo(fig, [tomos["vs"]], [cmap], moho=moho, region=vregion)
        fig.shift_origin(yshift="-2")
        fig.colorbar(
            cmap=cmap,
            position="JBC+w3i/0.10i+o0c/-0.5i+h",
            frame="xa2f2",
        )
    else:
        tms = [tomos[i] for i in ["vs", "moho"]]
        cs = [cpts[i] for i in ["lithos", "crust"]]
        fig = fig_vtomo(fig, tms, cs, moho=moho, region=vregion)
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
    fig = fig_htopo(fig, tomos["topo"], cpts["topo"], hregion, gra, line)

    fig.savefig(fname)


def gmt_plot_vs_hplane(region, cpt, tomo_grd, topo_gra, fname):
    fig = pygmt.Figure()

    # define figure configuration
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        # MAP_TITLE_OFFSET="0.25p",
        # MAP_DEGREE_SYMBOL="none",
        MAP_FRAME_WIDTH="0.1c",
        FONT_ANNOT_PRIMARY="20p,Times-Roman",
        FONT_TITLE="20p,Times-Roman",
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
    fig = fig_htomo(fig, tomo_grd, region, title, cpt, topo_gra, sta=sta)
    # plot colorbar
    fig.colorbar(
        cmap=cpt, position="jMR+v+w10c/0.3c+o-1.5c/0c+m", frame="xa0.2f0.2"
    )
    fig.colorbar(
        cmap=cpt, position="jTC+w10c/0.3c+o0i/-4c+h", frame="xa0.2f0.2"
    )
    fig.colorbar(
        cmap=cpt, position="jML+w10c/0.3c+o-1.5i/0i+v", frame="xa0.2f0.2"
    )
    fig.colorbar(
        cmap=cpt, position="jBC+w10c/0.3c+o0i/-2c+h+m", frame="xa0.2f0.2"
    )

    fig.savefig(fname)
