from pathlib import Path
from tpwt_r import Point
from icecream import ic
import pandas as pd
import json

from .points import points_boundary, points_inner


def vel_info_per(data_file: Path, points: list) -> dict:
    data = pd.read_csv(data_file, delim_whitespace=True, usecols=[0, 1, 2], names=["x", "y", "z"])
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
            vel_avg_diff = "{:.3f} m/s".format(vel_avg_diff * 1000)
            js_per.update({"avg_diff": vel_avg_diff})
            ic(per, vel_avg_diff)
        else:
            ic(per, "Data info lacked.")
        js_per.update({"ant": ant_info, "tpwt": tpwt_info})

        jsd.update({str(per): js_per})

    with open(target, "w+", encoding="UTF-8") as f:
        json.dump(jsd, f)

