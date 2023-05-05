from pathlib import Path
from tpwt_r import Point
from icecream import ic
import pandas as pd
import numpy as np
import pygmt
import json

from src import gmt

from .points import points_boundary, points_inner


def read_xyz(file: Path) -> pd.DataFrame:
    return pd.read_csv(file, delim_whitespace=True, usecols=[0, 1, 2], names=["x", "y", "z"])


def vel_info_per(data_file: Path, points: list) -> dict:
    data = read_xyz(data_file)
    data_inner = points_inner(data, points)

    grid_per = {
        "vel_avg": data_inner.z.mean(),
        "vel_max": data_inner.z.max(),
        "vel_min": data_inner.z.min()
        # "inner_num": len(data_inner.index)
    }

    return grid_per


def standard_deviation_per(ant, tpwt, region, stas, spacing) -> float:
    temp = "temp/temp.grd"
    gmt.gmt_blockmean_surface_grdsample(ant, temp, temp, region)
    ant = pygmt.grd2xyz(temp)
    gmt.gmt_blockmean_surface_grdsample(tpwt, temp, temp, region)
    tpwt = pygmt.grd2xyz(temp)

    # make diff
    diff = tpwt
    diff.z = (tpwt.z - ant.z) * 1000
    gmt.gmt_blockmean_surface_grdsample(diff, temp, temp, region, outgrid=temp, spacing=spacing)

    diff = gmt.diff_inner(temp, region, stas)

    return np.std(diff).data.tolist()


def vel_info(periods: list, target: str, spacing: float):
    region = [115, 122.5, 27.9, 34.3]
    sta_file = "src/txt/station.lst"
    stas = pd.read_csv(sta_file, delim_whitespace=True, usecols=[1, 2], names=["x", "y"])
    boundary_points = points_boundary(stas[["x", "y"]])  # default is clock
    # po = clock_sorted(boundary_points)  # no need

    gd = Path("grids")

    jsd = dict()
    for per in periods:
        ant = gd / "ant_grids" / f"ant_{per}"
        tpwt = gd / "tpwt_grids" / f"tpwt_{per}"

        ant_info = vel_info_per(ant, boundary_points) if (a := ant.exists()) else {}
        tpwt_info = vel_info_per(tpwt, boundary_points) if (t := tpwt.exists()) else {}

        js_per = dict()

        ic.disable()
        if all([a, t]):
            vel_avg_diff = abs(ant_info["vel_avg"]-tpwt_info["vel_avg"])
            vel_avg_diff = "{:.2f} m/s".format(vel_avg_diff * 1000)
            js_per.update({"avg_diff": vel_avg_diff})
            st = standard_deviation_per(ant, tpwt, region, stas, spacing=spacing)
            vel_standart_deviation = "{:.2f} m/s".format(st)
            js_per.update({"standard_deviation": vel_standart_deviation})
            ic(per, vel_avg_diff, vel_standart_deviation)
        else:
            ic(per, "Data info lacked.")
        js_per.update({"ant": ant_info, "tpwt": tpwt_info})

        jsd.update({str(per): js_per})

    with open(target, "w+", encoding="UTF-8") as f:
        json.dump(jsd, f)

