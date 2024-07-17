import papermill as pm

from src.data import config

parameters = {
    "01": {
        "BAG_NAME": "molisens_met_2023_08_29-06_04_46_converted",
        "DATA_DIR": config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data",
    },
    # "02": {
    #     "BAG_NAME": "molisens_met_2023_08_29-06_04_46_converted",
    #     "DATA_DIR": config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data",
    #    },
}

for run, params in parameters.items():
    pm.execute_notebook(
        "notebooks/target_analysis/1.1_cg_target_analysis.ipynb",
        f"notebooks/target_analysis/1.1_cg_target_analysis_{run}.ipynb",
        parameters=params,
    )
