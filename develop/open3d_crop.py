# ----------------------------------------------------------------------------
# -                        Open3D: www.open3d.org                            -
# ----------------------------------------------------------------------------
# Copyright (c) 2018-2023 www.open3d.org
# SPDX-License-Identifier: MIT
# ----------------------------------------------------------------------------

import open3d as o3d


def crop_cloud_with_bbox(cloud, center=[0, 0], length=50, width=50, height=5):
    """Crop the global point cloud.
    Args:
        cloud: the global point cloud.
    Returns:
        a cropped point cloud.
    """
    bbox = o3d.geometry.AxisAlignedBoundingBox(
        min_bound=(center[0] - length, center[1] - width, -height),
        max_bound=(center[0] + length, center[1] + width, +height),
    )
    return cloud.crop(bbox)


if __name__ == "__main__":
    # print("Load a ply point cloud, crop it, and render it")
    # sample_ply_data = o3d.data.DemoCropPointCloud()
    # pcd = o3d.io.read_point_cloud(sample_ply_data.point_cloud_path)
    # vol = o3d.visualization.read_selection_polygon_volume(sample_ply_data.cropped_json_path)
    # chair = vol.crop_point_cloud(pcd)
    # # Flip the pointclouds, otherwise they will be upside down.
    # pcd.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])
    # chair.transform([[1, 0, 0, 0], [0, -1, 0, 0], [0, 0, -1, 0], [0, 0, 0, 1]])

    # print("Displaying original pointcloud ...")
    # o3d.visualization.draw([pcd])
    # print("Displaying cropped pointcloud")
    # o3d.visualization.draw([chair])

    sample_ply_data = o3d.data.DemoCropPointCloud()
    pcd = o3d.io.read_point_cloud(sample_ply_data.point_cloud_path)
    crop = crop_cloud_with_bbox(pcd, [0, 0], 2, 2, 2)
    o3d.visualization.draw([crop])
