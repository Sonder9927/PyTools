from src.info_filter import GridVplane

from .gmt import lines_generator, plot_vs_hplane, plot_vs_vplane


def gmt_plot_vs(vf, mlf, profile=False):
    # read vs data by vel file
    ave = True
    gv = GridVplane(vf, mlf)
    r = gv.hregion

    # hplane
    # for _, data, fn in gv.depths_data(
    #     ave=ave,
    #     dep_filter=lambda d: (d % 50 == 0) or (d % 10 == 0 and d >= -60),
    # ):
    #     plot_vs_hplane(data, r, fn, ave=ave)

    # vplane
    params = {"hregion": r}
    for linetype in ["xline", "yline", "raise", "decline"]:
        for idt, ll in lines_generator(r, linetype):
            path, fn = gv.init_path(ll, linetype)
            params |= zip(
                ["idt", "line", "path", "fname"], [idt, ll, path, fn]
            )
            params |= {"moho": gv.track_border("moho", path)}
            plot_vs_vplane(gv.track_vs(path), **params)
            plot_vs_vplane(gv.track_vs(path, ave), **params, ave=ave)
