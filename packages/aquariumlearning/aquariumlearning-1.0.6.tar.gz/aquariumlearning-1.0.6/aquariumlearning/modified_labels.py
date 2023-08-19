from __future__ import annotations
from typing import Any, Dict, List, Optional, Tuple, Union

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
from .labels import _Label

from .util import (
    KEYPOINT_KEYS,
    POLYGON_VERTICES_KEYS,
    ResizeMode,
    InstanceSegInstance,
    PartialInstanceSegInstance as PartialInstanceSegInstance,
)


class _ModifiedLabel:
    pass


class ModifiedBbox2DLabel(_ModifiedLabel, _Bbox2D):
    """Create a modification to an existing 2D bounding box. If the id does not already exist on the frame, it will be dropped.

    Args:
        id: Id of the label to modify.
        classification: (optional) The classification of this label
        top: (optional) The top of the box in pixels
        left: (optional) The left of the box in pixels
        width: (optional) The width of the box in pixels
        height: (optional) The height of the box in pixels
        sensor_id: (optional) The id of the sensor data to attach this label to.
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: Optional[str] = None,
        top: Optional[Union[int, float]] = None,
        left: Optional[Union[int, float]] = None,
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        sensor_id: Optional[str] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        super(ModifiedBbox2DLabel, self).__init__(
            "MODIFY",
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


class ModifiedLineSegment2DLabel(_ModifiedLabel, _LineSegment2D):
    """Create a modification to an existing 2D line segment. If the id does not already exist on the frame, it will be dropped.

    Args:
        id: Id of the label to modify.
        classification: (optional) The classification of this label
        x1: (optional) The x-coord of the first vertex in pixels
        y1: (optional) The x-coord of the first vertex in pixels
        x2: (optional) The x-coord of the first vertex in pixels
        y2: (optional) The x-coord of the first vertex in pixels
        sensor_id: (optional) The id of the sensor data to attach this label to
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: Optional[str] = None,
        x1: Optional[Union[int, float]] = None,
        y1: Optional[Union[int, float]] = None,
        x2: Optional[Union[int, float]] = None,
        y2: Optional[Union[int, float]] = None,
        sensor_id: Optional[str] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        super(ModifiedLineSegment2DLabel, self).__init__(
            "MODIFY",
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


class ModifiedKeypoint2DLabel(_ModifiedLabel, _Keypoint2D):
    """Create a modification to an existing 2D keypoint. If the id does not already exist on the frame, it will be dropped.

    A keypoint is a dictionary of the form:
        'x': x-coordinate in pixels
        'y': y-coordinate in pixels
        'name': string name of the keypoint

    Args:
        id: Id which is unique across datasets and inferences.
        classification: (optional) The classification of this label
        keypoints: (optional) The keypoints of this detection
        top: (optional) The top of the bounding box in pixels. Defaults to None.
        left: (optional) The left of the bounding box in pixels. Defaults to None.
        width: (optional) The width of the bounding box in pixels. Defaults to None.
        height: (optional) The height of the bounding box in pixels. Defaults to None.
        polygons: (optional) The polygon geometry. Defaults to None.
        sensor_id: (optional) The id of the sensor data to attach this label to
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        center: (optional) The center point of the polygon instance. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: Optional[str] = None,
        keypoints: Optional[List[Dict[KEYPOINT_KEYS, Union[int, float, str]]]] = None,
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
        super(ModifiedKeypoint2DLabel, self).__init__(
            "MODIFY",
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


class ModifiedPolygonList2DLabel(_ModifiedLabel, _PolygonList2D):
    """Create a modification to an existing 2D polygon list. If the id does not already exist on the frame, it will be dropped.

    Polygons are dictionaries of the form:
        'vertices': List of (x, y) vertices (e.g. [[x1,y1], [x2,y2], ...])
            The polygon does not need to be closed with (x1, y1).
            As an example, a bounding box in polygon representation would look like:

            .. code-block::

                {
                    'vertices': [
                        [left, top],
                        [left + width, top],
                        [left + width, top + height],
                        [left, top + height]
                    ]
                }

    Args:
        id: Id which is unique across datasets and inferences.
        classification: (optional) The classification of this label
        polygons: (optional) The polygon geometry.
        center: (optional) The center point of the polygon instance. Defaults to None.
        sensor_id: (optional) The id of the sensor data to attach this label to
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: Optional[str] = None,
        polygons: Optional[
            List[Dict[POLYGON_VERTICES_KEYS, List[Coordinate2D]]]
        ] = None,
        center: Optional[List[Union[int, float]]] = None,
        sensor_id: Optional[str] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> None:
        super(ModifiedPolygonList2DLabel, self).__init__(
            "MODIFY",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            polygons=polygons,
            center=center,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class ModifiedSemseg2DLabel(_ModifiedLabel, _Semseg2D):
    """Create a modification to an existing 2D semseg mask.

    Args:
        id: Id which is unique across datasets and inferences.
        mask_url: (optional) URL to the pixel mask png.
        resize_mode (Optional[ResizeMode]): (optional) If the mask is a different size from the base image, define how to display it. "fill" will stretch the mask to fit the base image dimensions. None will do nothing.
        sensor_id: (optional) The id of the sensor data to attach this label to
    """

    def __init__(
        self,
        *,
        id: str,
        mask_url: Optional[str] = None,
        resize_mode: Optional[ResizeMode] = None,
        sensor_id: Optional[str] = None,
    ):
        super(ModifiedSemseg2DLabel, self).__init__(
            "MODIFY",
            id=id,
            sensor_id=sensor_id,
            mask_url=mask_url,
            resize_mode=resize_mode,
        )


class ModifiedInstanceSeg2DLabel(_ModifiedLabel, _InstanceSeg2D):
    """Create a modification to an existing 2D instance segmentation label.

    Args:
        id: Id which is unique across datasets and inferences.
        mask_url: (optional) URL to the pixel mask png.
        instances: (optional) A list of instances present in the mask
        resize_mode (Optional[ResizeMode]): (optional) If the mask is a different size from the base image, define how to display it. "fill" will stretch the mask to fit the base image dimensions. None will do nothing.
        sensor_id: (optional) The id of the sensor data to attach this label to
    """

    def __init__(
        self,
        *,
        id: str,
        mask_url: Optional[str] = None,
        instances: Optional[
            List[Union[PartialInstanceSegInstance, InstanceSegInstance]]
        ] = None,
        resize_mode: Optional[ResizeMode] = None,
        sensor_id: Optional[str] = None,
    ):
        super(ModifiedInstanceSeg2DLabel, self).__init__(
            "MODIFY",
            id=id,
            sensor_id=sensor_id,
            mask_url=mask_url,
            instances=instances,
            resize_mode=resize_mode,
        )


class ModifiedClassification2DLabel(_ModifiedLabel, _Classification2D):
    """Create a modification for an existing 2D classification label.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: (optional) The classification string
        secondary_labels: (optional) Dictionary of secondary labels
        sensor_id: (optional) The id of the sensor data to attach this label to
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: Optional[str] = None,
        secondary_labels: Optional[Dict[str, Any]] = None,
        sensor_id: Optional[str] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
    ):
        super(ModifiedClassification2DLabel, self).__init__(
            "MODIFY",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            secondary_labels=secondary_labels,
            user_attrs=user_attrs,
        )


class ModifiedClassification3DLabel(_ModifiedLabel, _Classification3D):
    """Create a modification for an existing 3D classification label.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: (optional) The classification string
        sensor_id: (optional) The id of the sensor data to attach this label to
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: Optional[str] = None,
        sensor_id: Optional[str] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
    ):
        super(ModifiedClassification3DLabel, self).__init__(
            "MODIFY",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            user_attrs=user_attrs,
        )


class ModifiedCuboid3DLabel(_ModifiedLabel, _Cuboid3D):
    """Create a modification to an existing 3D cuboid. If the id does not already exist on the frame, it will be dropped.

    Args:
        id: Id of the label to modify.
        classification: (optional) The classification of this label
        position: (optional) The position of the center of the cuboid
        dimensions: (optional) The dimensions of the cuboid
        rotation: (optional) The local rotation of the cuboid, represented as an xyzw quaternion.
        coordinate_frame_id: (optional) The id of the coordinate frame to attach this label to
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: Optional[str] = None,
        position: Optional[List[float]] = None,
        dimensions: Optional[List[float]] = None,
        rotation: Optional[List[float]] = None,
        coordinate_frame_id: Optional[str] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        super(ModifiedCuboid3DLabel, self).__init__(
            "MODIFY",
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


class ModifiedTextTokenLabel(_ModifiedLabel, _TextToken):
    """Create a modification to an existing text token label. If the id does not already exist on the frame, it will be dropped.

    Args:
        id: Id of the label to modify.
        classification: (optional) The classification of this label
        index: (optional) The index of this token in the text
        token: (optional) The text content of this token
        visible: (optional) Is this a visible token in the text
        sensor_id: (optional) The id of the sensor data to attach this label to
        iscrowd: (optional) Is this label marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional label-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: Optional[str] = None,
        index: Optional[int] = None,
        token: Optional[str] = None,
        visible: Optional[bool] = None,
        sensor_id: Optional[str] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        super(ModifiedTextTokenLabel, self).__init__(
            "MODIFY",
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


class _ModifiedLabelsSet(_BaseCropSet):
    """The internal class for organizing labels and partial labels attached to a modified frame

    :meta private:
    """

    def __init__(self, frame_id: str, dataset_client: DatasetClient):
        super().__init__(frame_id, "Inference", "ADD", dataset_client)

    def _add_crop(self, crop: _BaseCrop) -> None:
        if not isinstance(crop, (_Label, _ModifiedLabel)):
            class_name = self.__class__.__name__
            raise Exception(f"Cannot add {class_name} to a ModifiedFrame")
        return super()._add_crop(crop)


ModifiedLabel = Union[
    ModifiedBbox2DLabel,
    ModifiedLineSegment2DLabel,
    ModifiedKeypoint2DLabel,
    ModifiedPolygonList2DLabel,
    ModifiedSemseg2DLabel,
    ModifiedInstanceSeg2DLabel,
    ModifiedClassification2DLabel,
    ModifiedClassification3DLabel,
    ModifiedCuboid3DLabel,
    ModifiedTextTokenLabel,
]
