def fig_vel(fig, topo_grd, vel_grd, region, scale, title, cpts, topo_gra, sta):
    fig.basemap(
        projection=scale,
        region=region,
        frame=[f'WSne+t"{title}"', "xa2f2", "ya2f2"]
    )  # fmt: skip

    fig.coast(shorelines="", resolution="l", land="white", area_thresh=10_000)
    # grdimage
    fig.grdimage(grid=topo_grd, cmap=cpts[0], shading=topo_gra)
    fig.grdimage(grid=vel_grd, cmap=cpts[1], shading=topo_gra)

    fig = fig_sta(fig, sta)
    return fig


def fig_tomo(fig, grid, region, scale, title, cpt, topo_gra, sta):
    """
    plot single fig of tpwt or ant
    """
    fig.basemap(
        projection=scale,
        region=region,
        frame=[f'WSne+t"{title}"', "xa2f2", "ya2f2"]
    )  # fmt: skip

    fig.coast(shorelines="", resolution="l", land="white", area_thresh=10_000)
    # grdimage
    fig.grdimage(
        grid=grid,
        cmap=cpt,
        shading=topo_gra,
    )

    fig = fig_sta(fig, sta)

    return fig


def fig_sta(fig, sta):
    # station
    fig.plot(
        data=sta,
        style="t0.1c",
        fill="blue",
        pen="black",
    )
    # fig.plot(data="ncc_lv.xy", pen="0.8p,black")
    fig.plot(data="src/txt/China_tectonic.dat", pen="thick,black,-")

    return fig