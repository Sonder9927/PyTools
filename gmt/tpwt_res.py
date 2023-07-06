from icecream import ic
from pathlib import Path
from tpwt_show import PptMaker

from src.pygmt_plot import gmt_plot_all_periods, gmt_plot_dispersion_curves
from src.info_filter import vel_info


def make_ppt(ppt_name, figs: Path, diff_info):
    ppt = PptMaker(pn=ppt_name, fig_root=figs, remake=True)
    ppt.add_diffs(r"diff_figs", info_file=diff_info)
    ppt.add_vels(r"tpwt_figs")
    ppt.add_CBs(r"tpwt_figs")
    ppt.save()
    ic()


def main():
    """
    1. plot [diff, vel, as, cb]
    2. statistic info of grid files
    3. plot dispersion curves from vel_info
    4. make ppt to show results
    """
    gmt_plot_all_periods(r"src/txt/periods_series.json")

    periods = [20, 26, 28, 30, 32, 34]
    periods = []
    info_file = r"vel_info.json"
    vel_info(info_file)  # , periods)

    gmt_plot_dispersion_curves(info_file)

    make_ppt(
        ppt_name=r"target/tpwt.pptx", figs=Path(r"images"), diff_info=info_file
    )


if __name__ == "__main__":
    main()
