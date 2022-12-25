from scipy.spatial import ConvexHull
from functools import reduce
import math, operator
import numpy as np
import pandas as pd


def get_boundary_points(file: str):
    """
    Get the boundary of points getted from the file.
    """
    df = pd.read_csv(file, delim_whitespace=True, header=None, usecols=[0, 1], names=["x", "y"], engine="python")
    points = np.array(df)
    hull = ConvexHull(points)

    return points[hull.vertices]


def clock_sorted(points):
    center = tuple(
        map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), points),
        [len(points)]*2)
    )
    clock = sorted(
        points,
        key = lambda p: (
            -135 -math.degrees(math.atan2(*tuple(map(operator.sub, p, center))[::-1]))
        ) % 360,
        reverse = True
    )

    return clock

if __name__ == "__main__":
    points_file = "points_test.txt"
    boundary_points = get_boundary_points(points_file) # default is clock
    print(boundary_points)
    # points = clock_sorted(boundary_points)# no need

