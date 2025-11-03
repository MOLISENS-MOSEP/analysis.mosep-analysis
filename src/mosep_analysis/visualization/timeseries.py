from moseplib.data.utils import get_pointcloud_from_timestamp
from mosep_analysis.data.config import TARGET_DISTANCES
from mosep_analysis.visualization.utils_2d import compress_legend as compress_legend_fu

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def plot_timeseries_separate_axes(df: pd.DataFrame, parameters: dict) -> None:
    # Move plot to module
    fig = go.Figure()

    # Add traces, each with a unique y-axis
    for i, (param, param_info) in enumerate(parameters.items(), start=1):
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df[param_info["data_key"]],
                mode="lines",
                name=param,
                line=dict(color=param_info["color"]),
                yaxis=f"y{i}",
            )
        )

    # Create axis objects
    layout_args = {}
    for i, (param, param_info) in enumerate(parameters.items(), start=1):
        if i == 1:
            layout_args[f"yaxis{i}"] = dict(
                title=dict(text=param_info["axis_title"], font=dict(color=param_info["color"])),
                tickfont=dict(color=param_info["color"]),
            )
        else:
            layout_args[f"yaxis{i}"] = dict(
                title=dict(text=param_info["axis_title"], font=dict(color=param_info["color"])),
                tickfont=dict(color=param_info["color"]),
                anchor="free",
                overlaying="y1",
                autoshift=True,
                tickmode="sync",
            )

    fig.update_layout(**layout_args)

    # Update layout properties
    fig.update_layout(
        width=1400,
        height=600,
    )

    fig.show()


def target_stat_vs_precipitation(
    target_df: pd.DataFrame,
    precipitation_se: pd.Series,
    value_name: str = "intensity",
    exclude_cols: list[str] | None = None,
    precipitation_name: str | None = None,
    yaxis_title: str | None = None,
    yaxis2_title: str | None = None,
    compress_legend: bool = False,
    fig_size: tuple[int, int] = (1000, 700),
):
    if precipitation_name is None:
        precipitation_name = precipitation_se.name

    if len(target_df.columns.names) == 1:
        color = target_df.columns.name
        dash = None
    else:
        color = target_df.columns.names[0]
        dash = target_df.columns.names[1]

    if exclude_cols:
        target_df = target_df.drop(columns=exclude_cols)
    target_df_melted = target_df.melt(value_name=value_name, ignore_index=False).reset_index()

    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # fig.add_trace(go.Scatter(x=w_differ.index, y=w_differ*200, mode='lines', name='differential precipitation', line=dict(color='red')))
    fig.add_traces(
        list(
            px.line(
                target_df_melted,
                x="index",
                y=value_name,
                color=color,
                line_dash=dash,
                line_group=dash,
            ).select_traces()
        )
    )

    # * Alternatively if plotly express reaches its limits use go.Scatter
    # colors = [
    #     "#1f77b4",  # muted blue
    #     "#ff7f0e",  # safety orange
    #     "#2ca02c",  # cooked asparagus green
    #     "#d62728",  # brick red
    #     "#9467bd",  # muted purple
    #     "#8c564b",  # chestnut brown
    # ]
    # dashes = {"white": None, "grey": "dash", "black": "dot"}

    # for plot_col, (target_name, dic) in zip(colors, target_df.items()):
    #     for col, rain_ds_minutes_mean_ds in dic.items():
    #         fig.add_trace(
    #             go.Scatter(
    #                 x=rain_ds_minutes_mean_ds.index,
    #                 y=rain_ds_minutes_mean_ds,
    #                 mode="lines",
    #                 name=target_name + col,
    #                 line=dict(color=plot_col, width=2, dash=dashes[col]),
    #             ),
    #             secondary_y=True,
    #         )

    fig.add_trace(
        go.Scattergl(
            x=precipitation_se.index,
            y=precipitation_se,
            mode="lines",
            name=precipitation_name,
            line=dict(color="#000080", width=3, shape="hv"),
        ),
        secondary_y=True,
    )

    fig.update_layout(
        template="ggplot2",
        autosize=False,
        width=fig_size[0],
        height=fig_size[1],
        # title="Rainfall Rate vs. Noise in Pointclouds",
        # legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1.0),
        xaxis_title="",
        yaxis_title=yaxis_title,
        yaxis2_title=yaxis2_title,
        font=dict(size=16),
    )
    fig.update_yaxes(title_font_color="#000000")
    fig.update_yaxes(title_font_color="#000080", secondary_y=True)

    if compress_legend:
        compress_legend_fu(fig, [precipitation_name])

    return fig


