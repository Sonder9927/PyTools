import json

from src.info_filter import GridPhv

from .gmt import plot_as, plot_diff, plot_vel


def gmt_plot_all_periods(ps_file, dcheck=1.5, **targets) -> None:
    """
    plot [diff vel as cb] of tpwt
    [as] not ready
    """

    def _check_target(idt, gpobj, params: list):
        return gpobj.grid_file(*params) if targets.get(idt) else False

    with open(ps_file) as f:
        per_se_pairs = json.load(f)

    grid_periods: list[GridPhv] = [
        GridPhv(p, s) for p, s in per_se_pairs.items()
    ]
    # dcheck = targets["dcheck"] or "1.5"
    for gp in grid_periods:
        # plot tpwt phv
        tpwt = gp.grid_file("tpwt", "vel")
        # plot diff between ant and tpwt
        if ant := _check_target("diff", gp, ["ant", "vel"]):
            plot_diff(tpwt, ant, gp.region, gp.diff_name())
        # plot checkboard
        if tpwt_cb := _check_target("checkboard", gp, ["tpwt", "cb", dcheck]):
            plot_vel(tpwt_cb, gp.region, gp.fig_tpwt_name("CB"))
        # plot standard deviation
        if tpwt_std := _check_target("std", gp, ["tpwt", "std"]):
            plot_as(tpwt, tpwt_std, gp.region, gp.fig_tpwt_name("AS"))
        if tpwt := _check_target("tpwt", gp, ["tpwt", "vel"]):
            plot_vel(tpwt, gp.region, gp.fig_tpwt_name("Vel"), gp.series)
