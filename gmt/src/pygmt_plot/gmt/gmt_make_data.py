from pathlib import Path

import pandas as pd
import pygmt
from src import info_filter


def diff_make(ant, tpwt, region, cptfile, ant_grd, tpwt_grd, outgrid):
    # pick up information of series for `makecpt`
    seriess = get_info(tpwt) + get_info(ant)
    sm = sum(seriess) / 4
    series = [sm - 0.1, sm + 0.1, 0.1]
    # make cpt file
    pygmt.makecpt(
        cmap="seis",
        series=series,
        background=True,
        continuous=True,
        output=cptfile,
    )

    # make vel grid of ant and get vel grid generated by `surface`
    ant_sf = tomo_grid_data(ant, ant_grd, region, preffix="ant")
    # make vel grid of tpwt and get vel grid generated by `surface`
    tpwt_sf = tomo_grid_data(tpwt, tpwt_grd, region, preffix="tpwt")

    # make diff grid
    ant = pygmt.grd2xyz(ant_sf)
    tpwt = pygmt.grd2xyz(tpwt_sf)
    diff = tpwt
    diff.z = (tpwt.z - ant.z) * 1000  # pyright: ignore
    tomo_grid_data(diff, outgrid, region)


def topo_gradient(
    gra, region, normalize, *, data=None, resolution="01m", grd=None
):
    if Path(gra).exists():
        return
    TOPO_CUT = "temp/topo_cut.grd"
    TOPO_SAMPLE = "temp/topo_sample.grd"
    data = data or pygmt.datasets.load_earth_relief(
        resolution=resolution, region=region, registration="gridline"
    )
    # grdcut
    pygmt.grdcut(
        grid=data,
        region=region,
        outgrid=TOPO_CUT,
    )
    # grdsample
    pygmt.grdsample(
        grid=TOPO_CUT,
        outgrid=TOPO_SAMPLE,
        region=region,
        spacing=0.01,
        # translate=True,
    )
    TOPO_GRA = "temp/topo.gradient"
    # grdgradient
    pygmt.grdgradient(
        grid=TOPO_SAMPLE,
        outgrid=TOPO_GRA,
        azimuth=45,
        normalize=normalize,
        verbose="w",
    )
    Path(TOPO_GRA).rename(gra)
    if grd is not None:
        Path(TOPO_SAMPLE).rename(grd)


###############################################################################


def tomo_grid_data(data, outgrid, region, *, preffix="", **spacings) -> str:
    bm_out = "temp/bm_temp"
    sf_grd = "temp/sf.grd"
    gmt_blockmean_surface_grdsample(
        data, bm_out, sf_grd, region, spacings=spacings, outgrid=outgrid
    )

    pre_sf = Path(sf_grd)
    if preffix:
        pre_sf = pre_sf.parent / f"{preffix}_{pre_sf.name}"
        Path(sf_grd).rename(pre_sf)

    return str(pre_sf)


def gmt_blockmean_surface_grdsample(
    data, bm_output, sf_output, region, *, outgrid=None, spacings={}
):
    # blockmean
    pygmt.blockmean(
        data=data,
        outfile=bm_output,
        region=region,
        spacing=spacings.get("blockmean") or 0.5,
    )
    # surface
    pygmt.surface(
        data=bm_output,
        outgrid=sf_output,
        region=region,
        spacing=spacings.get("surface") or 0.5,
    )
    if outgrid is not None:
        # grdsample
        pygmt.grdsample(
            grid=sf_output,
            spacing=spacings.get("grdsample") or 0.01,
            outgrid=outgrid,
        )


def get_info(grd_file: str, ndigits: int = 1) -> list[float]:
    # pick up both min and max vel of grd_file
    grd = pd.read_csv(
        grd_file,
        usecols=[2],
        names=["vel"],
        index_col=None,
        header=None,
        delim_whitespace=True,
    )

    series = [min(grd.vel), max(grd.vel)]
    min_vel = int(pow(10, ndigits) * series[0] - 1) / pow(10, ndigits)
    max_vel = int(pow(10, ndigits) * series[1] + 2) / pow(10, ndigits)

    return [min_vel, max_vel]


def sta_clip(grdfile: str, region, sta):
    # # TODO use pygmt.select
    # sta_boundary = info_filter.points_boundary(sta)
    # grd = pygmt.select(data=vel_grd, polygon=sta_boundary)
    # cut vel_diff_grd by the boundary of stations
    data = pygmt.grd2xyz(grdfile)

    boundary = info_filter.points_boundary(sta, clock=True)
    data_inner = info_filter.points_inner(data, boundary=boundary)

    return pygmt.xyz2grd(data=data_inner, region=region, spacing=0.01)


# def vel_make(grid_vel, region, cptfiles, vel_grd, series):
#     if series is None:
#         series = get_info(grid_vel)
#         avg = sum(series) / 2
#         dev = min(abs(i - avg) for i in series)
#         series = [avg - dev, avg + dev, 0.05]
#     # make cpt file
#     pygmt.makecpt(
#         cmap="grayC",
#         series=[-100, 2000, 200],
#         continuous=True,
#         output=cptfiles[0],
#     )
#     pygmt.makecpt(
#         cmap="src/txt/Vc_1.8s.cpt",
#         series=series,
#         background=True,
#         continuous=True,
#         output=cptfiles[1],
#     )

#     # make vel grid and get vel grid generated by `surface`
#     tomo_grid_data(grid_vel, vel_grd, region)


# def vs_make(grid, region, cptfile, outgrid):
#     # make cpt file
#     pygmt.makecpt(
#         cmap="gridvel_6_v3.cpt",
#         series=[-10, 10, 0.05],
#         # continuous=True,
#         output=cptfile,
#     )
#     # make vel grid and get vel grid generated by `surface`
#     tomo_grid_data(grid, outgrid, region)


# def misfit_make(grid, region, cptfile, outgrid):
#     # make cpt file
#     pygmt.makecpt(
#         cmap="hot",
#         series=[-0, 2, 0.05],
#         continuous=True,
#         output=cptfile,
#     )
#     # make vel grid and get vel grid generated by `surface`
#     tomo_grid_data(grid, outgrid, region)
