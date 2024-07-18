import papermill as pm

from src.data import config

parameters = {
    "0": {
        "BAG_NAME": "molisens_met_2023_08_07-15_36_45_converted",
        "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    },
    "12": {
        "BAG_NAME": "molisens_met_2023_08_29-06_04_46_converted",
        "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    },
    "17": {
        "BAG_NAME": "molisens_met_2023_08_29-08_21_47_converted",
        "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    },
}

for run, params in parameters.items():
    pm.execute_notebook(
        "notebooks/target_analysis/1.1_cg_target_analysis.ipynb",
        f"notebooks/target_analysis/1.1_cg_target_analysis_{run}.ipynb",
        parameters=params,
    )
