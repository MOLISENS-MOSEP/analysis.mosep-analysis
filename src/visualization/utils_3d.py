import numpy as np
import plotly.graph_objects as go


def get_cube(x_coords, y_coords, z_coords, color="red", opacity=0.6):
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
        colorscale=[[0, "gold"], [0.5, "mediumturquoise"], [1, "magenta"]],
        intensity=np.linspace(0, 1, 12, endpoint=True),
        intensitymode="cell",
        showscale=False,
    )


if __name__ == "__main__":
    fig = go.Figure(data=[get_cube()])
    fig.show()
