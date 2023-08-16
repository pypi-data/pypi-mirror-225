import os
import streamlit.components.v1 as components
import pandas as pd
import base64
import io
from PIL import Image
import matplotlib.pyplot as plt
from io import BytesIO
from typing import TypedDict, List

_RELEASE = True


if not _RELEASE:
    _component_func = components.declare_component(
        "st_track_viewer",
        url="http://localhost:3000",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("st_track_viewer", path=build_dir)


class HeaderDictType(TypedDict):
    date: str
    min: int
    sec: int
    versions: List[str]
    types: List[str]
    filter: dict[str, int]


def process_tracks(tracks: pd.DataFrame):
    grouped = tracks.groupby("Id")

    result_tuples = []

    for group_id, group_data in grouped:
        timestamps = group_data.index.strftime("%Y-%m-%dT%H:%M:%S.%f").tolist()
        x_list = group_data["X"].tolist()
        y_list = group_data["Y"].tolist()
        speed_key = None
        for column in group_data.columns:
            if column.startswith("Speed"):
                speed_key = column
                break
        speed = group_data[speed_key].tolist()
        estimated_list = group_data["Estimated"].tolist()
        track_type = group_data["Class_id"].tolist()

        result_tuple = (
            group_id,
            timestamps,
            [x_list, y_list],
            speed,
            estimated_list,
            track_type,
        )
        result_tuples.append(result_tuple)
    return result_tuples


def st_track_viewer(
    data: HeaderDictType,
    tracks=[],
    grounds=[],
    images=[],
    shapes=[],
    names=[],
    key=None,
):
    if not (
        len(tracks) == len(grounds)
        and len(tracks) == len(images)
        and len(tracks) == len(shapes)
    ):
        raise ValueError(
            f"""Length of tracks, grounds, images, shapes and names must be equal:
                         Tracks length: {len(tracks)}
                         Grounds length: {len(grounds)}
                         Images length: {len(images)}
                         Shapes length: {len(shapes)}
                         Names length: {len(names)}"""
        )
    ims = []
    # Convert images into url strings
    for im in images:
        buffer = BytesIO()
        plt.imsave(buffer, im, cmap="gray", format="png")
        base64_string = base64.b64encode(buffer.getvalue()).decode()
        mime_type = "image/png"
        url_string = f"data:{mime_type};base64,{base64_string}"
        ims.append(url_string)
    component_value = _component_func(
        tracks=tracks,
        data=data,
        images=ims,
        grounds=grounds,
        shapes=shapes,
        names=names,
        key=key,
        default=0,
    )
    return component_value


# Test code
if not _RELEASE:
    import streamlit as st

    st.set_page_config(layout="wide")
    image = plt.imread("./assets/ground.png")
    image2 = plt.imread("./assets/ground2.png")
    if "data" not in st.session_state:
        st.session_state["data"]: HeaderDictType = {
            "date": "2023-05-03T10:10:00",
            "min": 10,
            "sec": 0,
            "versions": ["A1"],
            "types": [
                "Unknown",
                "Bicycle",
                "Pedestrian",
                "Light vehicle",
                "Heavy vehicle",
            ],
            "filter": {"filter": False, "minLength": 0, "maxLength": 100},
        }
    folder_path = "./CSV2"
    folder_path2 = "./CSV"
    csv_files = os.listdir(folder_path)
    csv_files2 = os.listdir(folder_path2)
    keys = list(map(lambda string: string.split("_")[0], csv_files))
    keys2 = list(map(lambda string: string.split("_")[0], csv_files2))

    if "track_data" not in st.session_state:
        track_data = {}

        for file_name in csv_files:
            if file_name.endswith(".csv"):
                date_str = file_name.split("_")[0]
                date_key = pd.to_datetime(date_str).date().isoformat()
                file_path = os.path.join(folder_path, file_name)
                tracks = pd.read_csv(
                    file_path, sep=";", parse_dates=["Time"]
                ).set_index("Time")
                track_data[date_key] = tracks
        st.session_state["track_data"] = track_data
    _tracks = (
        process_tracks(
            st.session_state.track_data[st.session_state.data["date"].split("T")[0]]
        )
        if st.session_state.data["date"].split("T")[0] in keys
        else []
    )

    ground = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 30.0, 27.0]
    ground2 = [[0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 90.35000000000001, 82.55000000000001]

    shape1 = [600, 540]
    shape2 = [1807, 1651]
    tracks = [
        _tracks,
    ]

    grounds = [
        ground,
    ]
    shapes = [
        shape1,
    ]
    images = [
        image,
    ]
    names = [
        "A1",
    ]
    key = st_track_viewer(
        tracks=tracks,
        data=st.session_state.data,
        images=images,
        grounds=grounds,
        shapes=shapes,
        names=names,
    )
    if (
        key != 0
        and "data" in st.session_state
        and not st.session_state.data["date"] == key["date"]
    ):
        st.session_state.data = key
        st.experimental_rerun()
    else:
        pass
