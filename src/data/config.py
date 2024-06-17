from src.data.utils import Limits

from pathlib import Path


PROJECT_FOLDER = Path("/workspaces/MOLISENSext_analysis")

DATA_FOLDER = Path.joinpath(PROJECT_FOLDER, "data")

FIGURE_FOLDER = Path.joinpath(PROJECT_FOLDER, "reports").joinpath("figures")
PRESENTATIONS_FOLDER = Path.joinpath(PROJECT_FOLDER, "presentations")

RAW_DATA_FOLDER = Path.joinpath(DATA_FOLDER, "1raw")
INTERIM_DATA_FOLDER = Path.joinpath(DATA_FOLDER, "2interim")
PROCESSED_DATA_FOLDER = Path.joinpath(DATA_FOLDER, "3processed")
EXTERNAL_DATA_FOLDER = Path.joinpath(DATA_FOLDER, "0external")

PATH_TO_LUFFT_MSGS = PROJECT_FOLDER / Path("src/config/custom_ros_msgs/lufft_wsx_interfaces/msg")

PC_TOPICS = [
    "/sensing/lidar/points",
    "/sensing/lidar/points2",
    "/sensing/radar/points",
]
FIELDS = ["x", "y", "z", "intensity", "t", "reflectivity", "ring", "ambient", "range", "original_id"]

TARGET_EXTENTS_BA = [
    #      xmin,  xmax,  ymin, ymax, zmin,  zmax,  rmin, rmax
    Limits(12.80, 13.60, 5.70, 7.20, -1.20, -0.69, 14.5, 15.0),
    Limits(23.50, 23.90, 0.20, 1.80, -1.40, -0.90, 23.6, 24.0),
    Limits(38.60, 39.80, 6.50, 9.60, -1.30, -0.70, 39.8, 40.3),
]

# * ViF Roof
# Margins:
# in x +-0.02 m
# in y +-0.1 m
# in z +-0.01 m
# in r +-0.1 m
TARGET_EXTENTS_VIF = {
    #                   xmin,  xmax,  ymin, ymax, zmin,  zmax, rmin, rmax
    "Target 1": Limits(
        x_min=5.90, x_max=6.30, y_min=0.72, y_max=2.20, z_min=-1.40, z_max=-0.80, r_min=6.19, r_max=6.57
    ),  # done
    "Target 2": Limits(
        x_min=14.00, x_max=14.25, y_min=-0.80, y_max=0.85, z_min=-1.60, z_max=-1.05, r_min=14.00, r_max=14.40
    ),
    "Target 3": Limits(
        x_min=23.08, x_max=23.18, y_min=-3.10, y_max=-1.60, z_min=-1.80, z_max=-1.21, r_min=23.10, r_max=23.40
    ),
    "Target 4": Limits(
        x_min=32.30, x_max=32.42, y_min=0.5, y_max=2.10, z_min=-2.00, z_max=-1.32, r_min=32.30, r_max=32.60
    ),
    "Target 5": Limits(
        x_min=45.51, x_max=45.80, y_min=-2.75, y_max=0.60, z_min=-2.26, z_max=-1.20, r_min=45.50, r_max=45.90
    ),
}

TARGET_EXTENTS_VIF_SPLITS = {
    "Target 1": {
        "white": TARGET_EXTENTS_VIF["Target 1"].replace(y_min=1.69),
        "grey": TARGET_EXTENTS_VIF["Target 1"].replace(y_min=1.20).replace(y_max=1.69),
        "black": TARGET_EXTENTS_VIF["Target 1"].replace(y_max=1.20),
    },
    "Target 2": {
        "white": TARGET_EXTENTS_VIF["Target 2"].replace(y_max=-0.21),
        "grey": TARGET_EXTENTS_VIF["Target 2"].replace(y_min=-0.21).replace(y_max=0.31),
        "black": TARGET_EXTENTS_VIF["Target 2"].replace(y_min=0.31),
    },
    "Target 3": {
        "white": TARGET_EXTENTS_VIF["Target 3"].replace(y_min=-2.61).replace(y_max=-2.06),
        "grey": TARGET_EXTENTS_VIF["Target 3"].replace(y_min=-2.61),
        "black": TARGET_EXTENTS_VIF["Target 3"].replace(y_max=-2.06),
    },
    "Target 4": {
        "white": TARGET_EXTENTS_VIF["Target 4"].replace(y_max=1.10),
        "grey": TARGET_EXTENTS_VIF["Target 4"].replace(y_min=1.10).replace(y_max=1.50),
        "black": TARGET_EXTENTS_VIF["Target 4"].replace(y_min=1.50),
    },
    "Target 5": {
        "white": TARGET_EXTENTS_VIF["Target 5"].replace(y_min=-1.53).replace(y_max=-0.53),
        "grey": TARGET_EXTENTS_VIF["Target 5"].replace(y_min=-0.53),
        "black": TARGET_EXTENTS_VIF["Target 5"].replace(y_max=-1.53),
    },
}

ROOF_EXTENT = Limits(x_min=1, x_max=50, y_min=-3.4, y_max=2.7, z_min=None, z_max=None, r_min=None, r_max=None)

RING_INNER = Limits(x_min=0, x_max=None, y_min=None, y_max=None, z_min=-0.065, z_max=None, r_min=0.00, r_max=0.6)
RING_OUTER = Limits(x_min=0, x_max=None, y_min=None, y_max=None, z_min=-0.2, z_max=None, r_min=0.6, r_max=20.0)

if __name__ == "__main__":
    print(TARGET_EXTENTS_VIF_SPLITS)
