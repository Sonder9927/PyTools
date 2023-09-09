# from icecream import ic
import pandas as pd
import pygmt
from src import info_filter
# import xarray as xr

# from .gmt_make_data import gmt_blockmean_surface_grdsample


def vplane_makecpt(cmoho, clab, ctopo):
    # cmap = "src/txt/gridvel_6_v3.cpt"
    cmap = "seis"
    pygmt.makecpt(
        cmap=cmap,
        series=[2.8, 4.2, 0.01],
        output=cmoho,
        continuous=True,
        background=True,
    )
    pygmt.makecpt(
        cmap=cmap,
        series=[4, 5, 0.01],
        output=clab,
        continuous=True,
        background=True,
    )
    pygmt.makecpt(
        cmap="grayC",
        series=[-100, 2000, 200],
        continuous=True,
        output=ctopo,
    )


def vplane_clip_data(grid, boundary, region):
    # read grid data and cut
    data: pd.DataFrame = pygmt.grd2xyz(grid=grid)  # pyright: ignore
    bbot, bup = boundary.y.min(), boundary.y.max()
    data_um = data[data["y"] > bbot]
    data_up = data_um[data_um["y"] >= bup]
    data_mid = data_um[data_um["y"] < bup]
    # make clip boundary and cut
    # only calculate moho
    xs = region[:2]
    data_moho = _reset_clip(
        data_up, data_mid, boundary, [[x, region[-1]] for x in xs]
    )
    nys = [bbot, region[-1]]
    return pygmt.xyz2grd(data=data_moho, region=xs + nys, spacing=0.01)


def _reset_clip(og_data, clip_data, borigin, pnew):
    # make boundary
    df1 = pd.DataFrame([pnew[0]], columns=borigin.columns)
    df = pd.concat([df1, borigin], ignore_index=True)
    df2 = pd.DataFrame([pnew[1]], columns=borigin.columns)
    df = pd.concat([df, df2], ignore_index=True)
    # return data clipped
    clipped_data = info_filter.points_inner(clip_data, boundary=df.to_numpy())
    return pd.concat([og_data, clipped_data], ignore_index=True)
    # data = data.pivot(index="x", columns="y", values="z")
    # return xr.DataArray(data)
