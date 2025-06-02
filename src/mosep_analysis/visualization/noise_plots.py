from pandas import Series
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pointcloudset import PointCloud

from .utils_3d import plot_cube


def plot3d(pc1: PointCloud, pc2: PointCloud, exclude_dict: dict | None = None) -> go.Figure:
    fig = pc1.plot(
        hover_data=True,
        color="N",
        range_color=(0, 20),
        color_continuous_scale="Turbo",
        width=1000,
        height=800,
        overlay={"close": pc2},
    )
    fig.update_traces(marker={"size": 4}, opacity=0.7)
    camera = dict(eye=dict(x=0.001, y=0.0, z=2.5), projection=dict(type="orthographic"))
    fig.update_layout(
        template="ggplot2",
        # scene=dict(
        #     xaxis=dict(
        #         # nticks=8,
        #         range=[-1, 20],
        #     ),
        #     yaxis=dict(
        #         # nticks=8,
        #         range=[-20, 20],
        #     ),
        # ),
        # margin=dict(r=20, l=10, b=10, t=10),
        # scene_camera=camera,
    )

    # Add cubes where points are excluded
    for name, limits in exclude_dict.items():
        fig.add_trace(
            plot_cube(
                *limits.get_vertices_from_limits(),
                color="red",
                opacity=0.6,
                name=name,
            )
        )
    fig.layout.scene.aspectmode = "data"
    # fig.update_layout(hover)
    return fig


def temporal_development(
    nrpc: Series | None = None,
    nrpw: Series | None = None,
    rr_differ: Series | None = None,
    rr_int_h: Series | None = None,
) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    if rr_differ is not None:
        fig.add_trace(
            go.Bar(
                x=rr_differ.index,
                y=rr_differ,
                # mode="lines",
                name="Differential Precipitation (x 1000) [mm]",
                width=1000,
                marker=dict(color="#0290bf", line=dict(width=0)),
            )
        )
    if rr_int_h is not None:
        fig.add_trace(
            go.Scattergl(
                x=rr_int_h.index,
                y=rr_int_h,
                mode="lines",
                name="Precipitation Rate [mm/h]",
                line=dict(
                    color="#000080",
                    width=3,
                ),
            )
        )
    if nrpc is not None and nrpw is not None:
        fig.add_trace(
            go.Scatter(
                x=nrpw.index,
                y=nrpw + nrpc,
                mode="lines",
                name="Noise all",
                line=dict(color="#d5196e", width=3),
            ),
            secondary_y=True,
        )
    if nrpc is not None:
        fig.add_trace(
            go.Scatter(
                x=nrpc.index,
                y=nrpc,
                mode="lines",
                name="Noise 0-0.6m",
                line=dict(color="#9e00c0", width=2),
            ),
            secondary_y=True,
        )
    if nrpw is not None:
        fig.add_trace(
            go.Scatter(
                x=nrpw.index,
                y=nrpw,
                mode="lines",
                name="Noise >0.6m",
                line=dict(color="#fea626", width=2),
            ),
            secondary_y=True,
        )
    fig.update_layout(
        template="ggplot2",
        autosize=False,
        width=1000,
        height=500,
        title="Precipitation vs. Noise in Pointclouds",
        legend=dict(orientation="h", yanchor="bottom", y=1.0, xanchor="right", x=0.8),
        xaxis_title="",
        yaxis_title="Recorded Precipitation",
        yaxis2_title="Number of Points",
        font=dict(size=16),
    )
    fig.update_yaxes(title_font_color="#000080")
    fig.update_yaxes(title_font_color="#d5196e", secondary_y=True)

    return fig
