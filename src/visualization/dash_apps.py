# dash_app.py

import pandas as pd
import plotly.graph_objs as go
from jupyter_dash import JupyterDash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State


def run_dash_3d_selection(df: pd.DataFrame, c_column="intensity", color_range=None) -> None:
    """Run a Dash app to display a 3D scatter plot and show statistics for selected points.

    Created with the help of ChatGPT 4o:
    https://chat.openai.com/share/ffd8391c-d20a-4590-a531-51e0deb621a1

    Args:
        df (pd.DataFrame): A DataFrame containing at least the columns "x", "y", "z".
        c_column (str, optional): The column to use for the marker color. Defaults to "intensity".
        color_range (tuple, optional): Min and Max value of color scale. Defaults to None.
    """

    if c_column:
        color = df[c_column]
    else:
        color = "blue"

    if color_range:
        cmin, cmax = color_range
    else:
        cmin, cmax = None, None

    camera = dict(eye=dict(x=0, y=-1, z=2.5), projection=dict(type="orthographic"))

    # Initialize the JupyterDash app
    app = JupyterDash(__name__)

    # Create the 3D scatter plot
    scatter3d = go.Figure(
        data=[
            go.Scatter3d(
                x=df["x"],
                y=df["y"],
                z=df["z"],
                mode="markers",
                marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
            )
        ],
        layout=go.Layout(
            title="3D Scatter Plot",
            margin=dict(l=50, r=50, b=50, t=50),
            scene=dict(aspectmode="data", camera=camera, yaxis=dict(autorange="reversed")),
        ),
    )

    # Create the 2D scatter plot (top-down view, x-y plane)
    scatter2d_xy = go.Figure(
        data=[
            go.Scatter(
                x=df["x"],
                y=df["y"],
                mode="markers",
                marker=dict(size=5),
                selected=dict(marker=dict(color="red", size=10)),
            )
        ],
        layout=go.Layout(
            title="2D Scatter Plot (Top-Down View, x-y)",
            margin=dict(l=50, r=50, b=50, t=50),
            yaxis=dict(autorange="reversed"),
            dragmode="select",
        ),
    )

    # Create the 2D scatter plot (side view, x-z plane)
    scatter2d_xz = go.Figure(
        data=[
            go.Scatter(
                x=df["x"],
                y=df["z"],
                mode="markers",
                marker=dict(size=5),
                selected=dict(marker=dict(color="red", size=10)),
            )
        ],
        layout=go.Layout(
            title="2D Scatter Plot (Side View, x-z)", margin=dict(l=50, r=50, b=50, t=50), dragmode="select"
        ),
    )

    # Define the layout of the app
    app.layout = html.Div(
        [
            dcc.Graph(id="3d-scatter-plot", figure=scatter3d, style={"height": "600px"}),
            dcc.Graph(id="2d-scatter-plot-xy", figure=scatter2d_xy, style={"height": "400px"}),
            dcc.Graph(id="2d-scatter-plot-xz", figure=scatter2d_xz, style={"height": "400px"}),
            html.Div(id="stats-table"),
        ]
    )

    # Callback to update the 3D plot and 2D projections based on selections
    @app.callback(
        [
            Output("3d-scatter-plot", "figure"),
            Output("2d-scatter-plot-xy", "figure"),
            Output("2d-scatter-plot-xz", "figure"),
            Output("stats-table", "children"),
        ],
        [Input("2d-scatter-plot-xy", "selectedData"), Input("2d-scatter-plot-xz", "selectedData")],
        [
            State("3d-scatter-plot", "figure"),
            State("2d-scatter-plot-xy", "figure"),
            State("2d-scatter-plot-xz", "figure"),
        ],
    )
    def update_plots(selectedDataXY, selectedDataXZ, fig3d, fig2dxy, fig2dxz):
        selected_indices_xy = set()
        if selectedDataXY:
            selected_indices_xy.update([point["pointIndex"] for point in selectedDataXY["points"]])

        selected_indices_xz = set()
        if selectedDataXZ:
            selected_indices_xz.update([point["pointIndex"] for point in selectedDataXZ["points"]])

        # Intersection of selected indices in both views
        selected_indices = list(selected_indices_xy.intersection(selected_indices_xz))

        # Debug print statements
        # print("Selected indices from XY projection:", selected_indices_xy)
        # print("Selected indices from XZ projection:", selected_indices_xz)
        # print("Intersection of selected indices:", selected_indices)

        if not selected_indices:
            # If no points are selected in both projections, return the original figures without highlighting
            scatter3d_clean = go.Figure(
                data=[
                    go.Scatter3d(
                        x=df["x"],
                        y=df["y"],
                        z=df["z"],
                        mode="markers",
                        marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
                    )
                ],
                layout=fig3d["layout"],
            )

            scatter2d_xy_clean = go.Figure(
                data=[
                    go.Scatter(
                        x=df["x"],
                        y=df["y"],
                        mode="markers",
                        marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
                        selected=dict(marker=dict(color="red", size=10)),
                    )
                ],
                layout=fig2dxy["layout"],
            )

            scatter2d_xz_clean = go.Figure(
                data=[
                    go.Scatter(
                        x=df["x"],
                        y=df["z"],
                        mode="markers",
                        marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
                        selected=dict(marker=dict(color="red", size=10)),
                    )
                ],
                layout=fig2dxz["layout"],
            )

            return (
                scatter3d_clean,
                scatter2d_xy_clean,
                scatter2d_xz_clean,
                html.Div("Select points in the 2D plots to see statistics"),
            )

        selected_df = df.iloc[selected_indices]

        # Update the 3D scatter plot with highlighted points
        scatter3d_updated = go.Figure(
            data=[
                go.Scatter3d(
                    x=df["x"],
                    y=df["y"],
                    z=df["z"],
                    mode="markers",
                    marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
                ),
                go.Scatter3d(
                    x=selected_df["x"],
                    y=selected_df["y"],
                    z=selected_df["z"],
                    mode="markers",
                    marker=dict(size=5, color="red"),
                ),
            ],
            layout=fig3d["layout"],
        )

        # Update the top-down 2D scatter plot with highlighted points
        scatter2d_xy_updated = go.Figure(
            data=[
                go.Scatter(
                    x=df["x"],
                    y=df["y"],
                    mode="markers",
                    marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
                    selected=dict(marker=dict(color="red", size=10)),
                ),
                go.Scatter(x=selected_df["x"], y=selected_df["y"], mode="markers", marker=dict(size=5, color="red")),
            ],
            layout=fig2dxy["layout"],
        )

        # Update the side view 2D scatter plot with highlighted points
        scatter2d_xz_updated = go.Figure(
            data=[
                go.Scatter(
                    x=df["x"],
                    y=df["z"],
                    mode="markers",
                    marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
                    selected=dict(marker=dict(color="red", size=10)),
                ),
                go.Scatter(x=selected_df["x"], y=selected_df["z"], mode="markers", marker=dict(size=5, color="red")),
            ],
            layout=fig2dxz["layout"],
        )

        # Compute and return statistics for the selected points
        stats = selected_df.describe().transpose()[["min", "max", "count"]]
        return (
            scatter3d_updated,
            scatter2d_xy_updated,
            scatter2d_xz_updated,
            dash_table.DataTable(
                data=stats.reset_index().to_dict("records"),
                columns=[{"name": i, "id": i} for i in stats.reset_index().columns],
            ),
        )

    # Run the app in Jupyter notebook
    app.run_server(mode="external", debug=True)
