from src.data.utils import Limits

from pathlib import Path


# PROJECT_FOLDER = Path("/workspaces/MOLISENSext_analysis")
PROJECT_FOLDER = Path("/workspaces/molisensext_analysis")
DATA_FOLDER = Path.joinpath(PROJECT_FOLDER, "data")

FIGURE_FOLDER = Path.joinpath(PROJECT_FOLDER, "reports").joinpath("figures")
PRESENTATIONS_FOLDER = Path.joinpath(PROJECT_FOLDER, "presentations")

RAW_DATA_FOLDER = Path.joinpath(DATA_FOLDER, "1raw")
INTERIM_DATA_FOLDER = Path.joinpath(DATA_FOLDER, "2interim")
PROCESSED_DATA_FOLDER = Path.joinpath(DATA_FOLDER, "3processed")
EXTERNAL_DATA_FOLDER = Path.joinpath(DATA_FOLDER, "0external")

PATH_TO_LUFFT_MSGS = PROJECT_FOLDER / Path("data/0external/lufft_wsx_interfaces/msg")

PC_TOPICS = [
    "/sensing/lidar/points",
    "/sensing/lidar/points2",
    "/sensing/radar/points",
]

TARGET_EXTENTS = [
    #      xmin,  xmax,  ymin, ymax, zmin,  zmax,  rmin, rmax
    Limits(12.80, 13.60, 5.70, 7.20, -1.20, -0.70, 14.5, 15.0),
    Limits(23.50, 23.90, 0.20, 1.80, -1.40, -0.90, 23.6, 24.0),
    Limits(38.60, 39.80, 6.50, 9.60, -1.30, -0.70, 39.8, 40.3),
]

FIELDS = ["x", "y", "z", "intensity", "t", "reflectivity", "ring", "ambient", "range", "original_id"]
