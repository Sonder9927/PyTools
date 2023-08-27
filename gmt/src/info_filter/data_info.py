from pathlib import Path
from icecream import ic
import pandas as pd
import pygmt
import json

from src.pygmt_plot.gmt import (
    gmt_blockmean_surface_grdsample,
)

from .points import points_boundary, points_inner
from .grid import GridPhv

# from tpwt_r import Point


def read_xyz(file: Path) -> pd.DataFrame:
    return pd.read_csv(
        file, delim_whitespace=True, usecols=[0, 1, 2], names=["x", "y", "z"]
    )


def vel_info_per(data_file: Path, points: list) -> dict:
    data = read_xyz(data_file)
    data_inner = points_inner(data, points)

    # sourcery skip: inline-immediately-returned-variable
    grid_per = {
        "vel_avg": data_inner.z.mean(),
        "vel_max": data_inner.z.max(),
        "vel_min": data_inner.z.min()
        # "inner_num": len(data_inner.index)
    }

    return grid_per


def standard_deviation_per(ant: Path, tpwt: Path, region, stas) -> float:
    temp = "temp/temp.grd"
    gmt_blockmean_surface_grdsample(ant, temp, temp, region)
    ant_xyz = pygmt.grd2xyz(temp)
    gmt_blockmean_surface_grdsample(tpwt, temp, temp, region)
    tpwt_xyz = pygmt.grd2xyz(temp)
    if ant_xyz is None or tpwt_xyz is None:
        raise ValueError(
            f"""
            Cannot calculate standard deviation with \n
            ant: {ant}\n
            and\n
            tpwt: {tpwt}
            """
        )

    # make diff
    diff = tpwt_xyz
    diff.z = (tpwt_xyz.z - ant_xyz.z) * 1000  # 0.5 X 0.5 grid

    boundary = points_boundary(stas)
    data_inner = points_inner(diff, boundary=boundary)
    std = data_inner.z.std(ddof=0)

    return std


def vel_info(target: str, periods=None):
    region = [115, 122.5, 27.9, 34.3]
    sta_file = "src/txt/station.lst"
    stas = pd.read_csv(
        sta_file, delim_whitespace=True, usecols=[1, 2], names=["x", "y"]
    )
    boundary_points = points_boundary(stas[["x", "y"]])  # default is clock
    # po = clock_sorted(boundary_points)  # no need

    gd = Path("grids")
    if periods is None:
        pg = gd.glob("*/*")
        periods = sorted([int(i.stem.split("_")[-1]) for i in pg])

    gps = [GridPhv(per) for per in periods]
    jsd = {}
    for gp in gps:
        ant = gp.grid_file("ant", "vel")
        tpwt = gp.grid_file("tpwt", "vel")

        ant_info = (
            vel_info_per(ant, boundary_points) if ant is not None else {}
        )
        tpwt_info = (
            vel_info_per(tpwt, boundary_points) if tpwt is not None else {}
        )

        js_per = {}

        ic.disable()
        if all([ant, tpwt]):
            vel_avg_diff = abs(ant_info["vel_avg"] - tpwt_info["vel_avg"])
            vel_avg_diff = "{:.2f} m/s".format(vel_avg_diff * 1000)
            js_per["avg_diff"] = vel_avg_diff
            st = standard_deviation_per(ant, tpwt, region, stas)
            vel_standart_deviation = "{:.2f} m/s".format(st)
            js_per["standard_deviation"] = vel_standart_deviation
            ic(gp.period, vel_avg_diff, vel_standart_deviation)
        else:
            ic(gp.period, "Data info lacked.")
        js_per |= {"ant": ant_info, "tpwt": tpwt_info}

        jsd[str(gp.period)] = js_per

    with open(target, "w+", encoding="UTF-8") as f:
        json.dump(jsd, f)
