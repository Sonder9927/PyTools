from pathlib import Path

from icecream import ic

from src.info_filter import calc_lab, truncate_misfit, vel_info
from src.pygmt_plot import (
    gmt_plot_all_periods,
    gmt_plot_area,
    gmt_plot_dispersion_curves,
    gmt_plot_misfit,
    gmt_plot_vs,
)
from src.tpwt_show import PptMaker


def make_ppt(ppt_name, figs: Path, diff_info):
    ppt = PptMaker(pn=ppt_name, fig_root=figs, remake=True)
    ppt.add_area(r"area_figs")
    ppt.add_tpwt_results(r"tpwt_figs")
    ppt.add_diffs(r"diff_figs")
    ppt.add_dispersion_curves(r"dispersion_curves")
    ppt.add_mc_results(r"mc_figs")
    ppt.save()
    ic()


def main():
    """
    1. get hull points and statistic info of grid files
    2. plot [diff, vel, as, cb]
    3. plot dispersion curves from vel_info
    4. plot s-wave figs (need to collect data
       from all grids by `collect_grids`)
    5. make ppt to show results
    """
    fig_dirs = [
        "tpwt_figs",
        "mc_figs",
        "dispersion_curves",
        "diff_figs",
        "area_figs",
    ]
    fp = Path("images")
    for fd in fig_dirs:
        fpd = fp / fd
        if not fpd.exists():
            fpd.mkdir()

    txt = Path(r"src/txt")
    region = [115, 122.5, 27.9, 34.3]

    # gmt_plot_area(region, txt / "per_evt_sta.csv")
    # hull and info of all pers
    # vel_info(r"vel_info.json")

    # phase result
    gmt_plot_all_periods(
        txt / "periods_series.json",
        tpwt=True,
        checkboard=not True,
        std=not True,
        diff=not True,
    )
    # gmt_plot_dispersion_curves(r"src/txt/station.lst")

    # mc result
    mmf = txt / "misfit_moho.csv"
    # data = truncate_misfit(mmf, 0.5)
    # gmt_plot_misfit(mmf, region)
    mlf = txt / "moho_lab.csv"
    vsf = txt / "vs.csv"
    # calc_lab(vsf, mmf, mlf)
    # gmt_plot_vs(vsf, mlf)

    # make_ppt(
    #   ppt_name=r"target/tpwt.pptx", figs=Path(r"images"), diff_info=info_file
    # )


if __name__ == "__main__":
    main()
