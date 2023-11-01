import json
from icecream import ic


from .gmt import plot_as, plot_diff, plot_vel


class PhasePainter:
    def __init__(self, region, ps_file) -> None:
        from src.info_filter import GridPhv

        self.region = region
        with open(ps_file) as f:
            per_se_pairs = json.load(f)
        self.periods = [int(i) for i in per_se_pairs.keys()]
        self.gps: list[GridPhv] = [
            GridPhv(p, s) for p, s in per_se_pairs.items()
        ]

    def vel(self, method, idt, *, periods=None, dcheck=2.0):
        for gp in self._gps(periods):
            if idt == "vel":
                vel = gp.grid_file(method, idt)
                if vel.exists():
                    cpt = {"series": gp.series}
                    plot_vel(vel, self.region, gp.fig_name(method, idt), cpt)
            elif idt == "cb":
                vel = gp.grid_file(method, idt, dcheck=dcheck)
                if vel.exists():
                    plot_vel(vel, self.region, gp.fig_name(method, idt))
            else:
                raise ValueError("choose `vel` or `cb` for idt")

    def std(self, periods=None):
        for gp in self._gps(periods):
            vel = gp.grid_file("tpwt", "vel")
            std = gp.grid_file("tpwt", "std")
            if all([vel.exists(), std.exists()]):
                plot_as(vel, std, self.region, gp.fig_name("tpwt", "as"))

    def diff(self, periods=None):
        for gp in self._gps(periods):
            ant = gp.grid_file("ant", "vel")
            tpwt = gp.grid_file("tpwt", "vel")
            if all([ant.exists(), tpwt.exists()]):
                plot_diff(tpwt, ant, self.region, gp.diff_name())

    def _gps(self, periods):
        pers = periods or self.periods
        return [gp for gp in self.gps if gp.period in pers]


def gmt_plot_all_periods(region, ps_file, dcheck=2.0, **targets) -> None:
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
    for gp in grid_periods:
        cptconfig = {"series": gp.series}
        ant = gp.grid_file("ant", "vel")
        tpwt = gp.grid_file("tpwt", "vel")
        # plot ant phv
        if targets.get("ant") and ant:
            plot_vel(ant, region, gp.fig_name("ant", "Vel"), cptconfig)
        # plot tpwt phv
        if targets.get("tpwt") and tpwt:
            plot_vel(tpwt, region, gp.fig_name("tpwt", "Vel"), cptconfig)
        # plot diff between ant and tpwt
        if targets.get("diff") and all([ant, tpwt]):
            plot_diff(ant, tpwt, region, gp.diff_name())
        # plot checkboard
        if tpwt_cb := _check_target("cb", gp, ["tpwt", "cb", dcheck]):
            plot_vel(tpwt_cb, region, gp.fig_name("tpwt", "CB"))
        # plot standard deviation
        if tpwt_std := _check_target("std", gp, ["tpwt", "std"]):
            plot_as(tpwt, tpwt_std, region, gp.fig_name("tpwt", "AS"))
