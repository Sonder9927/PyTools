from pathlib import Path
from icecream import ic
from src import gmt


def gmt_plot_diff_all_periods(periods):
    for per in periods:
        # grid_tpwt: grid file generated by TPWT
        grid_tpwt = f"grids/tpwt_grids/tpwt_{per}"
        # grid_tpwt: grid file generated by ANT
        grid_ant = f"grids/ant_grids/ant_{per}"
        if not all([Path(f).exists() for f in [grid_tpwt, grid_ant]]):
            ic("Not found grid of PERIOD", per)
            continue

        region = [115, 122.5, 27.9, 34.3]

        fig_name = f"images/diff_{per}.png"
        gmt.plot_diff(grid_tpwt, grid_ant, region, fig_name)


def gmt_plot_Vel_all_periods(periods):
    for per in periods:
        # grid_tpwt: grid file generated by TPWT
        grid_tpwt = Path(f"grids/tpwt_grids/tpwt_{per}")
        if not Path(grid_tpwt).exists():
            ic("Not found grid of PERIOD", per)
            continue

        region = [115, 122.5, 27.9, 34.3]

        fig_name = f"images/tpwt_Vel_{per}.png"
        # gmt.plot_vel(grid_tpwt, region, fig_name)

if __name__ == "__main__":
    periods = [20]
    periods = [20, 26, 28, 30, 32, 34]

    gmt_plot_diff_all_periods(periods)

