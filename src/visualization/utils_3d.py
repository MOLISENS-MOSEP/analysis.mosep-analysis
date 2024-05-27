import numpy as np
import plotly.graph_objects as go
import panel as pn


def plot_cube(x_coords, y_coords, z_coords, color="red", opacity=0.6) -> go.Figure:
    """Plot a go.Mesh3d object representing a cube."""

    return go.Mesh3d(
        # 8 vertices of a cube
        x=x_coords,
        y=y_coords,
        z=z_coords,
        # Should be the same for every cube.
        # i, j and k give the vertices of triangles
        i=[7, 0, 0, 0, 4, 4, 6, 6, 4, 0, 3, 2],
        j=[3, 4, 1, 2, 5, 6, 5, 2, 0, 1, 6, 3],
        k=[0, 7, 2, 3, 6, 7, 1, 1, 5, 5, 7, 6],
        opacity=opacity,
        color=color,
        flatshading=True,
        # Beautiful color but unnecessary.
        # colorscale=[[0, "gold"], [0.5, "mediumturquoise"], [1, "magenta"]],
        # intensity=np.linspace(0, 1, 12, endpoint=True),
        # intensitymode="cell",
        # showscale=False,
    )


def ms(x, y, z, radius, resolution=40):
    """Return the coordinates for plotting a sphere centered at (x,y,z)"""
    u, v = np.mgrid[0 : 2 * np.pi : resolution * 2j, 0 : np.pi : resolution * 1j]
    X = radius * np.cos(u) * np.sin(v) + x
    Y = radius * np.sin(u) * np.sin(v) + y
    Z = radius * np.cos(v) + z
    return (X, Y, Z)


def plot_sphere_interactive(fig, sphere_origin=(0, 0, 0)):
    """
    Plot an interactive 3D sphere on a Plotly figure.

    Args:
        fig (plotly.graph_objs.Figure): The Plotly figure to add the sphere to.
        sphere_origin (tuple of float, optional): The (x, y, z) coordinates of the center of the sphere.
            Defaults to (0, 0, 0).

    Returns:
        pn.Column: A Panel column containing a float input widget and a Plotly pane.

    Notes:
        This function uses the `ms` function to generate the x, y, and z coordinates of the sphere.
        The `float_input` widget controls the radius of the sphere.
    """
    float_input = pn.widgets.FloatInput(name="FloatInput", value=1.0, step=1e-1, start=1, end=60)

    x_pns_surface, y_pns_surface, z_pns_suraface = ms(*sphere_origin, float_input.value)
    surface_trace = go.Surface(x=x_pns_surface, y=y_pns_surface, z=z_pns_suraface, opacity=0.2, hoverinfo="skip")
    fig.add_trace(surface_trace)

    def update_trace(event):
        x_pns_surface, y_pns_surface, z_pns_surface = ms(*sphere_origin, float_input.value)
        surface_trace.x = x_pns_surface
        surface_trace.y = y_pns_surface
        # surface_trace.z = z_pns_surface
        # For some reason updating the figure directly does not work. As a work
        # around we set the last trace to invisible and add a new trace.
        fig.data[-1].visible = False
        fig.add_trace(surface_trace)

    plotly_pane = pn.pane.Plotly(fig)
    float_input.param.watch(update_trace, "value")

    return pn.Column("# Title", float_input, plotly_pane)


if __name__ == "__main__":
    fig = go.Figure(data=[plot_cube()])
    fig.show()

if __name__.startswith("bokeh"):
    from src.data import pointcloud_processing
    from src.data.config import TARGET_EXTENTS
    import warnings

    pn.extension("plotly")

    BAG_NAME = "molisens_met_2023_04_14-09_23_34_converted"
    DATA_DIR = "/workspaces/MOLISENSext_analysis/data/2interim/bad_aussee/data"

    dataset = pointcloud_processing.load_pointcloudset(
        DATA_DIR,
        BAG_NAME,
        topic="/sensing/lidar/points",
        verbose=True,
    )
    pc = dataset[100].limit("y", -50, 50).limit("x", -10, 40)

    # Catch runtime warnings from apply_limits
    with warnings.catch_warnings(record=True):
        targets_limited = [target.apply_limits(pc) for target in TARGET_EXTENTS]

    target_pcs = {f"Target {i}": c for i, c in enumerate(targets_limited) if len(c) > 0}

    pc_fig = pc.plot(
        color="z",
        overlay=target_pcs,
        hover_data=True,
        width=1200,
        height=800,
    )

    # pc_fig = pc_fig.add_trace(plot_cube(*TARGET_EXTENTS[0].get_vertices_from_limits(), color="red", opacity=0.6))
    # pc_fig = pc_fig.add_trace(
    #     plot_cube(*TARGET_EXTENTS[1].get_vertices_from_limits(), color="lightgreen", opacity=0.6)
    # )
    # pc_fig = pc_fig.add_trace(plot_cube(*TARGET_EXTENTS[2].get_vertices_from_limits(), color="gold", opacity=0.6))

    plot_sphere_interactive(pc_fig, sphere_origin=(0, 0, -1.3)).servable()

    # run with: panel serve src/visualization/utils_3d.py --show --autoreload
