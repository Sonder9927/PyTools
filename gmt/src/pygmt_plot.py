import json

from .gmt import plot_as, plot_vel, plot_diff, plot_dc
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
        if not (grid_tpwt := gp.grid_tpwt()):
            continue
        # plot vel of tpwt
        plot_vel(grid_tpwt, gp.region, gp.tpwt_vel_name(), gp.series)

        # plot diff
        if grid_ant := gp.grid_ant():
            plot_diff(grid_tpwt, grid_ant, gp.region, gp.diff_name())
        # plot checkboard of tpwt
        if grid_tpwt_cb := gp.grid_tpwt_cb():
            plot_vel(grid_tpwt_cb, gp.region, gp.tpwt_cb_name())
        # plot std of tpwt
        if grid_tpwt_std := gp.grid_tpwt_std():
            plot_as(grid_tpwt, grid_tpwt_std, gp.region, gp.tpwt_as_name())


def gmt_plot_dispersion_curves(info_file):
    """
    plot dispersion curves of tpwt and ant
    """
    with open(info_file) as f:
        vel_info = json.load(f)

    # dispersion curve of ant
    ant_dispersion = []
    # dispersion curve of tpwt
    tpwt_dispersion = []
    for per, info in vel_info.items():
        if ant_info := info.get("ant"):
            ant_dispersion.append([int(per), float(ant_info["vel_avg"])])
        if tpwt_info := info.get("tpwt"):
            tpwt_dispersion.append([int(per), float(tpwt_info["vel_avg"])])

    plot_dc(
        ant_dispersion,
        tpwt_dispersion,
        r"images/diff_figs/dispersion_curves.png",
    )
