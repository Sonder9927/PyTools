from pathlib import Path

from src.pygmt_plot import gmt_plot_area


def main():
    txt = Path(r"src/txt")
    region = [115, 122.5, 27.9, 34.3]
    gmt_plot_area(region, txt / "per_evt_sta.csv")


if __name__ == "__main__":
    main()
