from pathlib import Path
from typing import cast, Dict, Iterable, Iterator, List, Optional, Tuple, Union
import warnings
from rich import print as rprint
import time
from matplotlib import pyplot as plt

from ouster import client
from ouster.client import LidarPacket, SensorInfo
from ouster.client.data import ChanField, FieldDType, LidarScan, XYZLut, destagger, PacketIdError
from ouster.client.core import UDPProfileLidar, ClientTimeout, PacketSource, Packets

from rosbags.rosbag2 import Reader


class ListPacketSource(PacketSource):
    def __init__(self, packets):
        self.packets = packets
        self._metadata = None

    def __iter__(self):
        for packet in self.packets:
            yield packet

    @property
    def metadata(self) -> SensorInfo:
        """Metadata associated with the packet stream."""
        return self._metadata

    @metadata.setter
    def metadata(self, value: SensorInfo) -> None:
        """Set the metadata associated with the packet stream."""
        self._metadata = value


BAG_FILE = Path("/workspaces/molisensext_analysis/data/0external/ubuntu2004_bagfiles/molisens_met_2023_03_07-14_05_21")
METADATA_PATH = BAG_FILE / "ouster_metadata.txt"


def get_data(bag_file: Path, topic: str) -> list:
    data = []
    with Reader(bag_file) as reader:
        connections = [x for x in reader.connections if x.topic == topic]
        i = 0
        for connection, timestamp, rawdata in reader.messages(connections=connections):
            data.append(rawdata)
            # i += 1
            # if i > 40000:
            #     break

    return data


class ScansFromBag:
    """An iterable stream of scans batched from a PacketSource.

    Batching will emit a scan every time the frame_id increments (i.e. on
    receiving first packet in the next scan). Reordered packets will be handled,
    except across frame boundaries: packets from the previous scan will be
    dropped.

    Optionally filters out incomplete frames and enforces a timeout. A batching
    timeout can be useful to detect when we're only receiving incomplete frames
    or only imu packets. Can also be configured to manage internal buffers for
    soft real-time applications.
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
        column_window = self._source.metadata.format.column_window

        ls_write = None
        pf = client._client.PacketFormat.from_info(self._source.metadata)
        batch = client._client.ScanBatcher(w, pf)

        # Time from which to measure timeout
        start_ts = time.monotonic()

        it = iter(self._source)
        while True:
            try:
                packet = next(it)
            except StopIteration:
                if ls_write is not None:
                    if not self._complete or ls_write.complete(column_window):
                        yield ls_write
                return

            if self._timeout is not None and (time.monotonic() >= start_ts + self._timeout):
                raise ClientTimeout(f"No lidar scans within {self._timeout}s")

            if isinstance(packet, LidarPacket):
                ls_write = ls_write or LidarScan(h, w, self._fields)

                if batch(packet._data, ls_write):
                    # Got a new frame, return it and start another
                    if not self._complete or ls_write.complete(column_window):
                        yield ls_write
                        start_ts = time.monotonic()
                    ls_write = None



with open(METADATA_PATH, "r") as f:
    metadata = client.SensorInfo(f.read())


fields = None

# used to initialize LidarScan
_fields = metadata.format.udp_profile_lidar


w = metadata.format.columns_per_frame
h = metadata.format.pixels_per_column
packets_per_frame = w // metadata.format.columns_per_packet
column_window = metadata.format.column_window


ls_write = None
pf = client._client.PacketFormat.from_info(metadata)

batch = client._client.ScanBatcher(w, pf)

packet_data = get_data(Path(BAG_FILE), "/sensing/lidar/lidar_packets")
rprint(f"Done reading data. Got: {len(packet_data)} packets.")

passed_packets = []
source = []
for pd in packet_data:
    try:
        source.append(LidarPacket(pd, info=metadata, _raise_on_id_check=True))
    except ValueError:
        passed_packets.append(len(pd))
    except PacketIdError as e:
        print(e)
        
rprint(passed_packets)


# source = ListPacketSource(source)
# source.metadata = metadata
# metadata.format.columns_per_frame = 483
source = Packets(source, metadata)
# print(source.metadata.format.columns_per_frame)

scans = ScansFromBag(source, complete=False)

for scan in scans:
    # Process the lidar scan

    xyzlut = XYZLut(info=metadata)
    
    if xyzlut(scan).sum() > 0:
        pass
    
    destaggered_cartisian = destagger(info=metadata, fields=xyzlut(scan))

    # rprint(destaggered_cartisian.shape)


plt.imshow(xyzlut(scan)[:, :, 1], interpolation="nearest")
plt.show()

    # break

# for pd in packet_data:
#     # with warnings.catch_warnings(record=True):
#     #     warnings.simplefilter("ignore")
#     packet = LidarPacket(pd, info=metadata, _raise_on_id_check=False)

#     client.core.PacketSource(packet)

#     if isinstance(packet, client.LidarPacket):
#         # Now we can process the LidarPacket. In this case, we access
#         # the measurement ids, timestamps, and ranges
#         measurement_ids = packet.measurement_id
#         timestamps = packet.timestamp
#         ranges = packet.field(client.ChanField.RANGE)
#         # print(f"  encoder counts = {measurement_ids.shape}")
#         # print(f"  timestamps = {timestamps.shape}")
#         # print(f"  ranges = {ranges.shape}")
#         # print(packet)

#         ls_write = ls_write or client._client.LidarScan(h, w, _fields)

#         if batch(packet._data, ls_write):
#             rprint("true")
#             # Got a new frame, return it and start another
#             if ls_write.complete(column_window):
#                 rprint(ls_write)

#             ls_write = None


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