def histograms_targets_attime(pcs, weather_stats, timestamps, target_name, plot_value):
    pld = {}
    for ts in timestamps:
        pld[ts] = pd.concat(
            {col: get_pointcloud_from_timestamp(ds, ts).data for col, ds in pcs[target_name].items()},
            axis=0,
            names=["color", "ind_color"],
        )

    plot_data = pd.concat(pld, axis=0, names=["timestamp"]).reset_index()

    fig = px.line(
        weather_stats.precipitation.intensity_hour_shifted,
        line_shape="hv",
        height=200,
        labels={"value": "Rain Rate [mm/h]"},
    )
    # fig.add_hline(y=1, line_dash="dot", annotation_text="Jan 1, 2018 baseline", annotation_position="bottom right")
    for ts in timestamps:
        fig.add_vrect(
            x0=ts,
            x1=(pd.to_datetime(ts) + pd.Timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M:%S"),
            col=1,
            annotation_text=ts,
            annotation_position="top left",
            fillcolor="green",
            opacity=0.25,
            line_width=0,
        )
    fig.update_layout(
        xaxis_title=None,
        showlegend=False,
        margin=dict(
            l=80,  # left
            r=120,  # right
            t=10,  # top
            b=10,  # bottom
        ),
    )
    fig.show()

    fig = px.histogram(
        plot_data,
        x=plot_value,
        nbins=100,
        histnorm="percent",
        hover_data=plot_data.columns,
        color="color",
        marginal="box",
        title=f"Histogram(s) of target {target_name} (range: {TARGET_DISTANCES[target_name]} m) for `{plot_value}` value",
        facet_col="timestamp",
        facet_col_wrap=3,
        # height=800,
    )

    return fig


def histogram_targets_interactive(target_pcs: dict):
    import dash
    from dash import dcc, html
    from dash.dependencies import Input, Output

    app = dash.Dash(__name__)

    app.layout = html.Div(
        [
            dcc.Slider(
                id="timestamp-slider",
                min=0,
                max=len(target_pcs["Target-01"]["grey"]) - 1,
                value=0,
                marks={str(ts): str(ts) for ts in range(0, 60, 5)},
                step=1,
                updatemode="drag",  # Update the output as the slider is dragged
            ),
            dcc.Graph(id="intensity-histogram"),
        ]
    )

    @app.callback(Output("intensity-histogram", "figure"), [Input("timestamp-slider", "value")])
    def update_figure(selected_ts):
        plot_data = pd.concat(
            {col: ds[selected_ts].data for col, ds in target_pcs["Target-01"].items()}, axis=0, names=["color"]
        ).reset_index()

        traces = []
        for color in plot_data["color"].unique():
            df_filtered = plot_data[plot_data["color"] == color]
            traces.append(
                go.Histogram(x=df_filtered["intensity"], name=color, nbinsx=100, histnorm="percent", opacity=0.75)
            )

        figure = {
            "data": traces,
            "layout": go.Layout(
                title=f"Timestamp: {target_pcs['Target-01']['grey'].timestamps[selected_ts]}",
                xaxis={"title": "Intensity"},
                yaxis={"title": "Percent"},
                legend={"title": "Color"},
                barmode="overlay",
            ),
        }
        return figure

    return app
