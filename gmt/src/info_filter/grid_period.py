from pathlib import Path


class GridPeriod:
    def __init__(self, period, series=None) -> None:
        self.period = period
        self.series = series
        self.region = [115, 122.5, 27.9, 34.3]

    def grid_file(self, method: str, identifier: str) -> Path | None:
        idt = check_identifier(identifier)
        gsp = Path("grids")
        grid = gsp / f"{method}_grids/{method}_{idt}_{self.period}.grid"
        return grid if grid.exists() else None

    def fig_tpwt_name(self, identifier: str) -> str:
        idt = check_identifier(identifier)
        return f"images/tpwt_figs/tpwt_{idt.upper()}_{self.period}.png"

    def diff_name(self):
        return f"images/diff_figs/diff_{self.period}.png"


def check_identifier(identifier: str) -> str:
    ids = {"vel", "cb", "std", "as"}
    if (idt := identifier.lower()) not in ids:
        raise KeyError(f"identifier: {identifier}")
    return idt
