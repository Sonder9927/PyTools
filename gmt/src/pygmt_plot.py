import json
from pathlib import Path

import pandas as pd

from .gmt import plot_as, plot_dispersion_curve, plot_diff, plot_vel
from .info_filter import GridPeriod


def gmt_plot_all_periods(ps_file) -> None:
    """
    plot [diff vel as cb] of tpwt
    [as] not ready
    """
    with open(ps_file) as f:
        per_se_pairs = json.load(f)

    grid_periods: list[GridPeriod] = [
        GridPeriod(p, s) for p, s in per_se_pairs.items()
    ]
    for gp in grid_periods:
        if not (grid_tpwt := gp.grid_file("tpwt", "vel")):
            continue
        # plot vel of tpwt
        plot_vel(grid_tpwt, gp.region, gp.fig_tpwt_name("Vel"), gp.series)

        # plot diff
        if grid_ant := gp.grid_file("ant", "vel"):
            plot_diff(grid_tpwt, grid_ant, gp.region, gp.diff_name())
        # plot checkboard of tpwt
        if grid_tpwt_cb := gp.grid_file("tpwt", "cb"):
            plot_vel(grid_tpwt_cb, gp.region, gp.fig_tpwt_name("CB"))
        # plot std of tpwt
        if grid_tpwt_std := gp.grid_file("tpwt", "std"):
            plot_as(
                grid_tpwt, grid_tpwt_std, gp.region, gp.fig_tpwt_name("AS")
            )


def gmt_plot_dispersion_curves():
    """
    plot dispersion curves of tpwt and ant
    """
    gp = Path("grids")
    merged_ant = merge_periods_data(gp, "ant", "vel")
    merged_tpwt = merge_periods_data(gp, "tpwt", "vel")
    merged_data = pd.merge(merged_ant, merged_tpwt, on=["x", "y"], how="left")
    save_path = Path("images") / "dispersion_curves"
    if not save_path.exists():
        save_path.mkdir()
    for _, vs in merged_data.iterrows():
        plot_dispersion_curve(vs.to_dict(), save_path)

    # plot_dc(
    #     ant_dispersion,
    #     tpwt_dispersion,
    #     r"images/diff_figs/dispersion_curves.png",
    # )


def merge_periods_data(gp: Path, method: str, idt: str):
    merged_data = None
    for f in gp.glob(f"{method}_grids/*{idt}*"):
        per = f.stem.split("_")[-1]
        col_name = f"{method}_{per}"
        data = pd.read_csv(
            f, header=None, delim_whitespace=True, names=["x", "y", col_name]
        )
        if merged_data is None:
            merged_data = data
        else:
            merged_data = pd.merge(
                merged_data, data, on=["x", "y"], how="left"
            )
    return merged_data
