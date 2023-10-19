from copy import deepcopy
from pathlib import Path
from typing import Dict, Iterator, Optional, Union

from matplotlib import pyplot as plt

from ouster import client
from ouster.client import LidarPacket
from ouster.client.data import ChanField, FieldDType, LidarScan, XYZLut, PacketIdError
from ouster.client.core import UDPProfileLidar, Packets

from rosbags.rosbag2 import Reader


def get_data(bag_file: Path, topic: str) -> list:
    data = []
    with Reader(bag_file) as reader:
        connections = [x for x in reader.connections if x.topic == topic]

        for connection, timestamp, rawdata in reader.messages(connections=connections):
            data.append(rawdata)

    return data


class ScansFromBag:
    """An iterable stream of scans batched from a PacketSource.

    Batching will emit a scan every time the frame_id increments (i.e. on
    receiving first packet in the next scan). Reordered packets will be handled,
    except across frame boundaries: packets from the previous scan will be
    dropped.
    """

    def __init__(
        self,
        source: client.core.PacketSource,
        *,
        complete: bool = False,
        timeout: Optional[float] = 2.0,
        fields: Optional[Dict[ChanField, FieldDType]] = None,
        _max_latency: int = 0,
    ) -> None:
        """
        Args:
            source: any source of packets
            complete: if True, only return full scans
            timeout: seconds to wait for a scan before error or None
            fields: specify which channel fields to populate on LidarScans
            _max_latency: (experimental) approximate max number of frames to buffer
        """
        self._source = source
        self._complete = complete
        self._timeout = timeout
        self._max_latency = _max_latency
        # used to initialize LidarScan
        self._fields: Union[Dict[ChanField, FieldDType], UDPProfileLidar] = (
            fields if fields is not None else self._source.metadata.format.udp_profile_lidar
        )

    def __iter__(self) -> Iterator[LidarScan]:
        """Get an iterator."""

        w = self._source.metadata.format.columns_per_frame
        h = self._source.metadata.format.pixels_per_column
        packets_per_frame = w // self._source.metadata.format.columns_per_packet

        # pf = client._client.PacketFormat.from_info(self._source.metadata)
        batch = client._client.ScanBatcher(self._source.metadata)

        info = self._source.metadata

        ls = client.LidarScan(
            info.format.pixels_per_column, info.format.columns_per_frame, info.format.udp_profile_lidar
        )
        for p in self._source:
            if batch(p._data, ls):
                yield deepcopy(ls)

        # # Time from which to measure timeout
        # start_ts = time.monotonic()

        # ls_write = None
        # column_window = self._source.metadata.format.column_window

        # it = iter(self._source)
        # while True:
        #     try:
        #         packet = next(it)
        #     except StopIteration:
        #         if ls_write is not None:
        #             if not self._complete or ls_write.complete(column_window):
        #                 yield ls_write
        #         return

        #     if self._timeout is not None and (time.monotonic() >= start_ts + self._timeout):
        #         raise ClientTimeout(f"No lidar scans within {self._timeout}s")

        #     if isinstance(packet, LidarPacket):
        #         ls_write = ls_write or LidarScan(h, w, self._fields)

        #         if batch(packet._data, ls_write):
        #             # Got a new frame, return it and start another
        #             if not self._complete or ls_write.complete(column_window):
        #                 yield ls_write
        #                 start_ts = time.monotonic()
        #             ls_write = None


def main():
    BAG_FILE = Path("/workspaces/molisensext_analysis/data/0external/ubuntu2004_bagfiles/lidar_packets_test_file")
    METADATA = BAG_FILE / "ouster_metadata.txt"
    LIDAR_TOPIC = "/sensing/lidar_top/lidar_packets"

    with open(METADATA, "r") as f:
        metadata = client.SensorInfo(f.read())

    # Get the raw data from the bag file
    packet_data = get_data(Path(BAG_FILE), LIDAR_TOPIC)
    print(f"Done reading data. Got: {len(packet_data)} packets.")

    # Convert the raw data packets into LidarPackets (numpy arrays).
    passed_packets = []
    lp = []
    for pd in packet_data:
        try:
            lp.append(LidarPacket(pd, info=metadata, _raise_on_id_check=True))
        except ValueError:
            passed_packets.append(len(pd))
        except PacketIdError as e:
            print(e)

    print(f"{passed_packets=}")

    # Create a packet stream from the list of LidarPackets
    packet_stream = Packets(lp, metadata)
    # Apply the ScansFromBag class to the packet stream
    scans = ScansFromBag(packet_stream, complete=True)

    xyz_frames = []
    for scan in scans:
        # Process the lidar scan

        xyzlut = XYZLut(info=metadata)
        xyz_frames.append(xyzlut(scan))
        # destaggered_cartisian = destagger(info=metadata, fields=xyzlut(scan))
        # print(destaggered_cartisian.shape)

        # if xyzlut(scan).sum() == 0:
        #     print("Scan is empty")
        # else:
        #     print("Scan is not empty")

    return xyz_frames


if __name__ == "__main__":
    frames = main()
    plt.imshow(frames[120][:, :, 0])
    plt.show()
