from .gmt_make_data import sta_clip


def fig_vel(fig, topo_grd, vel_grd, region, title, cpts, gra, sta=None):
    """
    plot vel map
    """
    fig.basemap(
        projection=_hscale(region),
        region=region,
        frame=[f'WSne+t"{title}"', "xa2f2", "ya2f2"],
    )
    # fig.coast(resolution="l", land="white", area_thresh=10_000)
    # grdimage
    fig.grdimage(grid=topo_grd, cmap=cpts[0], shading=gra)
    # cut vel_grd by the boundary of stations
    if sta is None:
        fig.grdimage(grid=vel_grd, cmap=cpts[1], shading=gra)
    else:
        grd = sta_clip(vel_grd, region, sta)
        fig.grdimage(grid=grd, cmap=cpts[1], shading=gra, nan_transparent=True)
    return fig_lines_and_sta(fig, sta)


def fig_vtomo(fig, tomos: list, cpts: list, *, moho, region):
    fig.basemap(
        projection="X6i/2i",
        region=region,
        frame=["WSne", "xa2f2", "ya50f50"],
    )
    for t, c in zip(tomos, cpts):
        fig.grdimage(grid=t, cmap=c, nan_transparent=True)
    fig.plot(data=moho, pen="1p,black,-")

    return fig


def fig_vtopo(fig, topo, region, title):
    fig.plot(
        data=topo,
        projection="X6i/0.5i",
        region=region,
        frame=[f"sW+t{title}", "ya3000f3000"],
        pen="4",
    )
    return fig


def fig_htopo(fig, grd, cmap, region, gra, line):
    fig.basemap(
        projection=_hscale(region),
        region=region,
        frame=["WSne", "xa4f2", "ya4f2"],
    )
    fig.grdimage(grid=grd, cmap=cmap, shading=gra)
    fig = fig_lines_and_sta(fig)
    fig.plot(data=line, pen="fat,red")
    return fig


def fig_htomo(fig, grid, region, title, cpt, topo_gra, sta=None):
    """
    plot subfig of tpwt or ant in diff map
    """
    fig.basemap(
        projection=_hscale(region),
        region=region,
        frame=[f'WSne+t"{title}"', "xa2f2", "ya2f2"],
    )
    fig.coast(resolution="l", land="white", area_thresh=10_000)
    # grdimage
    fig.grdimage(grid=grid, cmap=cpt, shading=topo_gra, nan_transparent=True)
    return fig_lines_and_sta(fig, sta)


def fig_diff(fig, diff, region, title, cpt, topo_gra, sta):
    fig.coast(
        region=region,
        projection=_hscale(region),
        frame=[f"WSne+t{title}", "xa2f2", "ya2f2"],
        resolution="l",
        land="white",
        area_thresh=10_000,
    )

    # cut vel_diff_grd by the boundary of stations
    diff = sta_clip(diff, region, sta)
    fig.grdimage(grid=diff, cmap=cpt, shading=topo_gra, nan_transparent=True)

    fig = fig_lines_and_sta(fig, sta)

    # colorbar
    fig.colorbar(
        cmap=cpt, position="jBC+w8c/0.4c+o0c/-1.5c+m", frame="xa30f30"
    )

    return fig


def fig_lines_and_sta(fig, sta=None):
    # stations and China_tectonic
    # lines
    fig.coast(shorelines="1/0.5p,black")
    # fig.plot(data="ncc_lv.xy", pen="0.8p,black")
    fig.plot(data="src/txt/China_tectonic.dat", pen="thick,black,-")
    if sta is None:
        return fig
    fig.plot(data=sta, style="t0.1c", fill="blue", pen="black")
    return fig


def _hscale(region: list) -> str:
    # projection
    x = (region[0] + region[1]) / 2
    y = (region[2] + region[3]) / 2
    return f"m{x}/{y}/0.3i"
