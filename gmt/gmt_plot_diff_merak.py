"""
Author: Sonder Merak
Version: 0.1.0
Description: Contract 2 grid files generated from ANT or TPWT.
"""

import pandas as pd
import pygmt


def cal_grd_diff(f1, f2):
    load_grd = lambda f: pd.read_csv(f,
        delim_whitespace=True, header=None, names=["lo", "la", "vel"]
    ).sort_values(by=["lo", "la"])

    grd1 = load_grd(f1)
    print(grd1.head())
    grd2 = load_grd(f2)
    print(grd2.head())

    grd1.vel = grd1.vel - grd2.vel

    return grd1


def gmt_plot(grd):
    pass


def grd_plot(f1, f2):

    grd = cal_grd_diff(f1, f2)

    gmt_plot(grd)


if __name__ == "__main__":
    grd_plot("grids/test1.grd", "grids/test2.grd")

