from src.info_filter import GridVplane
from icecream import ic

from .gmt import plot_vs_vplane, plot_vs_hplane


def gmt_plot_vs(vf, mmf):
    # read vs data by vel file
    ave = True
    gv = GridVplane(vf, mmf)
    r = gv.hregion
    # hplane
    for _, data, fn in gv.depths_data(
        ave=ave,
        dep_filter=lambda d: (d % 30 == 0) or (d % 10 == 0 and d <= 60),
    ):
        plot_vs_hplane(data, r, fn, ave=ave)
    return

    # vplane
    params = {"hregion": r}
    for idt, ll in lines_generator(r):
        path, fn = gv.init_path(*ll)
        params |= zip(["idt", "line", "path", "fname"], [idt, ll, path, fn])
        params["moho"] = gv.track_moho(path)
        plot_vs_vplane(gv.track_vs(path), **params)
        plot_vs_vplane(gv.track_vs(path, ave), **params, ave=ave)
        return


def lines_generator(region):
    ys = [28, 30, 32, 34]
    hlines = [[[region[0], y], [region[1], y]] for y in ys]
    xs = [116, 118, 120, 122]
    vlines = [[[x, region[2]], [x, region[3]]] for x in xs]
    for idt, lls in zip(["x", "y"], [hlines, vlines]):
        for ll in lls:
            yield idt, ll
