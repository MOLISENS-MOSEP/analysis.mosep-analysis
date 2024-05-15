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
    "Target 1": Limits(5.9, 6.3, -2.2, -0.72, -1.4, -0.96, 6.19, 6.4),  # done
    "Target 2": Limits(14.0, 14.25, -0.85, 0.8, -1.52, -1.15, 14.0, 14.4),
    "Target 3": Limits(23.08, 23.18, 1.6, 3.1, -1.64, -1.31, 23.1, 23.4),
    "Target 4": Limits(32.3, 32.42, -2.1, -0.5, -1.85, -1.03, 32.3, 32.6),
    "Target 5": Limits(45.58, 45.80, -0.40, 1.80, -2.06, -1.46, 45.5, 45.9),
    "Ring Sensor": Limits(None, 0.0, None, None, -0.067, None, 0.0, 0.6),  # done
}

ROOF_EXTENT = Limits(x_min=1, x_max=50, y_min=-2.7, y_max=3.4, z_min=None, z_max=None, r_min=None, r_max=None)
