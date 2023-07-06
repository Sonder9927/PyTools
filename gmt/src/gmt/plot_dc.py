import pygmt
import numpy as np


def plot_dc(ant, tpwt, fig_name) -> None:
    fig = pygmt.Figure()

    region = [0, 150, 2.9, 4.3]

    # gmt plot
    # define figure configuration
    pygmt.config(
        MAP_FRAME_TYPE="plain",
        MAP_TITLE_OFFSET="0.25p",
        MAP_DEGREE_SYMBOL="none",
        FONT_TITLE="18p,1,black",
        FONT_LABEL="8p,1,black",
    )

    fig.basemap(
        region=region,
        projection="X8c/4c",
        frame=["WeSn", r'xa20f5+l"Period (Sec)"', r'ya0.5f0.1+l"Vel (km/s)"'],
    )
    fig.plot(
        data=np.array(ant),
        # error_bar="Y",
        pen="0.8p,red",
    )
    # fig.plot(
    #     data=np.array(ant),
    #     style="s0.15c",
    #     # error_bar="Y",
    #     fill="red",
    # )
    fig.plot(
        data=np.array(tpwt),
        # error_bar="Y",
        pen="0.4p,blue",
    )

    fig.savefig(fig_name)
