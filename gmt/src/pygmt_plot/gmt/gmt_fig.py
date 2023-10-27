from .gmt_make_data import sta_clip


def fig_tomos(fig, topo, tomos, frame=None, **kwargs):
    if frame is None:
        frame = "a"
    tomo_param = {"nan_transparent": True}
    # basemap and topo
    fig.basemap(
        region=topo["region"],
        projection=kwargs.get("projection") or _hscale(topo["region"]),
        frame=frame,
    )
    if gra := topo.get("gra"):
        fig.grdimage(
            grid=topo["grd"],
            cmap=topo["cpt"],
            shading=gra,
        )
        tomo_param["shading"] = gra
    # plot tomos
    if kwargs.get("clip"):
        for tomo in tomos:
            tomo["grid"] = sta_clip(tomo["grid"], topo["region"])
            fig.grdimage(**tomo, **tomo_param)
    else:
        for tomo in tomos:
            fig.grdimage(**tomo, **tomo_param)
    # plot tects and stas
    if (tect := kwargs.get("tect")) is not None:
        fig = fig_tect_and_sta(fig, tect, kwargs.get("sta"))
    # plot lines
    if lines := kwargs.get("lines"):
        for line in lines:
            fig.plot(data=line, pen=kwargs["line_pen"])
    return fig


def fig_tect_and_sta(fig, tect, sta):
    # stations and China_tectonic
    # lines
    geo_data = ["China_tectonic.dat", "CN-faults.gmt", "find.gmt"]
    fig.coast(shorelines="1/0.5p,black")
    fig.plot(data=f"src/txt/tects/{geo_data[tect]}", pen="1.5p,black,-")
    fig.plot(data="src/txt/tects/small_faults.gmt", pen="0.9p,black,-")
    # fig.plot(data="src/txt/tects/small_faults_finding.gmt", pen="red,-")
    if sta is not None:
        fig.plot(data=sta, style="t0.1c", fill="darkblue")
    return fig


def _hscale(region: list) -> str:
    # projection
    x = (region[0] + region[1]) / 2
    y = (region[2] + region[3]) / 2
    return f"m{x}/{y}/0.3i"
