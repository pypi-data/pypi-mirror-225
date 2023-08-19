from __future__ import annotations
from typing import Any, Dict, List, Optional, Set, Tuple, Union

from .dataset_client import DatasetClient
from .base_labels import (
    Coordinate2D,
    _BaseCrop,
    _BaseSingleCrop,
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

from .sensor_data import SensorData, SensorData2D, SensorData3D
from .util import (
    DEFAULT_SENSOR_ID,
    KEYPOINT_KEYS,
    POLYGON_VERTICES_KEYS,
    ResizeMode,
    InstanceSegInstance,
)


class _Inference(_BaseSingleCrop):
    _require_confidence = True


# gross but also multi inheritance is gross
class _UnconfidentInference:
    pass


# TODO: make this less fragile??
# inheritance order matters here
# super.__init__ is called sequentially in order, and so _Inference will correctly set _require_confidence
class Bbox2DInference(_Inference, _Bbox2D):
    """Create an inference for a 2D bounding box.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this inference
        confidence: The model's confidence of the inference
        top: The top of the box in pixels
        left: The left of the box in pixels
        width: The width of the box in pixels
        height: The height of the box in pixels
        sensor_id: (optional) The id of the sensor data to attach this label to (defaults to "DEFAULT")
        iscrowd: (optional) Is this inference marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional inference-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        confidence: float,
        top: Union[int, float],
        left: Union[int, float],
        width: Union[int, float],
        height: Union[int, float],
        sensor_id: str = DEFAULT_SENSOR_ID,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        super(Bbox2DInference, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            top=top,
            left=left,
            width=width,
            height=height,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class LineSegment2DInference(_Inference, _LineSegment2D):
    """Create an inference for a 2D line segment.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this inference
        confidence: The model's confidence of the inference
        x1: The x-coord of the first vertex in pixels
        y1: The x-coord of the first vertex in pixels
        x2: The x-coord of the first vertex in pixels
        y2: The x-coord of the first vertex in pixels
        sensor_id: (optional) The id of the sensor data to attach this label to (defaults to "DEFAULT")
        iscrowd: (optional) Is this inference marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional inference-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        confidence: float,
        x1: Union[int, float],
        y1: Union[int, float],
        x2: Union[int, float],
        y2: Union[int, float],
        sensor_id: str = DEFAULT_SENSOR_ID,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        super(LineSegment2DInference, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class Keypoint2DInference(_Inference, _Keypoint2D):
    """Create an inference for a 2D Keypoint.

    A keypoint is a dictionary of the form:
        'x': x-coordinate in pixels
        'y': y-coordinate in pixels
        'name': string name of the keypoint

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this inference
        confidence: The model's confidence of the inference
        keypoints: The keypoints of this detection
        top: The top of the bounding box in pixels. Defaults to None.
        left: The left of the bounding box in pixels. Defaults to None.
        width: The width of the bounding box in pixels. Defaults to None.
        height: The height of the bounding box in pixels. Defaults to None.
        polygons: The polygon geometry. Defaults to None.
        center: The center point of the polygon instance. Defaults to None.
        sensor_id: (optional) The id of the sensor data to attach this label to (defaults to "DEFAULT")
        iscrowd: (optional) Is this inference marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional inference-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        confidence: float,
        keypoints: List[Dict[KEYPOINT_KEYS, Union[int, float, str]]],
        top: Optional[Union[int, float]] = None,
        left: Optional[Union[int, float]] = None,
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        polygons: Optional[
            List[Dict[POLYGON_VERTICES_KEYS, List[Coordinate2D]]]
        ] = None,
        center: Optional[List[Union[int, float]]] = None,
        sensor_id: str = DEFAULT_SENSOR_ID,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> None:
        super(Keypoint2DInference, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
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


class PolygonList2DInference(_Inference, _PolygonList2D):
    """Create an inference for a 2D Polygon List.

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
        classification: The classification of this inference
        confidence: The model's confidence of the inference
        polygons: The polygon geometry.
        center: The center point of the polygon instance. Defaults to None.
        sensor_id: (optional) The id of the sensor data to attach this label to (defaults to "DEFAULT")
        iscrowd: (optional) Is this inference marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional inference-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        confidence: float,
        polygons: List[Dict[POLYGON_VERTICES_KEYS, List[Coordinate2D]]],
        center: Optional[List[Union[int, float]]] = None,
        sensor_id: str = DEFAULT_SENSOR_ID,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ) -> None:
        super(PolygonList2DInference, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            polygons=polygons,
            iscrowd=iscrowd,
            center=center,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class Semseg2DInference(_UnconfidentInference, _Semseg2D):
    """
    Add an inference mask for 2D semseg.

    Args:
        id: Id which is unique across datasets and inferences.
        mask_url: URL to the pixel mask png.
        resize_mode (Optional[ResizeMode]): (optional) If the mask is a different size from the base image, define how to display it. "fill" will stretch the mask to fit the base image dimensions. None will do nothing.
        sensor_id: (optional) The id of the sensor data to attach this label to (defaults to "DEFAULT")
    """

    def __init__(
        self,
        *,
        id: str,
        mask_url: str,
        resize_mode: Optional[ResizeMode] = None,
        sensor_id: str = DEFAULT_SENSOR_ID,
    ):
        super(Semseg2DInference, self).__init__(
            "ADD",
            id=id,
            sensor_id=sensor_id,
            mask_url=mask_url,
            resize_mode=resize_mode,
        )


class InstanceSeg2DInference(_UnconfidentInference, _InstanceSeg2D):
    """Create an 2D instance segmentation inference.

    Args:
        id: Id which is unique across datasets and inferences.
        mask_url: URL to the pixel mask png.
        instances: A list of instances present in the mask
        resize_mode (Optional[ResizeMode]): (optional) If the mask is a different size from the base image, define how to display it. "fill" will stretch the mask to fit the base image dimensions. None will do nothing.
        sensor_id: (optional) The id of the sensor data to attach this label to (defaults to "DEFAULT")
    """

    def __init__(
        self,
        *,
        id: str,
        mask_url: str,
        instances: List[InstanceSegInstance],
        resize_mode: Optional[ResizeMode] = None,
        sensor_id: str = DEFAULT_SENSOR_ID,
    ):
        for instance in instances:
            if not isinstance(instance, InstanceSegInstance):
                raise Exception(
                    "Can only add InstanceSegInstance instances to a new InstanceSeg2D Label"
                )

        super(InstanceSeg2DInference, self).__init__(
            "ADD",
            id=id,
            sensor_id=sensor_id,
            mask_url=mask_url,
            instances=instances,
            resize_mode=resize_mode,
        )


class Classification2DInference(_Inference, _Classification2D):
    """Create a 2D classification inference.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification string
        confidence: The confidence between 0.0 and 1.0 of the prediction
        sensor_id: (optional) The id of the sensor data to attach this label to (defaults to "DEFAULT")
        user_attrs: (optional) Any additional inference-level metadata fields. Defaults to None.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        confidence: float,
        sensor_id: str = DEFAULT_SENSOR_ID,
        user_attrs: Optional[Dict[str, Any]] = {},
    ):
        super(Classification2DInference, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            user_attrs=user_attrs,
        )


class Classification3DInference(_Inference, _Classification3D):
    """Create a 3D classification inference.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification string
        confidence: The confidence between 0.0 and 1.0 of the prediction
        sensor_id: (optional) The id of the sensor data to attach this label to (defaults to "DEFAULT")
        user_attrs: (optional) Any additional inference-level metadata fields. Defaults to None.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        confidence: float,
        sensor_id: str = DEFAULT_SENSOR_ID,
        user_attrs: Optional[Dict[str, Any]] = {},
    ):
        super(Classification3DInference, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            user_attrs=user_attrs,
        )


class Cuboid3DInference(_Inference, _Cuboid3D):
    """Add an inference for a 3D cuboid.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this inference
        confidence: The model's confidence of the inference
        position: The position of the center of the cuboid
        dimensions: The dimensions of the cuboid
        rotation: The local rotation of the cuboid, represented as an xyzw quaternion.
        coordinate_frame_id: (optional) The id of the coordinate frame to attach this label to (defaults to "world")
        iscrowd: (optional) Is this inference marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional inference-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        confidence: float,
        position: List[float],
        dimensions: List[float],
        rotation: List[float],
        coordinate_frame_id: str = "world",
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
        embedding: Optional[List[float]] = None,
    ):
        super(Cuboid3DInference, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            coordinate_frame_id=coordinate_frame_id,
            confidence=confidence,
            position=position,
            dimensions=dimensions,
            rotation=rotation,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class TextTokenInference(_TextToken, _Inference):
    """Create a text token inference.

    Args:
        id: Id which is unique across datasets and inferences.
        classification: The classification of this inference
        confidence: The model's confidence of the inference
        index: The index of this token in the text
        token: The text content of this token
        visible: Is this a visible token in the text
        sensor_id: (optional) The id of the sensor data to attach this label to (defaults to "DEFAULT")
        iscrowd: (optional) Is this inference marked as a crowd. Defaults to None.
        user_attrs: (optional) Any additional inference-level metadata fields. Defaults to None.
        embedding: (optional) A vector of floats of at least length 2.
    """

    def __init__(
        self,
        *,
        id: str,
        classification: str,
        confidence: float,
        index: int,
        token: str,
        visible: bool,
        sensor_id: str = DEFAULT_SENSOR_ID,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
        embedding: Optional[List[float]] = None,
    ):
        super(TextTokenInference, self).__init__(
            "ADD",
            id=id,
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            index=index,
            token=token,
            visible=visible,
            iscrowd=iscrowd,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class _InferenceSet(_BaseCropSet):
    """The internal class for organizing labels attached to an inference frame

    :meta private:
    """

    def __init__(self, frame_id: str, dataset_client: DatasetClient):
        super(_InferenceSet, self).__init__(
            frame_id, "Inference", "ADD", dataset_client
        )

    def _add_crop(self, crop: _BaseCrop) -> None:
        if not isinstance(crop, (_Inference, _UnconfidentInference)):
            class_name = self.__class__.__name__
            raise Exception(f"Cannot add {class_name} to an InferenceFrame")
        return super()._add_crop(crop)


Inference = Union[
    Bbox2DInference,
    LineSegment2DInference,
    Keypoint2DInference,
    PolygonList2DInference,
    Semseg2DInference,
    InstanceSeg2DInference,
    Classification2DInference,
    Classification3DInference,
    Cuboid3DInference,
    TextTokenInference,
]
