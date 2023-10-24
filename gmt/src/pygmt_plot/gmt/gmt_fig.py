from .gmt_make_data import sta_clip


def fig_vel(fig, topos, vels, title, sta=None):
    """
    plot vel map
    """
    region = topos["region"]
    fig.basemap(
        projection=_hscale(region),
        region=region,
        frame=[f'WSne+t"{title}"', "xa2f2", "ya2f2"],
    )
    # fig.coast(resolution="l", land="white", area_thresh=10_000)
    # grdimage
    fig.grdimage(
        grid=topos["grd"], cmap=topos["cpt"], shading=topos["gra"]
    )  # cut vel_grd by the boundary of stations
    if sta is None:
        fig.grdimage(grid=vels["grd"], cmap=vels["cpt"], shading=topos["gra"])
    else:
        grd = sta_clip(vels["grd"], region, sta)
        fig.grdimage(
            grid=grd,
            cmap=vels["cpt"],
            shading=topos["gra"],
            nan_transparent=True,
        )
    return fig_tect_and_sta(fig, 0, sta)


def fig_vtomo(fig, tomos: list, cpts: list, region, borders: dict):
    fig.basemap(
        projection="X6i/2i",
        region=region,
        frame=["WSne", "xa2f2", "ya50f50"],
    )
    for t, c in zip(tomos, cpts):
        fig.grdimage(grid=t, cmap=c, nan_transparent=True)
    for bb in borders.values():
        fig.plot(data=bb, pen="1p,black,-")

    return fig


def fig_vtopo(fig, topo, region, title):
    v = int(region[-1] / 4)
    fig.plot(
        data=topo,
        projection="X6i/0.5i",
        region=region,
        frame=[f"sW+t{title}", f"ya{v}f{v}"],
        pen="4",
    )
    return fig


def fig_htopo(
    fig,
    topos,
    lines=None,
    line_pen="thick,black",
    scale=None,
    tect=0,
    sta=None,
):
    region = topos["region"]
    fig.basemap(
        # projection=_hscale(region),
        projection=scale or _hscale(region),
        region=region,
        frame=["WSne", "xa4f2", "ya4f2"],
    )
    fig.grdimage(grid=topos["grd"], cmap=topos["cpt"], shading=topos["gra"])
    if lines:
        for line in lines:
            fig.plot(data=line, pen=line_pen)
    fig = fig_tect_and_sta(fig, tect, sta)
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
    return fig_tect_and_sta(fig, 0, sta)


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

    fig = fig_tect_and_sta(fig, 0, sta)

    # colorbar
    fig.colorbar(
        cmap=cpt, position="jBC+w8c/0.4c+o0c/-1.5c+m", frame="xa30f30"
    )

    return fig


def fig_tect_and_sta(fig, tect, sta):
    # stations and China_tectonic
    # lines
    geo_data = ["China_tectonic.dat", "CN-faults.gmt"]
    fig.coast(shorelines="1/0.5p,black")
    fig.plot(data=f"src/txt/tects/{geo_data[tect]}", pen="thick,black,-")
    if sta is not None:
        fig.plot(data=sta, style="t0.1c", fill="blue", pen="black")
    return fig


def _hscale(region: list) -> str:
    # projection
    x = (region[0] + region[1]) / 2
    y = (region[2] + region[3]) / 2
    return f"m{x}/{y}/0.3i"
