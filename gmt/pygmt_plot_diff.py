from src import gmt
from src.info_filter import GridPeriod
import json
# from icecream import ic
from tqdm import tqdm


def gmt_plot_all_periods(ps) -> None:
    # grid_periods: list[GridPeriod] = [GridPeriod(p) for p in periods]
    grid_periods: list[GridPeriod] = [GridPeriod(p, s) for p, s in ps.items()]
    for gp in tqdm(grid_periods):
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


if __name__ == "__main__":
    periods = [32]
    periods = [20, 26, 28, 30, 32, 34]
    periods: list[int] = [20, 25, 26, 28, 30, 32, 34,
                          35, 40, 45, 50, 60, 70,
                          80, 90, 100, 111, 125, 135, 143,]  # fmt: skip

    with open("src/txt/periods_series.json") as f:
        per_se_pairs = json.load(f)
    gmt_plot_all_periods(per_se_pairs)
    # gmt_plot_all_periods(periods)
