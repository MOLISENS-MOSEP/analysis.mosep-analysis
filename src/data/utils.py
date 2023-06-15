from typing import NamedTuple, Union
from pointcloudset import PointCloud


class Limits(NamedTuple):
    x_min: Union[float, None]
    x_max: Union[float, None]
    y_min: Union[float, None]
    y_max: Union[float, None]
    z_min: Union[float, None]
    z_max: Union[float, None]

    def apply_limits(self, pc: PointCloud) -> PointCloud:
        """
        Applies limits to a PointCloud object along the x, y, and z dimensions.

        Args:
            pc (PointCloud): The PointCloud object to apply the limits to.

        Returns:
            PointCloud: A new PointCloud object with the limits applied.
        """
        x_min = float("-inf") if self.x_min is None else self.x_min
        x_max = float("inf") if self.x_max is None else self.x_max
        y_min = float("-inf") if self.y_min is None else self.y_min
        y_max = float("inf") if self.y_max is None else self.y_max
        z_min = float("-inf") if self.z_min is None else self.z_min
        z_max = float("inf") if self.z_max is None else self.z_max

        return (
            pc.limit(dim="x", minvalue=x_min, maxvalue=x_max)
            .limit(dim="y", minvalue=y_min, maxvalue=y_max)
            .limit(dim="z", minvalue=z_min, maxvalue=z_max)
        )

    def get_vertices_from_limits(self, format: str = "xyz"):
        """Calculates the coordinates of the 8 vertices of a cube given the minimum and maximum values for each
        dimension.

        Possible formats for the output: xyz_lists and vertices_list.
        - xyz_lists format returns the x, y, and z coordinates of each vertex as separate lists. This format is useful when
        you need to work with the x, y, and z coordinates separately, for example, when plotting the vertices using a
        library like Matplotlib or Plotly.
        - vertices_list format returns a list of tuples, where each tuple represents the x, y, and z coordinates of a
        vertex. This format is useful when you need to work with the vertices as a whole, for example, when calculating the
        distance between two vertices or when performing operations on the vertices as a group

        Args:
            limits (object): An object that has the following attributes: x_min, x_max, y_min, y_max, z_min, z_max.
            format (str, optional): The format of the output. Can be 'xyz' or 'vertices'. Defaults to 'xyz'.

        Raises:
            ValueError: If the format is not supported.

        Returns:
            tuple or list: The coordinates of the 8 vertices of the cube.
        """

        vertices = [
            (self.x_min, self.y_min, self.z_min),
            (self.x_min, self.y_max, self.z_min),
            (self.x_max, self.y_max, self.z_min),
            (self.x_max, self.y_min, self.z_min),
            (self.x_min, self.y_min, self.z_max),
            (self.x_min, self.y_max, self.z_max),
            (self.x_max, self.y_max, self.z_max),
            (self.x_max, self.y_min, self.z_max),
        ]

        if format == "xyz":
            return zip(*vertices)
        elif format == "vertices":
            return vertices
        else:
            raise ValueError("Format not supported.")
