#!/usr/bin/env python3

# from src.data import config

from pointcloudset import Dataset
from pathlib import Path
from rich import print as rprint


def load_pointcloudset(bag_path: Path, verbose=False) -> Dataset:
    dataset = Dataset.from_file(Path(bag_path))

    if verbose:
        rprint(f"Dataset loaded from {bag_path}")
        rprint(f"start = {dataset.start_time}")
        rprint(f"end =   {dataset.end_time}")
        rprint(f"end =   {dataset.duration}")
        rprint(f"length =  {len(dataset)}")
        freq = len(dataset) / (
            dataset.duration.seconds + dataset.duration.microseconds / 1e6
        )
        rprint(f"avg frequency =  {freq :.2f} Hz")
    return dataset


def get_dataset_statistics(dataset: Dataset):
    pass


if __name__ == "__main__":
    load_pointcloudset(
        "/workspaces/MOLISENSext_analysis/data/2interim/bad_aussee/data/molisens_met_2023_04_14-09_23_34_converted_pointcloudset",
        verbose=True,
    )
