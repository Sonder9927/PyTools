from icecream import ic
from pathlib import Path

from src.pygmt_plot import (
    gmt_plot_all_periods,
    gmt_plot_dispersion_curves,
    gmt_plot_misfit,
    gmt_plot_vs,
    # gmt_plot_vs_abso,
    # gmt_plot_vs_boundary,
    # gmt_plot_vs_compare,
)
from src.info_filter import vel_info, truncate_misfit
from src.tpwt_show import PptMaker


def make_ppt(ppt_name, figs: Path, diff_info):
    ppt = PptMaker(pn=ppt_name, fig_root=figs, remake=True)
    ppt.add_mc_results(r"mc_figs")
    ppt.add_dispersion_curves(r"dispersion_curves")
    ppt.add_diffs(r"diff_figs", info_file=diff_info)
    ppt.add_tpwt_results(r"twpt_figs")
    ppt.save()
    ic()


def main():
    """
    1. plot [diff, vel, as, cb]
    2. statistic info of grid files
    3. plot dispersion curves from vel_info
    4. plot s-wave figs (need to collect data
       from all grids by `collect_grids`)
    5. make ppt to show results
    """
    fig_dirs = ["tpwt_figs", "mc_figs", "dispersion_curves", "diff_figs"]
    fp = Path("images")
    for fd in fig_dirs:
        fpd = fp / fd
        if not fpd.exists():
            fpd.mkdir()

    txt = Path(r"src/txt")

    # # phase result
    gmt_plot_all_periods(r"src/txt/periods_series.json")
    # vel_info(r"vel_info.json")
    # gmt_plot_dispersion_curves(r"src/txt/station.lst")

    # mc result
    # gmt_plot_misfit(txt / "misfit_moho.csv")
    # data = truncate_misfit(txt / "misfit_moho.csv", 0.5)
    # gmt_plot_vs(txt / "vs.csv", txt / "misfit_moho.csv")

    # make_ppt(
    #   ppt_name=r"target/tpwt.pptx", figs=Path(r"images"), diff_info=info_file
    # )


if __name__ == "__main__":
    main()
