from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .gmt import plot_area_map, plot_evt_sites, plot_rays, plot_misfit


def gmt_plot_area(region, pesf):
    vicinity = [110, 125, 25, 40]
    ip = Path("images/area_figs")
    if not ip.exists():
        ip.mkdir()
    plot_area_map([vicinity, region], str(ip / "area.png"))
    return
    pes = pd.read_csv(pesf)

    # _plot_per_evt(pes.groupby("per").size().to_dict(), ip / "perNum_vel.png")
    rays = pes[["evt", "sta"]].drop_duplicates()
    sites = rays[["evt"]].drop_duplicates()
    # plot_evt_sites(sites, region, str(ip / "evt_sites.png"))
    # plot_rays([vicinity, region], rays, str(ip / "rays_cover.png"))


def gmt_plot_misfit(mm_file, region):
    grid = pd.read_csv(mm_file)[["x", "y", "misfit"]]
    grid.rename(columns={"misfit": "z"}, inplace=True)
    plot_misfit(grid, region, "images/mc_figs/misfit.png")


def _plot_per_evt(data: dict, fn):
    pers = [25, 30] + [35, 40, 45, 50, 60, 70, 80, 90, 100, 111, 125, 143]
    pns = []
    vels_res = []
    for per in pers:
        pns.append(data[per])
        vel = pd.read_csv(
            f"grids/tpwt_grids/tpwt_vel_{per}.grid",
            header=None,
            delim_whitespace=True,
            usecols=[2],
            names=["vel"],
        )
        vels_res.append(vel["vel"].mean())

    vels_init = (
        [3.365, 3.43]
        + [3.51, 3.55, 3.57, 3.59]
        + [3.63, 3.67, 3.71, 3.75, 3.79, 3.82, 3.85, 3.92]
    )

    fig = plt.figure(figsize=(10, 6))
    ax1 = fig.add_subplot(111)
    ax1.bar(pers, pns, width=4)
    ax1.set_ylabel("Number of Ray")
    ax2 = ax1.twinx()
    # ax2.plot(pers, vels_init, "b", label="Vel Init")
    ax2.plot(pers, vels_res, "r", label="Average Phv")
    ax2.set_ylabel("Velocity")
    ax2.legend(loc="upper right")
    fig.savefig(fn)
