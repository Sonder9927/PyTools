from .gmt import lines_generator, plot_vs_hpanel, plot_vs_vpanel


def gmt_plot_vs(gv, targets: dict):
    dps = targets.get("depths")
    dft = targets.get("dep_filter")
    if any([dps, dft is not None]):
        _vs_hpanel(gv, True, {"depths": dps, "dep_filter": dft})
    if lts := targets.get("linetypes"):
        if type(lts) is str:
            lts = [lts]
        _vs_vpanel(gv, lts)


def _vs_hpanel(gv, ave, dep):
    for _, grid, fn in gv.depths_data("tomo", ave, **dep):
        plot_vs_hpanel(grid, gv.hregion, fn, ave=ave)


def _vs_vpanel(gv, linetypes):
    ave = True
    params = {"hregion": gv.hregion}
    for linetype in linetypes:
        for idt, ll in lines_generator(gv.hregion, linetype):
            path, fn = gv.init_path(ll, linetype)
            params |= zip(
                ["idt", "line", "path", "fname"], [idt, ll, path, fn]
            )
            params |= {"moho": gv.track_border("moho", path)}
            plot_vs_vpanel(gv.track_vs(path), **params)
            plot_vs_vpanel(gv.track_vs(path, ave), **params, ave=ave)
