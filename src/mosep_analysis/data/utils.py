import pickle
from pathlib import Path
from typing import Callable, Any

from moseplib.data import pointcloud_processing
from pointcloudset import Dataset


def load_pickle_or_calculate(path: Path, calc_func: Callable[..., Any], *args, **kwargs) -> Any:
    """
    Loads a variable from a pickle file if it exists, otherwise calculates it using calc_func,
    saves it to the pickle file, and returns the result.

    Args:
        path (Path): Path to the pickle file.
        calc_func (Callable): Function to calculate the variable if not cached.
        *args, **kwargs: Arguments to pass to calc_func.

    Returns:
        Any: The loaded or calculated variable.

    Example usage:
        rain_ds_seconds = load_or_calculate(
            "path/to/pickled/data.pickle",
            pointcloud_processing.resample_dataset,
            dataset, "1s", statistics=["std", "sum"]
        )
    """
    if not path.exists():
        result = calc_func(*args, **kwargs)
        with open(path, "wb") as handle:
            pickle.dump(result, handle, protocol=pickle.HIGHEST_PROTOCOL)
    else:
        with open(path, "rb") as handle:
            result = pickle.load(handle)
    return result


def load_or_resample_dataset(path: Path, ds: Dataset = None, *args, **kwargs) -> Any:
    """Load or resample dataset.

    Loads a resampled dataset from parquet files if they exist, otherwise resamples the given dataset,
    saves the resampled datasets to parquet files, and returns the result.

    Keyword arguments:
    argument -- description
    Return: return_description
    """

    if not path.is_dir() and ds is not None:
        ds_res = pointcloud_processing.resample_dataset(ds, *args, **kwargs)
        # Save the resampled datasets to parquet
        for stat, ds in ds_res.items():
            ds.to_file(path / stat, use_orig_filename=False)

    # load from parquet
    ds_res = {}
    for p in path.iterdir():
        ds_res[p.stem] = Dataset.from_file(p)

    return ds_res
