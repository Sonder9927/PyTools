import json

from src.info_filter import GridPhv

from .gmt import plot_as, plot_diff, plot_vel


def gmt_plot_all_periods(ps_file) -> None:
    """
    plot [diff vel as cb] of tpwt
    [as] not ready
    """
    with open(ps_file) as f:
        per_se_pairs = json.load(f)

    grid_periods: list[GridPhv] = [
        GridPhv(p, s) for p, s in per_se_pairs.items()
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
        if grid_tpwt_cb := gp.grid_file("tpwt", "cb", "2.0"):
            plot_vel(grid_tpwt_cb, gp.region, gp.fig_tpwt_name("CB"))
        # plot std of tpwt
        if grid_tpwt_std := gp.grid_file("tpwt", "std"):
            plot_as(
                grid_tpwt, grid_tpwt_std, gp.region, gp.fig_tpwt_name("AS")
            )
