from pointcloudset import Dataset, PointCloud
from pathlib import Path

# import urllib.request

# urllib.request.urlretrieve("https://github.com/virtual-vehicle/pointcloudset/raw/master/tests/testdata/test.bag", "test.bag")
# urllib.request.urlretrieve("https://github.com/virtual-vehicle/pointcloudset/raw/master/tests/testdata/las_files/test_tree.las", "test_tree.las")

dataset = Dataset.from_file(
    Path(
        "/workspaces/molisensext_analysis/data/0external/ubuntu2004_bagfiles/molisens_met_2023_04_14-09_23_34_wrong_time"
    ),
    topic="/sensing/lidar/points",
    keep_zeros=False,
)
pointcloud = dataset[0]
pointcloud.timestamp

# tree = PointCloud.from_file(Path("test_tree.las"))

# tree.plot("x", hover_data=True)
