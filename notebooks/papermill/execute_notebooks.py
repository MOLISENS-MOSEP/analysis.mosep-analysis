import papermill as pm

from mosep_analysis.data import config

parameters = {
    "0": {
        "BAG_NAME": "molisens_met_2023_08_07-15_36_45_converted",
        "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
        "TIMESTAMPS_HISTOGRAMS": ["2023-08-07T13:37:00"],
    },
    # "7": {
    #     "BAG_NAME": "molisens_met_2023_08_28-21_02_52_converted",
    #     "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    #     "TIMESTAMPS_HISTOGRAMS": [],
    # },
    # "8": {
    #     "BAG_NAME": "molisens_met_2023_08_28-21_40_13_converted",
    #     "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    #     "TIMESTAMPS_HISTOGRAMS": [
    #         "2023-08-29T04:05:00",
    #     ],
    # },
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
    # "17": {
    #     "BAG_NAME": "molisens_met_2023_08_29-08_21_47_converted",
    #     "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    #     "TIMESTAMPS_HISTOGRAMS": [
    #         "2023-08-29T06:23:00",
    #         "2023-08-29T06:26:00",
    #         "2023-08-29T06:32:00",
    #         "2023-08-29T06:41:00",
    #     ],
    # },
    # "18": {
    #     "BAG_NAME": "molisens_met_2023_08_29-08_54_47_converted",
    #     "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    #     "TIMESTAMPS_HISTOGRAMS": [],
    # },
    # "27": {
    #     "BAG_NAME": "molisens_met_2023_08_29-13_41_50_converted",
    #     "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    #     "TIMESTAMPS_HISTOGRAMS": [],
    # },
    # "31": {
    #     "BAG_NAME": "molisens_met_2023_08_29-16_58_02_converted",
    #     "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    #     "TIMESTAMPS_HISTOGRAMS": [],
    # },
    # "32": {
    #     "BAG_NAME": "molisens_met_2023_08_29-17_58_33_converted",
    #     "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    #     "TIMESTAMPS_HISTOGRAMS": [],
    # },
    # "39": {
    #     "BAG_NAME": "molisens_met_2023_08_30-15_34_22_converted",
    #     "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    #     "TIMESTAMPS_HISTOGRAMS": [],
    # },
    # "48": {
    #     "BAG_NAME": "molisens_met_2023_08_30-21_14_20_converted",
    #     "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    #     "TIMESTAMPS_HISTOGRAMS": [],
    # },
    # "95": {
    #     "BAG_NAME": "molisens_met_2023_09_23-06_39_11_converted",
    #     "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    #     "TIMESTAMPS_HISTOGRAMS": [],
    # },
    # "104": {
    #     "BAG_NAME": "molisens_met_2023_09_23-11_26_44_converted",
    #     "DATA_DIR": str(config.INTERIM_DATA_FOLDER / "ViF_Roof" / "data"),
    #     "TIMESTAMPS_HISTOGRAMS": [],
    # },
}

for run, params in parameters.items():
    pm.execute_notebook(
        "/home/chg/mosep-analysis/notebooks/target_analysis/1.1_cg_target_analysis_template.ipynb",
        f"/home/chg/mosep-analysis/notebooks/target_analysis/1.1_cg_target_analysis_{run}.ipynb",
        parameters=params,
    )

# consolidate datasets after individual processing
