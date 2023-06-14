from pathlib import Path


from ouster import client
from ouster.client import LidarPacket
from rosbags.rosbag2 import Reader


BAG_FILE = "data/1raw/bad_aussee/data/molisens_met_2023_04_14-09_23_34"
METADATA_PATH = "data/1raw/bad_aussee/data/molisens_met_2023_04_14-09_23_34/ouster_metadata.txt"


def get_data(bag_file: Path, topic: str) -> list:
    data = []
    with Reader(bag_file) as reader:
        connections = [x for x in reader.connections if x.topic == topic]
        i = 0
        for connection, timestamp, rawdata in reader.messages(connections=connections):
            data.append(rawdata)
            i += 1
            if i > 100:
                break

    return data


with open(METADATA_PATH, "r") as f:
    info = client.SensorInfo(f.read())

print(info)

packet_data = get_data(Path(BAG_FILE), "/sensing/lidar/lidar_packets")


packet = LidarPacket(packet_data[0], info=info, _raise_on_id_check=False)

if isinstance(packet, client.LidarPacket):
    # Now we can process the LidarPacket. In this case, we access
    # the measurement ids, timestamps, and ranges
    measurement_ids = packet.measurement_id
    timestamps = packet.timestamp
    ranges = packet.field(client.ChanField.RANGE)
    print(f"  encoder counts = {measurement_ids.shape}")
    print(f"  timestamps = {timestamps.shape}")
    print(f"  ranges = {ranges.shape}")
    print(packet)


# scans = client.Scans(packet, fields=info.format.udp_profile_lidar)

# # iterate `scans` and get the 84th LidarScan (it can be different with your data)
# scan = nth(scans, 84)
# ranges = scan.field(client.ChanField.RANGE)

# # destagger ranges, notice `metadata` use, that is needed to get
# # sensor intrinsics and correctly data transforms
# ranges_destaggered = client.destagger(info, ranges)

# plt.imshow(ranges_destaggered, cmap="gray", resample=False)


# packet_data = get_timeseries_data.get_data_deserialized(
#     Path(bag_file),
#     "/sensing/lidar/lidar_packets",
#     path_to_custom_msgs=config.PROJECT_FOLDER / Path("data/0external/ouster_msgs/msg"),
#     timestamp_source="msg",
#     has_header=False,
# )


# for packet in packet_data:
#     if isinstance(packet, client.LidarPacket):
#         print("true")
