#!/usr/bin/env python3

# from src.data import config

from pointcloudset import Dataset
from pathlib import Path
from rich import print as rprint

from src.data import extract_pcs_from_bagfile


def print_stats(bag_path, dataset):
    rprint(f"Dataset loaded from {bag_path}")
    rprint(f"start = {dataset.start_time}")
    rprint(f"end =   {dataset.end_time}")
    rprint(f"end =   {dataset.duration}")
    rprint(f"length =  {len(dataset)}")
    freq = len(dataset) / (dataset.duration.seconds + dataset.duration.microseconds / 1e6)
    rprint(f"avg frequency =  {freq :.2f} Hz")


def load_pointcloudset(
    data_dir: Path, bag_name: str, topic: str, safe_parquet: bool = True, keep_zeros: bool = False, verbose=False
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
        rprint(f"Searching for pointcloudset files in {pointcloudset_path}")

    if not pointcloudset_path.exists():
        rprint(f"No pointcloudset files found for topic {topic}.")

        if not bag_path.exists():
            raise FileNotFoundError(f"No pointcloudset files found and {bag_path} does not exist")

        if not safe_parquet:
            # Calculate on the fly
            rprint("Loading bag file on the fly..")
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
        print_stats(bag_path, dataset)
    return dataset


def get_dataset_statistics(dataset: Dataset):
    pass


if __name__ == "__main__":
    load_pointcloudset(
        "/workspaces/MOLISENSext_analysis/data/2interim/bad_aussee/data/molisens_met_2023_04_14-09_23_34_converted_pointcloudset",
        verbose=True,
    )
