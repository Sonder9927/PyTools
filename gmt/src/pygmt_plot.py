import json

from src import gmt  # pyright: ignore
from src.info_filter import GridPeriod  # pyright: ignore


def gmt_plot_all_periods(ps_file) -> None:
    with open(ps_file) as f:
        per_se_pairs = json.load(f)

    grid_periods: list[GridPeriod] = [
        GridPeriod(p, s) for p, s in per_se_pairs.items()
    ]
    for gp in grid_periods:
        if not (grid_tpwt := gp.grid_tpwt()):
            continue
        # plot vel of tpwt
        gmt.plot_vel(grid_tpwt, gp.region, gp.tpwt_vel_name(), gp.series)

        # plot diff
        if grid_ant := gp.grid_ant():
            gmt.plot_diff(grid_tpwt, grid_ant, gp.region, gp.diff_name())
        # plot checkboard of tpwt
        if grid_tpwt_cb := gp.grid_tpwt_cb():
            gmt.plot_vel(grid_tpwt_cb, gp.region, gp.tpwt_cb_name())
        # plot std of tpwt
        if grid_tpwt_std := gp.grid_tpwt_std():
            gmt.plot_as(grid_tpwt, grid_tpwt_std, gp.region, gp.tpwt_as_name())
