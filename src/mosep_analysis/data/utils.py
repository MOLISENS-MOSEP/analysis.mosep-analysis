import pickle
from pathlib import Path
from typing import Callable, Any


def load_or_calculate(path: Path, calc_func: Callable[..., Any], *args, **kwargs) -> Any:
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
