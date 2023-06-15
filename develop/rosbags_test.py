"""Example: Register types from msg files."""

from pathlib import Path

from rosbags.typesys import get_types_from_msg, register_types


def guess_msgtype(path: Path) -> str:
    """Guess message type name from path."""
    name = path.relative_to(path.parents[2]).with_suffix("")
    if "msg" not in name.parts:
        name = name.parent / "msg" / name.name
    return str(name)


add_types = {}

for pathstr in Path("/workspaces/molisensext_analysis/data/0external/lufft_wsx_interfaces/msg").glob('**/*'):
    msgpath = Path(pathstr)
    msgdef = msgpath.read_text(encoding="utf-8")
    add_types.update(get_types_from_msg(msgdef, guess_msgtype(msgpath)))

register_types(add_types)

# Type import works only after the register_types call,
# the classname is derived from the msgtype names above.

# pylint: disable=no-name-in-module,wrong-import-position
# from rosbags.typesys.types import custom_msgs__msg__Accel as Accel  # type: ignore  # noqa
# from rosbags.typesys.types import custom_msgs__msg__Speed as Speed  # type: ignore  # noqa

# pylint: enable=no-name-in-module,wrong-import-position





from rosbags.rosbag2 import Reader
from rosbags.serde import deserialize_cdr

# create reader instance and open for reading
with Reader(
    "/workspaces/molisensext_analysis/data/0external/ubuntu2004_bagfiles/molisens_met_2023_04_14-09_23_34_convert_time"
) as reader:
    # topic and msgtype information is available on .connections list
    for connection in reader.connections:
        print(connection.topic, connection.msgtype)

    tops = []
    # iterate over messages
    for connection, timestamp, rawdata in reader.messages():
        tops.append(connection.topic)
        if connection.topic == "/sensing/aws/ws100_measurements":
            msg = deserialize_cdr(rawdata, connection.msgtype)
            print(msg)
            try:
                print(msg.header.frame_id)
            except AttributeError as e:
                print(e)

print(set(tops))





    # messages() accepts connection filters
    connections = [x for x in reader.connections if x.topic == "/imu_raw/Imu"]
    for connection, timestamp, rawdata in reader.messages(connections=connections):
        msg = deserialize_cdr(rawdata, connection.msgtype)
        try:
            print(msg.header.frame_id)
        except AttributeError:
            pass


# Highlivel
from pathlib import Path

from rosbags.highlevel import AnyReader

# create reader instance and open for reading
with AnyReader(
    [
        Path(
            "/workspaces/molisensext_analysis/data/1raw/molisens_met_2023_03_27-12_33_46_converted_2"
        )
    ]
) as reader:
    connections = [x for x in reader.connections if x.topic == "/imu_raw/Imu"]
    for connection, timestamp, rawdata in reader.messages(connections=connections):
        msg = reader.deserialize(rawdata, connection.msgtype)
        print(msg.header.frame_id)








def unpack_object_to_dict(obj):
    data = {}

    for field, value in obj.__dict__.items():
        if field == "header" or field == "__msgtype__":
            continue
        try:
            data[field] = unpack_object_to_dict(value)
        except AttributeError:
            if field.endswith("_valid") and value == True:
                data[field.rsplit("_", 1)[0]] = getattr(obj, field.rsplit("_", 1)[0])
    return data

data = {}

with Reader(bag_file) as reader:
    connections = [x for x in reader.connections if x.topic == "/sensing/aws/ws100_measurements"]
    for connection, timestamp, rawdata in reader.messages(connections=connections):
        msg = deserialize_cdr(rawdata, connection.msgtype)
        # print(msg.header.frame_id)
        # rprint(msg)
        timestamp = pd.to_datetime(
            msg.header.stamp.sec * 1e9 + msg.header.stamp.nanosec,
            unit="ns",
            origin="unix",
        )

        msg_data = unpack_object_to_dict(msg)
        if len(msg_data) == 0:
            continue

        data[timestamp] = msg_data
index = list(data.keys())
columns = pd.MultiIndex.from_product([data[index[0]].keys(), [k for v in data[index[0]].values() for k in v.keys()]])
df = pd.DataFrame(index=index, columns=columns)

# populate the DataFrame with values
for idx, val in data.items():
    for measure, subdict in val.items():
        for submeasure, value in subdict.items():
            df.loc[idx, (measure, submeasure)] = value

# drop the empty columns
df.dropna(how="all", axis=1, inplace=True)
df