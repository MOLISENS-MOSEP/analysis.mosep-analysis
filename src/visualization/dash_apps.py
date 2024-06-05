# dash_app.py

import pandas as pd
import plotly.graph_objs as go
import dash
# from jupyter_dash import JupyterDash
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
    # app = JupyterDash(__name__)
    app = dash.Dash(__name__, serve_locally=False)

    # Create hover text for 3D scatter plot
    hover_text = df.apply(
        lambda row: f"x: {row['x']}<br>y: {row['y']}<br>z: {row['z']}<br>intensity: {row['intensity']}"
        if "intensity" in df.columns
        else f"x: {row['x']}<br>y: {row['y']}<br>z: {row['z']}",
        axis=1,
    )

    # Create the 3D scatter plot
    scatter3d = go.Figure(
        data=[
            go.Scatter3d(
                x=df["x"],
                y=df["y"],
                z=df["z"],
                mode="markers",
                marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
                hovertemplate=hover_text,
            )
        ],
        layout=go.Layout(
            title="3D Scatter Plot",
            margin=dict(l=50, r=50, b=50, t=50),
            scene=dict(aspectmode="data", camera=camera),
        ),
    )

    # Create the 2D scatter plot (top-down view, x-y plane)
    scatter2d_xy = go.Figure(
        data=[
            go.Scatter(
                x=df["x"],
                y=df["y"],
                mode="markers",
                marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
                selected=dict(marker=dict(color="red", size=10)),
                hovertemplate=hover_text,
            )
        ],
        layout=go.Layout(
            title="2D Scatter Plot (Top-Down View, x-y)",
            margin=dict(l=50, r=50, b=50, t=50),
            dragmode="select",
            xaxis=dict(scaleanchor="y", scaleratio=1),
            yaxis=dict(scaleanchor="x", scaleratio=1),
        ),
    )

    # Create the 2D scatter plot (side view, x-z plane)
    scatter2d_xz = go.Figure(
        data=[
            go.Scatter(
                x=df["x"],
                y=df["z"],
                mode="markers",
                marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
                selected=dict(marker=dict(color="red", size=10)),
                hovertemplate=hover_text,
            )
        ],
        layout=go.Layout(
            title="2D Scatter Plot (Side View, x-z)",
            margin=dict(l=50, r=50, b=50, t=50),
            dragmode="select",
            xaxis=dict(scaleanchor="y", scaleratio=1),
            yaxis=dict(scaleanchor="x", scaleratio=1),
        ),
    )

    # Define the layout of the app
    app.layout = dash.html.Div(
        [
            dash.dcc.Graph(id="3d-scatter-plot", figure=scatter3d, style={"height": "600px"}),
            dash.dcc.Graph(
                id="2d-scatter-plot-xy", figure=scatter2d_xy, style={"height": "400px"}, config={"scrollZoom": True}
            ),
            dash.dcc.Graph(
                id="2d-scatter-plot-xz", figure=scatter2d_xz, style={"height": "400px"}, config={"scrollZoom": True}
            ),
            dash.html.Div(id="stats-table"),
        ]
    )

    # Callback to update the 3D plot and 2D projections based on selections
    @app.callback(
        Output("2d-scatter-plot-xy", "figure"),
        [Input("2d-scatter-plot-xy", "selectedData")],
        [State("2d-scatter-plot-xy", "figure")],
    )
    def update_2d_xy(selectedDataXY, fig2dxy):
        selected_indices_xy = set()
        if selectedDataXY and "points" in selectedDataXY:
            selected_indices_xy = {point["pointIndex"] for point in selectedDataXY["points"]}

        print("Selected indices from XY projection:", selected_indices_xy)
        return fig2dxy

    @app.callback(
        Output("2d-scatter-plot-xz", "figure"),
        [Input("2d-scatter-plot-xz", "selectedData")],
        [State("2d-scatter-plot-xz", "figure")],
    )
    def update_2d_xz(selectedDataXZ, fig2dxz):
        selected_indices_xz = set()
        if selectedDataXZ and "points" in selectedDataXZ:
            selected_indices_xz = {point["pointIndex"] for point in selectedDataXZ["points"]}

        print("Selected indices from XZ projection:", selected_indices_xz)
        return fig2dxz

    @app.callback(
        [
            Output("3d-scatter-plot", "figure"),
            Output("stats-table", "children"),
        ],
        [Input("2d-scatter-plot-xy", "selectedData"), Input("2d-scatter-plot-xz", "selectedData")],
        [
            State("3d-scatter-plot", "relayoutData"),
            State("3d-scatter-plot", "figure"),
        ],
    )
    def update_3d(selectedDataXY, selectedDataXZ, relayoutData3d, fig3d):
        selected_indices_xy = set()
        selected_indices_xz = set()

        if selectedDataXY and "points" in selectedDataXY:
            selected_indices_xy = {point["pointIndex"] for point in selectedDataXY["points"]}

        if selectedDataXZ and "points" in selectedDataXZ:
            selected_indices_xz = {point["pointIndex"] for point in selectedDataXZ["points"]}

        selected_indices = list(selected_indices_xy.intersection(selected_indices_xz))

        print("Intersection of selected indices:", selected_indices)

        if relayoutData3d and "scene.camera" in relayoutData3d:
            camera_settings = relayoutData3d["scene.camera"]
        else:
            camera_settings = fig3d["layout"]["scene"]["camera"]

        if not selected_indices:
            scatter3d_clean = go.Figure(
                data=[
                    go.Scatter3d(
                        x=df["x"],
                        y=df["y"],
                        z=df["z"],
                        mode="markers",
                        marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
                        hovertemplate=hover_text,
                    )
                ],
                layout=fig3d["layout"],
            )
            scatter3d_clean.update_layout(scene_camera=camera_settings)
            return scatter3d_clean, dash.html.Div("Select points in the 2D plots to see statistics")

        selected_df = df.iloc[selected_indices]
        updated_hover_text = selected_df.apply(
            lambda row: f"x: {row['x']}<br>y: {row['y']}<br>z: {row['z']}<br>intensity: {row['intensity']}"
            if "intensity" in df.columns
            else f"x: {row['x']}<br>y: {row['y']}<br>z: {row['z']}",
            axis=1,
        )

        scatter3d_updated = go.Figure(
            data=[
                go.Scatter3d(
                    x=df["x"],
                    y=df["y"],
                    z=df["z"],
                    mode="markers",
                    marker=dict(size=5, color=color, cmin=cmin, cmax=cmax, colorscale="Plasma"),
                    hovertemplate=hover_text,
                ),
                go.Scatter3d(
                    x=selected_df["x"],
                    y=selected_df["y"],
                    z=selected_df["z"],
                    mode="markers",
                    marker=dict(size=5, color="red"),
                    hovertemplate=updated_hover_text,
                ),
            ],
            layout=fig3d["layout"],
        )
        scatter3d_updated.update_layout(scene_camera=camera_settings)

        stats = selected_df.describe().transpose()[["min", "max", "mean", "count"]]
        return (
            scatter3d_updated,
            dash.dash_table.DataTable(
                data=stats.reset_index().to_dict("records"),
                columns=[{"name": i, "id": i} for i in stats.reset_index().columns],
            ),
        )

    # Run the app in Jupyter notebook
    return app
    # app.run_server(mode="external", debug=True)

