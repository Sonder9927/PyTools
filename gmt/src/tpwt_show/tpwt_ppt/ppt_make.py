from pathlib import Path

from pptx import Presentation

from .ppt_adds import (
    ppt_add_dcs,
    ppt_add_probs,
    ppt_add_diffs,
    ppt_add_one_fig_per_slide,
    ppt_add_single_type,
)


class PptMaker:
    def __init__(self, pn, fig_root: Path, remake=True) -> None:
        self.ppt_name = pn
        self.figs = fig_root
        self.margin = [0.789, 0.567]
        self.shape = {"h1": [7, 8.5], "dc": [6.8, 3.2], "prob": [7.2, 8.5]}
        # create a new instance for pptx
        self.prs = self._ppt(remake)

    def add_mc_results(self, mc_dir):
        mc = self.figs / mc_dir
        rc1 = {"rc_n": [2, 3], "rc_i": [0.382, 1]}
        # misfit
        self.prs = ppt_add_one_fig_per_slide(
            self.prs, mc, [3.456, 2.345], "misfit.png"
        )
        # probalCrs
        self.prs = ppt_add_probs(
            self.prs, mc / "prob", self.margin, self.shape["prob"]
        )
        # vs depth
        self.prs = ppt_add_single_type(
            self.prs,
            mc / "depth",
            rc1,
            self.margin,
            self.shape["h1"],
            "vs*",
            lambda p: int(p.stem.split("_")[-1][1:-4]),
        )
        # vs profile
        self.prs = ppt_add_one_fig_per_slide(
            self.prs, mc / "profile", self.margin, "vs*"
        )

    def add_dispersion_curves(self, dcs_dir):
        """
        add diff of all periods
        """
        self.prs = ppt_add_dcs(
            self.prs, self.figs / dcs_dir, self.margin, self.shape["dc"]
        )

    def add_diffs(self, diff_dir, info_file):
        """
        add diff of all periods
        """
        self.prs = ppt_add_diffs(
            self.prs, self.figs / diff_dir, info_file, self.margin
        )

    def add_tpwt_results(self, tpwt_dir):
        tpwt = self.figs / tpwt_dir
        # add phase vel of all periods
        key = lambda p: int(p.stem.split("_")[-1])
        rc1 = {"rc_n": [2, 3], "rc_i": [0.382, 1]}
        self.prs = ppt_add_single_type(
            self.prs,
            tpwt / "phv",
            rc1,
            self.margin,
            self.shape["h1"],
            "*VEL*",
            key,
        )
        rc2 = {"rc_n": [3, 2], "rc_i": [0.32, 1]}
        self.prs = ppt_add_single_type(
            self.prs,
            tpwt / "as",
            rc2,
            self.margin,
            [15, 8],
            "*AS*",
            key,
        )
        # add check board of all periods
        self.prs = ppt_add_single_type(
            self.prs,
            tpwt / "checkboard",
            rc1,
            self.margin,
            self.shape["h1"],
            "*CB*",
            key,
        )

    def save(self, target=None):
        """
        save ppt
        """
        pn = target or self.ppt_name
        self.prs.save(pn)

    def _ppt(self, remake):
        prs = Presentation() if remake else Presentation(self.ppt_name)
        # make first slide
        slide = prs.slides.add_slide(prs.slide_layouts[0])
        title = slide.shapes.title
        title.text = "Results Show"
        return prs
