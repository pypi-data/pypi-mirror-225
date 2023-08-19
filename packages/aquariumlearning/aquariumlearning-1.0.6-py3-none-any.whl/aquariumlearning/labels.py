from typing import Any, Dict, List, Optional, Union
from typing_extensions import TypedDict

from .dataset_client import DatasetClient
from .base_labels import (
    Coordinate2D,
    _BaseCrop,
    _BaseCropSet,
    _Bbox2D,
    _Classification2D,
    _Classification3D,
    _Cuboid3D,
    _Keypoint2D,
    _LineSegment2D,
    _PolygonList2D,
    _Semseg2D,
    _InstanceSeg2D,
    _TextToken,
)

from .util import (
    KEYPOINT_KEYS,
    POLYGON_VERTICES_KEYS,
    ResizeMode,
    InstanceSegInstance as InstanceSegInstance,
)


class _Label:
    pass


# TODO: figure out how to get nice typechecking and typehinting without having to list out these args every time
class Bbox2DLabel(_Label, _Bbox2D):
    """Create a label for a 2D bounding box.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        top: The top of the box in pixels
        left: The left of the box in pixels
        width: The width of the box in pixels
        height: The height of the box in pixels
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        top: Union[int, float],
        left: Union[int, float],
        width: Union[int, float],
        height: Union[int, float],
        sensor_id: Optional[str] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        super(Bbox2DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            top=top,
            left=left,
            width=width,
            height=height,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class LineSegment2DLabel(_Label, _LineSegment2D):
    """Create a 2D line segment label.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        x1: The x-coord of the first vertex in pixels
        y1: The x-coord of the first vertex in pixels
        x2: The x-coord of the first vertex in pixels
        y2: The x-coord of the first vertex in pixels
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        x1: Union[int, float],
        y1: Union[int, float],
        x2: Union[int, float],
        y2: Union[int, float],
        sensor_id: Optional[str] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        super(LineSegment2DLabel, self).__init__(
            "ADD",
            id,
            classification=classification,
            sensor_id=sensor_id,
            x1=x1,
            x2=x2,
            y1=y1,
            y2=y2,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class Keypoint2DLabel(_Label, _Keypoint2D):
    """Create a label for a 2D Keypoint.

    A keypoint is a dictionary of the form:
        'x': x-coordinate in pixels
        'y': y-coordinate in pixels
        'name': string name of the keypoint

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        keypoints: The keypoints of this detection
        top: The top of the bounding box in pixels. Defaults to None.
        left: The left of the bounding box in pixels. Defaults to None.
        width: The width of the bounding box in pixels. Defaults to None.
        height: The height of the bounding box in pixels. Defaults to None.
        polygons: The polygon geometry. Defaults to None.
        center: The center point of the polygon instance. Defaults to None.
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        keypoints: List[Dict[KEYPOINT_KEYS, Union[int, float, str]]],
        top: Optional[Union[int, float]] = None,
        left: Optional[Union[int, float]] = None,
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        polygons: Optional[
            List[Dict[POLYGON_VERTICES_KEYS, List[Coordinate2D]]]
        ] = None,
        center: Optional[List[Union[int, float]]] = None,
        sensor_id: Optional[str] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> None:
        super(Keypoint2DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            keypoints=keypoints,
            top=top,
            left=left,
            width=width,
            height=height,
            polygons=polygons,
            iscrowd=iscrowd,
            center=center,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class PolygonList2DLabel(_Label, _PolygonList2D):
    """Create a label for a 2D polygon list for instance segmentation

    Polygons are dictionaries of the form:
        'vertices': List of (x, y) vertices (e.g. [(x1,y1), (x2,y2), ...])
            The polygon does not need to be closed with (x1, y1).
            As an example, a bounding box in polygon representation would look like:

            .. code-block::

                {
                    'vertices': [
                        (left, top),
                        (left + width, top),
                        (left + width, top + height),
                        (left, top + height)
                    ]
                }

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        polygons: The polygon geometry.
        center: The center point of the polygon instance. Defaults to None.
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        polygons: List[Dict[POLYGON_VERTICES_KEYS, List[Coordinate2D]]],
        center: Optional[List[Union[int, float]]] = None,
        sensor_id: Optional[str] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> None:
        super(PolygonList2DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            polygons=polygons,
            center=center,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class Semseg2DLabel(_Label, _Semseg2D):
    """
    Add a mask for 2D semseg.

    Args:
        id: Id which is unique across datasets and inferences.
        mask_url: URL to the pixel mask png.
        resize_mode (Optional[ResizeMode]): (optional) If the mask is a different size from the base image, define how to display it. "fill" will stretch the mask to fit the base image dimensions. None will do nothing.
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
    """

    def __init__(
        self,
        *,
        id: str,
        mask_url: str,
        resize_mode: Optional[ResizeMode] = None,
        sensor_id: Optional[str] = None,
    ):
        super(Semseg2DLabel, self).__init__(
            "ADD",
            id=id,
            sensor_id=sensor_id,
            mask_url=mask_url,
            resize_mode=resize_mode,
        )


class InstanceSeg2DLabel(_Label, _InstanceSeg2D):
    """Create an 2D instance segmentation label.

    Args:
        id: Id which is unique across datasets and inferences.
        mask_url: URL to the pixel mask png.
        instances: A list of instances present in the mask
        resize_mode (Optional[ResizeMode]): (optional) If the mask is a different size from the base image, define how to display it. "fill" will stretch the mask to fit the base image dimensions. None will do nothing.
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
    """

    def __init__(
        self,
        *,
        id: str,
        mask_url: str,
        instances: List[InstanceSegInstance],
        resize_mode: Optional[ResizeMode] = None,
        sensor_id: Optional[str] = None,
    ):
        for instance in instances:
            if not isinstance(instance, InstanceSegInstance):
                raise Exception(
                    "Can only add InstanceSegInstance instances to a new InstanceSeg2D Label"
                )

        super(InstanceSeg2DLabel, self).__init__(
            "ADD",
            id=id,
            sensor_id=sensor_id,
            mask_url=mask_url,
            instances=instances,
            resize_mode=resize_mode,
        )


class Classification2DLabel(_Label, _Classification2D):
    """Create a 2D classification label.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification string
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        secondary_labels: (optional) Dictionary of secondary labels
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        sensor_id: Optional[str] = None,
        secondary_labels: Optional[Dict[str, Any]] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
    ):
        super(Classification2DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            secondary_labels=secondary_labels,
            user_attrs=user_attrs,
        )


class Classification3DLabel(_Label, _Classification3D):
    """Create a 3D classification label.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification string
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        sensor_id: Optional[str] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
    ):
        super(Classification3DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            user_attrs=user_attrs,
        )


class Cuboid3DLabel(_Label, _Cuboid3D):
    """Add a label for a 3D cuboid.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        position: The position of the center of the cuboid
        dimensions: The dimensions of the cuboid
        rotation: The local rotation of the cuboid, represented as an xyzw quaternion.
        coordinate_frame_id: (optional) The id of the coordinate frame to attach this label to (if not set, we will try to infer this from the frame's coordinate frames)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        position: List[float],
        dimensions: List[float],
        rotation: List[float],
        coordinate_frame_id: Optional[str] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
        embedding: Optional[List[float]] = None,
    ):
        super(Cuboid3DLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            coordinate_frame_id=coordinate_frame_id,
            position=position,
            dimensions=dimensions,
            rotation=rotation,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class TextTokenLabel(_Label, _TextToken):
    """Create a text token label.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this label
        index: The index of this token in the text
        token: The text content of this token
        visible: Is this a visible token in the text
        sensor_id: (optional) The id of the sensor data to attach this label to (if not set, we will try to infer this from the frame's sensors)
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        index: int,
        token: str,
        visible: bool,
        sensor_id: Optional[str] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
        embedding: Optional[List[float]] = None,
    ):
        super(TextTokenLabel, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            index=index,
            token=token,
            visible=visible,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class _LabeledSet(_BaseCropSet):
    """The internal class for organizing labels attached to a frame

    :meta private:
    """

    def __init__(self, frame_id: str, dataset_client: DatasetClient):
        super().__init__(frame_id, "GT", "ADD", dataset_client)

    def _add_crop(self, crop: _BaseCrop) -> None:
        if not isinstance(crop, _Label):
            class_name = self.__class__.__name__
            raise Exception(f"Cannot add {class_name} to a LabeledFrame")
        return super()._add_crop(crop)


Label = Union[
    Bbox2DLabel,
    LineSegment2DLabel,
    Keypoint2DLabel,
    PolygonList2DLabel,
    Semseg2DLabel,
    InstanceSeg2DLabel,
    Classification2DLabel,
    Classification3DLabel,
    Cuboid3DLabel,
    TextTokenLabel,
]


class _CommonLabelKwargs(TypedDict):
    id: str
    classification: str
    sensor_id: str
    user_attrs: Dict[str, Any]


def _get_single_label_from_json(label_json: Dict[str, Any]) -> Label:
    label_type = label_json["label_type"]

    iscrowd = label_json["attributes"].pop("iscrowd", None)
    user_attrs = {
        key: value
        for key, value in label_json["attributes"].items()
        if key.startswith("user__")
    }
    base_label_kwargs = _CommonLabelKwargs(
        id=label_json["uuid"],
        classification=label_json["label"],
        sensor_id=label_json["label_coordinate_frame"],
        user_attrs=user_attrs,
    )

    if label_type == "BBOX_2D":
        top = label_json["attributes"]["top"]
        left = label_json["attributes"]["left"]
        width = label_json["attributes"]["width"]
        height = label_json["attributes"]["height"]
        return Bbox2DLabel(
            **base_label_kwargs,
            iscrowd=iscrowd,
            top=top,
            left=left,
            width=width,
            height=height,
        )
    elif label_type == "LINE_SEGMENT_2D":
        x1 = label_json["attributes"]["x1"]
        y1 = label_json["attributes"]["y1"]
        x2 = label_json["attributes"]["x2"]
        y2 = label_json["attributes"]["y2"]
        return LineSegment2DLabel(
            **base_label_kwargs, iscrowd=iscrowd, x1=x1, y1=y1, x2=x2, y2=y2
        )
    elif label_type == "KEYPOINTS_2D":
        keypoints = label_json["attributes"]["keypoints"]
        top = label_json["attributes"].get("top")
        left = label_json["attributes"].get("left")
        width = label_json["attributes"].get("width")
        height = label_json["attributes"].get("height")
        polygons = label_json["attributes"].get("polygons")
        center = label_json["attributes"].get("center")
        return Keypoint2DLabel(
            **base_label_kwargs,
            iscrowd=iscrowd,
            keypoints=keypoints,
            top=top,
            left=left,
            width=width,
            height=height,
            polygons=polygons,
            center=center,
        )
    elif label_type == "POLYGON_LIST_2D":
        polygons = label_json["attributes"]["polygons"]
        center = label_json["attributes"].get("center")
        return PolygonList2DLabel(
            **base_label_kwargs, iscrowd=iscrowd, polygons=polygons, center=center
        )
    elif label_type == "SEMANTIC_LABEL_URL_2D":
        mask_url = label_json["attributes"]["url"]
        resize_mode = label_json["attributes"].get("resize_mode")
        return Semseg2DLabel(
            id=label_json["uuid"],
            mask_url=mask_url,
            resize_mode=resize_mode,
            sensor_id=label_json["label_coordinate_frame"],
        )
    elif label_type == "CLASSIFICATION_2D":
        secondary_labels = {
            key: value
            for key, value in label_json["attributes"].items()
            if not key.startswith("user__") and not key.startswith("derived__")
        }
        return Classification2DLabel(
            **base_label_kwargs, secondary_labels=secondary_labels
        )
    elif label_type == "CLASSIFICATION_3D":
        return Classification3DLabel(**base_label_kwargs)
    elif label_type == "CUBOID_3D":
        pos_x = label_json["attributes"]["pos_x"]
        pos_y = label_json["attributes"]["pos_y"]
        pos_z = label_json["attributes"]["pos_z"]
        position = [pos_x, pos_y, pos_z]
        dim_x = label_json["attributes"]["dim_x"]
        dim_y = label_json["attributes"]["dim_y"]
        dim_z = label_json["attributes"]["dim_z"]
        dimensions = [dim_x, dim_y, dim_z]
        rot_x = label_json["attributes"]["rot_x"]
        rot_y = label_json["attributes"]["rot_y"]
        rot_z = label_json["attributes"]["rot_z"]
        rot_w = label_json["attributes"]["rot_w"]
        rotation = [rot_x, rot_y, rot_z, rot_w]

        return Cuboid3DLabel(
            id=label_json["uuid"],
            classification=label_json["label"],
            coordinate_frame_id=label_json["label_coordinate_frame"],
            position=position,
            dimensions=dimensions,
            rotation=rotation,
            user_attrs=user_attrs,
        )
    elif label_type == "TEXT_TOKEN":
        index = label_json["attributes"]["index"]
        token = label_json["attributes"]["token"]
        visible = label_json["attributes"]["visible"]
        return TextTokenLabel(
            **base_label_kwargs, index=index, token=token, visible=visible
        )
    else:
        raise Exception(f"Cannot reinstantiate a label of type {label_type}")


def _get_instance_seg_label_from_jsons(
    mask_json: Dict[str, Any],
    instances: List[Dict[str, Any]],
) -> InstanceSeg2DLabel:
    instantiated_instances = []
    for ins in instances:
        id: int = ins["attributes"].pop("id")
        instantiated_instances.append(
            InstanceSegInstance(id, ins["classification"], ins["attributes"])
        )
    label = InstanceSeg2DLabel(
        id=mask_json["uuid"],
        sensor_id=mask_json["label_coordinate_frame"],
        instances=instantiated_instances,
        **mask_json["attributes"],
    )
    return label
