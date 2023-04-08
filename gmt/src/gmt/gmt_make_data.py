from src import grid

from icecream import ic
from pathlib import Path
import pandas as pd
import pygmt


def make_vel(grid, outfile, region) -> str:
    vel = "temp/vel"
    temp_grd = "temp/temp.grd"
    # blockmean
    pygmt.blockmean(
        data = grid,
        outfile = vel,
        region = region,
        spacing = .5,
    )
    # surface
    pygmt.surface(
        data = vel,
        outgrid = temp_grd,
        region = region,
        spacing = .5,
    )
    # grdsample
    pygmt.grdsample(
        grid = temp_grd,
        spacing = .01,
        outgrid = outfile,
    )

    return vel


def make_diff(tpwt, ant, region, outfile):
    temp_grd = "temp/temp.grd"
    # make vel diff tpwt grid
    pygmt.surface(
        data = tpwt,
        outgrid = temp_grd,
        region = region,
        spacing = .5
    )
    tpwt = pygmt.grd2xyz(temp_grd)
    # make vel diff ant grid
    pygmt.surface(
        data = ant,
        outgrid = temp_grd,
        region = region,
        spacing = .5
    )
    ant = pygmt.grd2xyz(temp_grd)

    # make diff
    diff = tpwt
    diff.z = (tpwt.z - ant.z) * 1000
    tomo_diff = "temp/tomo_diff.xyz"
    temp_grd = "temp/temp.grd"
    pygmt.blockmean(
        data = diff,
        region = region,
        spacing = .5,
        outfile = tomo_diff,
    )
    pygmt.surface(
        data = tomo_diff,
        outgrid = temp_grd,
        region = region,
        spacing = .5,
    )
    pygmt.grdsample(
        grid = temp_grd,
        region = region,
        spacing = .01,
        outgrid = outfile,
    )


def get_info(grd_file: str, ndigits: int=1) -> list[float]:
    # pick up both min and max vel of grd_file
    grd = pd.read_csv(grd_file, usecols=[2], names=["vel"],
        index_col=None, header=None, delim_whitespace=True)

    series = [min(grd.vel), max(grd.vel)]
    min_vel = int(pow(10, ndigits) * series[0] - 1) / pow(10, ndigits)
    max_vel = int(pow(10, ndigits) * series[1] + 2) / pow(10, ndigits)

    return [min_vel, max_vel]
    

###############################################################################


def make_grd(tpwt, ant, region, cptfile, tpwt_grd, ant_grd, diff_grd):
    # pick up information of series for `makecpt`
    series = get_info(tpwt) + get_info(ant)
    series = [min(series), max(series), .1]
    # make cpt file
    pygmt.makecpt(
        cmap = "seis",
        series = series,
        background = "",
        continuous = "",
        output = cptfile,
    )

    # make vel grid of tpwt and get vel grid generated by `blockmean` for `make_diff`
    vel = make_vel(tpwt, tpwt_grd, region)
    vel_tpwt = f"{vel}_tpwt"
    Path(vel).rename(vel_tpwt)
    # make vel grid of ant and get vel grid generated by `blockmean` for `make_diff`
    vel= make_vel(ant, ant_grd, region)
    vel_ant = f"{vel}_ant"
    Path(vel).rename(vel_ant)

    # make diff grid
    make_diff(vel_tpwt, vel_ant, region, diff_grd)


def make_topo(topo, region, outfile):
    TOPO_GRD = "temp/topo.grd"
    TOPO_GRD2 = "temp/topo.grd2"
    # grdcut
    pygmt.grdcut(
        grid = topo,
        region = region,
        outgrid = TOPO_GRD,
    )
    # grdsample
    pygmt.grdsample(
        grid =  TOPO_GRD,
        outgrid = TOPO_GRD2,
        region = region,
        spacing = .01,
    )
    # grdgradient
    pygmt.grdgradient(
        grid = TOPO_GRD2,
        outgrid = outfile,
        azimuth = 45,
        normalize = "t",
        verbose = "",
    )


def grid_inner_for_grdimage(grdfile: str, region, sta):
    # cut vel_diff_grd by the boundary of stations
    data = pygmt.grd2xyz(grdfile)

    boundary = grid.points_boundary(sta)
    data_inner = grid.points_inner(data, boundary=boundary)

    return pygmt.xyz2grd(data=data_inner, region=region, spacing=.01)
