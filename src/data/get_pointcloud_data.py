#!/usr/bin/env python3

# from src.data import config

from pointcloudset import Dataset, PointCloud
from pathlib import Path
from rich import print as rprint

from src.data import extract_pcs_from_bagfile


def print_stats(bag_path, dataset):
    print(f"Dataset loaded from:\n{bag_path}")
    print(f"start =    {dataset.start_time}")
    print(f"end =      {dataset.end_time}")
    print(f"duration = {dataset.duration}")
    print(f"length =   {len(dataset)}")
    freq = len(dataset) / (dataset.duration.seconds + dataset.duration.microseconds / 1e6)
    print(f"avg frequency =  {freq :.2f} Hz")


def load_pointcloudset(
    data_dir: Path,
    bag_name: str,
    topic: str,
    safe_parquet: bool = True,
    keep_zeros: bool = False,
    invert_axes=None,
    verbose=False,
) -> Dataset:
    """
    Load a point cloud dataset from a ROS bag file.

    Args:
        data_dir (Path): Path to the directory containing the bag file and/or pointcloudset files.
        bag_name (str): Name of the ROS bag file to load.
        topic (str): Name of the ROS topic containing to load.
        safe_parquet (bool, optional): Whether to store pre-generated point cloud dataset files in Parquet format if
            available. Defaults to True.
        keep_zeros (bool, optional): Whether to keep points with zero coordinates. Defaults to False.
        invert_axes (list, optional): List of axes to invert (Multiply by -1). Defaults to None.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.

    Returns:
        Dataset: A point cloud dataset object.

    Raises:
        FileNotFoundError: If no point cloud dataset files are found and the ROS bag file does not exist.
    """
    data_dir = Path(data_dir)
    bag_path = data_dir / bag_name

    pointcloudset_path = data_dir / "pointcloudset" / topic[1:].replace("/", "_") / bag_name
    if verbose:
        rprint(f"Searching for pointcloudset files in:\n{pointcloudset_path}")

    if not pointcloudset_path.exists():
        print(f"No pointcloudset files found for topic: {topic}.")

        if not bag_path.exists():
            raise FileNotFoundError(f"No pointcloudset files found and {bag_path} does not exist")

        if not safe_parquet:
            # Calculate on the fly
            print("Loading bag file on the fly..")
            dataset = Dataset.from_file(
                bag_path,
                topic=topic,
                keep_zeros=keep_zeros,
            )
            if verbose:
                print_stats(bag_path, dataset)
            return dataset

        rprint("Creating pointcloudset files now..")
        extract_pcs_from_bagfile.extract(bag_path, [topic], verbose=verbose)

    dataset = Dataset.from_file(pointcloudset_path)
    if verbose:
        print_stats(pointcloudset_path, dataset)
    
    if invert_axes:
        if not isinstance(invert_axes, list):
            raise TypeError("invert_axes must be a list")
        missing_axis = [elem for elem in invert_axes if elem not in dataset.daskdataframe.columns]
        if missing_axis:
            raise ValueError(f"These axis are not in present in dataset: {missing_axis}")
        dataset = dataset.apply(_invert_axes, axes=invert_axes)
        
    return dataset


def _invert_axes(frame: PointCloud, axes) -> PointCloud:
    df = frame.data
    df.update(-df[axes])
    return PointCloud(df)

def get_dataset_statistics(dataset: Dataset):
    pass


if __name__ == "__main__":
    load_pointcloudset(
        "/workspaces/MOLISENSext_analysis/data/2interim/bad_aussee/data/molisens_met_2023_04_14-09_23_34_converted_pointcloudset",
        verbose=True,
    )
