from pathlib import Path


class GridPeriod:
    def __init__(self, period, series) -> None:
        self.period = period
        self.series = series
        self.region = [115, 122.5, 27.9, 34.3]

    def grid_tpwt(self):
        grid = Path(f"grids/tpwt_grids/tpwt_{self.period}")
        return grid if grid.exists() else None

    def grid_tpwt_cb(self):
        grid = Path(f"grids/tpwt_grids/tpwt_cb_{self.period}")
        return grid if grid.exists() else None

    def grid_tpwt_std(self):
        grid = Path(f"grids/tpwt_grids/tpwt_std_{self.period}")
        return grid if grid.exists() else None

    def grid_ant(self):
        grid = Path(f"grids/ant_grids/ant_{self.period}")
        return grid if grid.exists() else None

    def tpwt_vel_name(self):
        return f"images/tpwt_figs/tpwt_Vel_{self.period}.png"

    def tpwt_as_name(self):
        return f"images/tpwt_figs/tpwt_AS_{self.period}.png"

    def tpwt_cb_name(self):
        return f"images/tpwt_figs/tpwt_CB_{self.period}.png"

    def diff_name(self):
        return f"images/diff_figs/diff_{self.period}.png"
