from src.info_filter import GridVplane

from .gmt import plot_vs_vplane


def gmt_plot_vs(vf, mmf):
    # read vs data by vel file
    gv = GridVplane(vf, mmf)
    r = gv.hregion
    # lon
    ys = [28, 30, 32, 34]
    hlines = [[[r[0], y], [r[1], y]] for y in ys]
    # for ll in hlines:
    #     path, fn = gv.init_path(*ll)
    #     data = gv.track_vs(path)
    #     moho = gv.track_moho(path)
    #     # plot vplane with coord `x` and `z`
    #     plot_vs_vplane(
    #         data,
    #         "x",
    #         moho=moho,
    #         line=ll,
    #         path=path,
    #         hregion=r,
    #         fname=fn,
    #     )
    # lat
    xs = [116, 118, 120, 122]
    vlines = [[[x, r[2]], [x, r[3]]] for x in xs]
    for ll in vlines:
        path, fn = gv.init_path(*ll)
        data = gv.track_vs(path)
        moho = gv.track_moho(path)
        # plot vplane with coord `y` and `z`
        plot_vs_vplane(
            data,
            "y",
            moho=moho,
            line=ll,
            path=path,
            hregion=r,
            fname=fn,
        )
