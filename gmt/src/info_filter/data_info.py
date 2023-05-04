from pathlib import Path
from tpwt_r import Point
from icecream import ic
import pandas as pd
import numpy as np
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


def info_of_grid_exists(target: Path, points: list) -> dict:
    if target.exists():

        info = vel_info_per(target, points)
        return info
    else:
        return {}


def standard_deviation_per(diff_grd: str) -> float:
    region = [115, 122.5, 27.9, 34.3]
    sta = pd.read_csv("src/txt/station.lst",
        usecols=[1, 2], index_col=None, header=None, delim_whitespace=True)
    diff = gmt.diff_inner(diff_grd, region, sta)

    return np.std(diff).data.tolist()


def vel_info(periods: list, target: str):
    sta_file = "src/txt/station.lst"
    stas = pd.read_csv(sta_file, delim_whitespace=True, usecols=[1, 2], names=["x", "y"])
    boundary_points = points_boundary(stas[["x", "y"]])  # default is clock
    # po = clock_sorted(boundary_points)  # no need

    gd = Path("grids")

    jsd = dict()
    for per in periods:
        tpwt = gd / "tpwt_grids" / f"tpwt_{per}"
        ant = gd / "ant_grids" / f"ant_{per}"
        ant_info = info_of_grid_exists(ant, boundary_points)
        tpwt_info = info_of_grid_exists(tpwt, boundary_points)

        js_per = dict()

        ic.enable()
        if all([ant_info, tpwt_info]):
            vel_avg_diff = abs(ant_info["vel_avg"]-tpwt_info["vel_avg"])
            vel_avg_diff = "{:.2f} m/s".format(vel_avg_diff * 1000)
            js_per.update({"avg_diff": vel_avg_diff})
            diff_grd = f"src/vel_diff/vel_diff_{per}.grd"
            st = standard_deviation_per(diff_grd)
            vel_standart_deviation = "{:.2f} m/s".format(st)
            js_per.update({"standard_deviation": vel_standart_deviation})
            ic(per, vel_avg_diff, vel_standart_deviation)
        else:
            ic(per, "Data info lacked.")
        js_per.update({"ant": ant_info, "tpwt": tpwt_info})

        jsd.update({str(per): js_per})

    with open(target, "w+", encoding="UTF-8") as f:
        json.dump(jsd, f)

