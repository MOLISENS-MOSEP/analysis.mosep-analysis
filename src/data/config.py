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

TARGET_EXTENTS_BA = [
    #      xmin,  xmax,  ymin, ymax, zmin,  zmax,  rmin, rmax
    Limits(12.80, 13.60, 5.70, 7.20, -1.20, -0.69, 14.5, 15.0),
    Limits(23.50, 23.90, 0.20, 1.80, -1.40, -0.90, 23.6, 24.0),
    Limits(38.60, 39.80, 6.50, 9.60, -1.30, -0.70, 39.8, 40.3),
]

TARGET_EXTENTS_VIF = {
    #                   xmin,  xmax,  ymin, ymax, zmin,  zmax, rmin, rmax
    "Target 1": Limits(-6.3, -5.9, -2.2, -0.72, -1.4, -0.96, 6.5, 6.7),  # done
    "Target 2": Limits(23.50, 23.90, 0.20, 1.80, -1.40, -0.90, 23.6, 24.0),
    "Target 3": Limits(38.60, 39.80, 6.50, 9.60, -1.30, -0.70, 39.8, 40.3),
    "Target 4": Limits(38.60, 39.80, 6.50, 9.60, -1.30, -0.70, 39.8, 40.3),
    "Target 5": Limits(38.60, 39.80, 6.50, 9.60, -1.30, -0.70, 39.8, 40.3),
    "Ring Sensor": Limits(None, None, None, None, -0.067, None, 0, 0.6),  # done
}


FIELDS = ["x", "y", "z", "intensity", "t", "reflectivity", "ring", "ambient", "range", "original_id"]
