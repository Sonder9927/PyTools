from pathlib import Path

from icecream import ic
import pandas as pd

from .info_filter import GridVs, area_hull_files, calc_lab
from .pygmt_plot import (
    AreaPainter,
    PhasePainter,
    gmt_plot_all_periods,
    gmt_plot_dispersion_curves,
    gmt_plot_misfit,
    gmt_plot_vs,
)
from .tpwt_show import PptMaker


class Painter:
    def __init__(self, init=False) -> None:
        self.images = Path("images")
        self.region = [115, 122.5, 27.9, 34.3]
        self.txt = Path("src/txt")
        self.vsf = self.txt / "vs.csv"
        self.mmf = self.txt / "misfit_moho.csv"
        self.mlf = self.txt / "moho_lab.csv"
        self.ap = AreaPainter(self.region, self.txt / "per_evt_sta.csv")
        self.php = PhasePainter(self.region, self.txt / "periods_series.json")
        if init:
            self._init()

    # def area(self):
    #     self._mkdir("area_figs")
    def area(self, *args):
        self._mkdir("area_figs")
        for tt in args:
            if tt == "area":
                self.ap.area_map()
            elif tt == "per_evt":
                self.ap.per_evt()
            elif tt == "sites":
                self.ap.sites()
            elif tt == "rays":
                self.ap.rays()
            else:
                raise NotImplementedError

    def phase(self, idt="vel", method="tpwt", *, periods=None, dcheck=2.0):
        self._mkdir("ant_figs", "tpwt_figs")
        if idt == "vel":
            self.php.vel(method, idt, periods=periods)
        elif idt == "cb":
            self.php.vel(method, idt, periods=periods, dcheck=dcheck)
        elif idt == "std":
            self.php.std(periods)
        elif idt == "diff":
            self.php.diff(periods)
        else:
            raise NotImplementedError

    # def phv(self, *targets, dcheck=2.0):
    #     self._mkdir("ant_figs")
    #     self._mkdir("tpwt_figs")
    # ts = {t: True for t in targets}
    # gmt_plot_all_periods(self.region, psjf, dcheck, **ts)

    def dispersion(self):
        self._mkdir("dispersion_curves")
        gmt_plot_dispersion_curves(self.mmf)

    def mcmc(self, *, misfit=False, **kwargs):
        self._mkdir("mc_figs/depth", "mc_figs/profile")
        # plot misfit
        if misfit:
            gmt_plot_misfit(self.mmf, self.region)
        gv = GridVs(self.region, self.vsf, self.mlf)
        # plot vs panels
        gmt_plot_vs(gv, kwargs)

    def _init(self, misfit_limit=0.5):
        # notice: `self.*f` will be made by this class
        # filter grid where misfit > limit
        mm = pd.read_csv(self.mmf)
        misfit = mm[["x", "y", "misfit"]]
        misfit_limit = misfit[misfit["misfit"] > misfit_limit]
        ic(misfit_limit)
        moho_range = mm["moho"].min(), mm["moho"].max()
        ic(moho_range)
        # make misfit lab file
        vs = pd.read_csv(self.vsf)
        vs_mantle = vs[vs["z"] < -moho_range[1]]
        vs_ave = vs_mantle["v"].mean()
        ic(vs_ave)
        calc_lab(vs, mm, self.mlf)
        # make hull of stas in the area
        area_hull_files(self.region, txt=self.txt)

    def _mkdir(self, *args):
        for target in args:
            if not (tt := self.images / target).exists():
                tt.mkdir(parents=True)


def make_ppt(ppt_name, figs: Path):
    ppt = PptMaker(pn=ppt_name, fig_root=figs, remake=True)
    ppt.add_area(r"area_figs")
    ppt.add_phase_results(r"phase")
    ppt.add_dispersion_curves(r"dispersion_curves")
    ppt.add_mc_results(r"mc_figs")
    ppt.save()
    ic()
