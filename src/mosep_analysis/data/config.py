from pathlib import Path

from moseplib.data.utils import Limits


PROJECT_FOLDER = Path.home() / "mosep-analysis"

DATA_FOLDER = PROJECT_FOLDER / "data"

FIGURE_FOLDER = PROJECT_FOLDER / "reports" / "figures"
PRESENTATIONS_FOLDER = PROJECT_FOLDER / "presentations"

RAW_DATA_FOLDER = Path("/nas/home/chg/MOLISENSext")
INTERIM_DATA_FOLDER = Path("/datalocal/chg/MOLISENSext")
PROCESSED_DATA_FOLDER = Path("/datalocal/chg/MOLISENSext/processed")
EXTERNAL_DATA_FOLDER = Path.joinpath(DATA_FOLDER, "0external")

BAG_NAMES = {
    "0": "molisens_met_2023_08_07-15_36_45_converted",
    "7": "molisens_met_2023_08_28-21_02_52_converted",
    "8": "molisens_met_2023_08_28-21_40_13_converted",
    "12": "molisens_met_2023_08_29-06_04_46_converted",
    "17": "molisens_met_2023_08_29-08_21_47_converted",
    "27": "molisens_met_2023_08_29-13_41_50_converted",
    "31": "molisens_met_2023_08_29-16_58_02_converted",
    "32": "molisens_met_2023_08_29-17_58_33_converted",
    "39": "molisens_met_2023_08_30-15_34_22_converted",
    "48": "molisens_met_2023_08_30-21_14_20_converted",
    "95": "molisens_met_2023_09_23-06_39_11_converted",
    "104": "molisens_met_2023_09_23-11_26_44_converted",
}
SHIFT_DS_DATA = {
    "7": -2 * 60 * 60,
    "39": -2 * 60 * 60,
    "48": -2 * 60 * 60,
    "104": -2 * 60 * 60,
}

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
    "Target-01": Limits(
        x_min=5.90, x_max=6.30, y_min=0.72, y_max=2.20, z_min=-1.40, z_max=-0.80, r_min=6.19, r_max=6.57
    ),  # done
    "Target-02": Limits(
        x_min=14.00, x_max=14.25, y_min=-0.80, y_max=0.85, z_min=-1.60, z_max=-1.05, r_min=14.00, r_max=14.40
    ),
    "Target-03": Limits(
        x_min=23.08, x_max=23.18, y_min=-3.10, y_max=-1.60, z_min=-1.80, z_max=-1.21, r_min=23.10, r_max=23.40
    ),
    "Target-04": Limits(
        x_min=32.30, x_max=32.42, y_min=0.5, y_max=2.10, z_min=-2.00, z_max=-1.32, r_min=32.30, r_max=32.60
    ),
    "Target-05": Limits(
        x_min=45.51, x_max=45.80, y_min=-2.75, y_max=0.60, z_min=-2.26, z_max=-1.20, r_min=45.50, r_max=45.90
    ),
}


def _get_target_distance(min_dist, max_dist):
    """Helper to calculate the target distance from min and max distance."""
    if min_dist is None or max_dist is None:
        return None
    return round(min_dist + (max_dist - min_dist) / 2, 2)


TARGET_DISTANCES = {k: _get_target_distance(v.r_min, v.r_max) for k, v in TARGET_EXTENTS_VIF.items()}

TARGET_EXTENTS_VIF_SPLITS = {
    "Target-01": {
        "white": TARGET_EXTENTS_VIF["Target-01"].replace(y_min=1.69),
        "grey": TARGET_EXTENTS_VIF["Target-01"].replace(y_min=1.20).replace(y_max=1.69),
        "black": TARGET_EXTENTS_VIF["Target-01"].replace(y_max=1.20),
    },
    "Target-02": {
        "white": TARGET_EXTENTS_VIF["Target-02"].replace(y_max=-0.21),
        "grey": TARGET_EXTENTS_VIF["Target-02"].replace(y_min=-0.21).replace(y_max=0.31),
        "black": TARGET_EXTENTS_VIF["Target-02"].replace(y_min=0.31),
    },
    "Target-03": {
        "white": TARGET_EXTENTS_VIF["Target-03"].replace(y_min=-2.61).replace(y_max=-2.06),
        "grey": TARGET_EXTENTS_VIF["Target-03"].replace(y_min=-2.61),
        "black": TARGET_EXTENTS_VIF["Target-03"].replace(y_max=-2.06),
    },
    "Target-04": {
        "white": TARGET_EXTENTS_VIF["Target-04"].replace(y_max=1.10),
        "grey": TARGET_EXTENTS_VIF["Target-04"].replace(y_min=1.10).replace(y_max=1.50),
        "black": TARGET_EXTENTS_VIF["Target-04"].replace(y_min=1.50),
    },
    "Target-05": {
        "white": TARGET_EXTENTS_VIF["Target-05"].replace(y_min=-1.53).replace(y_max=-0.53),
        "grey": TARGET_EXTENTS_VIF["Target-05"].replace(y_min=-0.53),
        "black": TARGET_EXTENTS_VIF["Target-05"].replace(y_max=-1.53),
    },
}

ROOF_EXTENT = Limits(x_min=1, x_max=50, y_min=-3.4, y_max=2.7, z_min=None, z_max=None, r_min=None, r_max=None)

RING_INNER = Limits(x_min=0, x_max=None, y_min=None, y_max=None, z_min=-0.065, z_max=None, r_min=0.00, r_max=0.6)
RING_OUTER = Limits(x_min=0, x_max=None, y_min=None, y_max=None, z_min=-0.2, z_max=None, r_min=0.6, r_max=20.0)

if __name__ == "__main__":
    print(TARGET_EXTENTS_VIF_SPLITS)
