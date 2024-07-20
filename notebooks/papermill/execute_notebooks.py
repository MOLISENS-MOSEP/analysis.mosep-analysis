import papermill as pm

from src.data import config

parameters = {
    "0": {
        "BAG_NAME": "molisens_met_2023_08_07-15_36_45_converted",
        "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
        "TIMESTAMPS_HISTOGRAMS": ["2023-08-07T13:37:00"],
    },
    "12": {
        "BAG_NAME": "molisens_met_2023_08_29-06_04_46_converted",
        "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
        "TIMESTAMPS_HISTOGRAMS": [
            "2023-08-29T04:05:00",
            "2023-08-29T04:25:00",
            "2023-08-29T04:35:00",
            "2023-08-29T04:42:00",
            "2023-08-29T04:50:00",
        ],
    },
    "17": {
        "BAG_NAME": "molisens_met_2023_08_29-08_21_47_converted",
        "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
        "TIMESTAMPS_HISTOGRAMS": [
            "2023-08-29T06:23:00",
            "2023-08-29T06:26:00",
            "2023-08-29T06:32:00",
            "2023-08-29T06:41:00",
        ],
    },
}

for run, params in parameters.items():
    pm.execute_notebook(
        "notebooks/target_analysis/1.1_cg_target_analysis.ipynb",
        f"notebooks/target_analysis/1.1_cg_target_analysis_{run}.ipynb",
        parameters=params,
    )
