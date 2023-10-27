from functools import reduce
import math
import operator

import numpy as np
import pandas as pd
from scipy.spatial import ConvexHull
from tpwt_r import Point  # pyright: ignore
import xarray as xr


def hull_points(data: pd.DataFrame) -> None:
    ff = "src/txt/sta_hull.nc"
    points = data[["x", "y"]].values
    hull = ConvexHull(points)
    hull_points = points[hull.vertices]
    df = pd.DataFrame(hull_points, columns=["x", "y"])
    # df.to_csv(pf, sep="\t", index=False, header=False)
    ds = xr.Dataset(
        {"x_values": ("points", df["x"]), "y_values": ("points", df["y"])},
        coords={
            "x_coords": ("points", df["x"]),
            "y_coords": ("points", df["y"]),
        },
    )
    ds.to_netcdf(ff)


###############################################################################


def times_of_crossing_boundary(point: Point, points: list[Point]) -> int:
    times = 0
    for i in range(len(points)):
        segment_start = points[i]
        segment_end = points[0] if i == len(points) - 1 else points[i + 1]
        if point.is_ray_intersects_segment(segment_start, segment_end):
            times += 1

    return times


def clock_sorted(points):
    center = tuple(
        map(
            operator.truediv,
            reduce(lambda x, y: map(operator.add, x, y), points),
            [len(points)] * 2,
        )
    )
    return sorted(
        points,
        key=lambda p: (
            -135
            - math.degrees(
                math.atan2(*tuple(map(operator.sub, p, center))[::-1])
            )
        )
        % 360,
        reverse=True,
    )


def points_boundary(grids: pd.DataFrame, clock=False):
    """
    Get the boundary of points getted from the file.
    """
    data = np.array(grids)
    hull = ConvexHull(data)
    points = data[hull.vertices]
    if clock:
        points = clock_sorted(points)

    return points


def points_inner(data: pd.DataFrame, boundary) -> pd.DataFrame:
    lo = [i[0] for i in boundary]
    la = [i[1] for i in boundary]

    points_in_rect = data[
        (data["y"] < max(la))
        & (data["y"] > min(la))
        & (data["x"] < max(lo))
        & (data["x"] > min(lo))
    ].copy()

    boundary_points: list[Point] = [Point(p.tolist()) for p in boundary]

    points_in_rect["times"] = points_in_rect.apply(
        lambda dd: times_of_crossing_boundary(
            Point(x=dd.loc["x"], y=dd.loc["y"]), boundary_points
        ),
        axis=1,
    )
    data = points_in_rect[points_in_rect["times"] % 2 == 1].drop(
        columns=["times"]
    )

    return data
