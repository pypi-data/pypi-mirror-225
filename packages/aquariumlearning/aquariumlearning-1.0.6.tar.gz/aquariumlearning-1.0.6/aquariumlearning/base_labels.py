"""
Internal label type classes for creating labels and inferences
"""
import numbers
from typing import Any, Dict, List, Optional, Set, Tuple, Type, Union
from typing_extensions import Literal

from .coordinate_frames import (
    _BaseCoordinateFrame3D,
    _BaseCoordinateFrame2D,
    _BaseCoordinateFrame,
)
from .dataset_client import DatasetClient
from .sensor_data import (
    _BaseSensor,
    _BaseSensor2D,
    _BaseSensor3D,
)
from .util import (
    _BaseEntity,
    BaseLabelAssetDict,
    InstanceSegInstance,
    PartialInstanceSegInstance,
    LabelFrameSummary,
    LabelType,
    UpdateType,
    ResizeMode,
    add_object_user_attrs,
    is_valid_number,
    is_valid_float,
    KEYPOINT_KEYS,
    POLYGON_VERTICES_KEYS,
)

CropType = Literal["GT", "Inference"]

Sensor = Union[
    Type[_BaseSensor],
    Type[_BaseSensor2D],
    Type[_BaseSensor3D],
]

CoordinateFrameType = Union[
    Type[_BaseCoordinateFrame],
    Type[_BaseCoordinateFrame2D],
    Type[_BaseCoordinateFrame3D],
]

FRIENDLY_SENSOR_NAMES: Dict[Sensor, str] = {
    _BaseSensor2D: "2D Sensor Data",
    _BaseSensor3D: "3D Sensor Data",
    _BaseSensor: ", ".join(["2D Sensor Data", "3D Sensor Data"]),
}

Coordinate2D = Tuple[Union[int, float], Union[int, float]]


class LabelAsset(BaseLabelAssetDict):
    pass


class _BaseSingleCrop(_BaseEntity):
    """The base class for all crops (labels and inferences)

    :meta private:
    """

    # at add to frame time, make sure that this crop is attached to a supported sensor_data type
    _valid_sd_classes: Optional[Set[Sensor]] = None
    # at add to frame time, make sure that this crop is attached to a supported coordinate_frame type
    _valid_cf_classes: Optional[Set[CoordinateFrameType]] = None
    # in general, whether we should infer a coordinate frame or a sensor data association
    _add_to_sensor: bool = True
    _add_to_coordinate_frame: bool = False
    # check if confidence is required
    _require_confidence: Optional[bool] = False
    classification: Optional[str] = None
    classification_id: Optional[int] = None  # to also pass to the backend?
    embedding: Optional[List[float]] = None
    embedding_dim: Optional[int] = None
    label_type: LabelType

    def __init__(
        self,
        id: str,
        update_type: UpdateType,
        label_type: LabelType,
        classification: Optional[str] = None,
        sensor_id: Optional[str] = None,
        coordinate_frame_id: Optional[str] = None,
        confidence: Optional[float] = None,
        iscrowd: Optional[bool] = None,
        attributes: Optional[Dict[str, Any]] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        super().__init__(id)

        # validate that we're passing the right flag
        if update_type == "ADD":
            required: Dict[str, Any] = {
                "classification": classification,
            }
            if self._require_confidence:
                required["confidence"] = confidence

            not_passed = [k for k in required if required[k] is None]
            if not_passed:
                raise Exception(
                    f"Cannot create a new crop without the following kwargs defined: {not_passed}"
                )

        if attributes is None:
            attributes = {}

        if confidence is not None:
            if not is_valid_float(confidence):
                raise Exception("confidence must be floats")
            if confidence < 0.0 or confidence > 1.0:
                raise Exception("confidence must be between 0.0 and 1.0")

            attributes["confidence"] = confidence

        if iscrowd is not None:
            attributes["iscrowd"] = iscrowd

        if classification is not None and not isinstance(classification, str):
            raise Exception("classifications must be strings")

        add_object_user_attrs(attributes, user_attrs)

        self.label_type = label_type
        self.classification = classification
        self.sensor_id = sensor_id
        self.coordinate_frame_id = coordinate_frame_id
        self.update_type = update_type
        self.attributes = attributes
        self.reuse_latest_embedding = update_type == "MODIFY" and not embedding
        self.embedding_dim = -1

        if embedding:
            self._add_embedding(embedding)

    def _add_embedding(self, embedding: List[float]) -> None:
        if len(embedding) <= 1:
            raise Exception("Length of embeddings should be at least 2.")

        for embedding_el in embedding:
            if not isinstance(embedding_el, numbers.Number):
                raise Exception(
                    f"Unexpectedly encountered a {type(embedding[0])} element. Only flat arrays of numbers are supported for embeddings."
                )

        if not self.embedding:
            self.embedding_dim = len(embedding)
            self.embedding = embedding
        else:
            raise Exception("An embedding has already been added to this label")

    def to_dict(self) -> Dict[str, Any]:
        label_dict = {
            "uuid": self.id,
            "label_type": self.label_type,
            "label": self.classification,
            "class_id": self.classification_id,
            "label_coordinate_frame": self.sensor_id or self.coordinate_frame_id,
            "attributes": self.attributes,
            "reuse_latest_embedding": self.reuse_latest_embedding,
            "change": self.update_type,
        }

        if self.update_type == "MODIFY":
            # only return the fields that are populated
            return {k: v for k, v in label_dict.items() if v is not None}
        return label_dict


class _BaseMultiCrop(_BaseEntity):
    """The base class for crop types that result in multiple crops (mainly instance segmentation)

    :meta private:
    """

    _crops: List[_BaseSingleCrop]

    def __init__(self, id: str):
        super().__init__(id)
        self._crops = []


_BaseCrop = Union[_BaseSingleCrop, _BaseMultiCrop]


class _Bbox2D(_BaseSingleCrop):
    """The base class for 2D bboxes (labels and inferences) to attach to frames

    :meta private:
    """

    _valid_sd_classes = {_BaseSensor2D}

    def __init__(
        self,
        update_type: UpdateType,
        id: str,
        classification: Optional[str] = None,
        sensor_id: Optional[str] = None,
        confidence: Optional[float] = None,
        top: Optional[Union[int, float]] = None,
        left: Optional[Union[int, float]] = None,
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        for dim in [top, left, width, height]:
            if update_type == "MODIFY" and dim is None:
                continue
            if not is_valid_number(dim):
                raise Exception("all bounding box dimensions must be valid int/float")

        dim_attrs = {
            "top": top,
            "left": left,
            "width": width,
            "height": height,
        }
        attributes = {k: v for k, v in dim_attrs.items() if v is not None}

        super().__init__(
            id,
            update_type,
            label_type="BBOX_2D",
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            iscrowd=iscrowd,
            attributes=attributes,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class _LineSegment2D(_BaseSingleCrop):
    """The base class for 2D line segments (labels and inferences) to attach to frames

    :meta private:
    """

    _valid_sd_classes = {_BaseSensor2D}

    def __init__(
        self,
        update_type: UpdateType,
        id: str,
        classification: Optional[str] = None,
        sensor_id: Optional[str] = None,
        confidence: Optional[float] = None,
        x1: Optional[Union[int, float]] = None,
        y1: Optional[Union[int, float]] = None,
        x2: Optional[Union[int, float]] = None,
        y2: Optional[Union[int, float]] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        for coord in [x1, y1, x2, y2]:
            if update_type == "MODIFY" and coord is None:
                continue
            if not is_valid_number(coord):
                raise Exception("all line segment coordinates must be valid int/float")

        coord_attrs = {"x1": x1, "y1": y1, "x2": x2, "y2": y2}
        attributes = {k: v for k, v in coord_attrs.items() if v is not None}

        super().__init__(
            id,
            update_type,
            label_type="LINE_SEGMENT_2D",
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            iscrowd=iscrowd,
            attributes=attributes,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class _Keypoint2D(_BaseSingleCrop):
    """The base class for 2D keypoints (labels and inferences) to attach to frames

    :meta private:
    """

    _valid_sd_classes = {_BaseSensor}

    def __init__(
        self,
        update_type: UpdateType,
        id: str,
        classification: Optional[str] = None,
        sensor_id: Optional[str] = None,
        confidence: Optional[float] = None,
        keypoints: Optional[List[Dict[KEYPOINT_KEYS, Union[int, float, str]]]] = None,
        top: Optional[Union[int, float]] = None,
        left: Optional[Union[int, float]] = None,
        width: Optional[Union[int, float]] = None,
        height: Optional[Union[int, float]] = None,
        polygons: Optional[
            List[Dict[POLYGON_VERTICES_KEYS, List[Coordinate2D]]]
        ] = None,
        center: Optional[List[Union[int, float]]] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        attributes: Dict[str, Any] = {}
        if keypoints:
            keypoint_names_set = set()
            for keypoint in keypoints:
                x = keypoint["x"]
                y = keypoint["y"]
                name = keypoint["name"]
                if not is_valid_number(x):
                    raise Exception("keypoint x coordinate must be valid int/float")
                if not is_valid_number(y):
                    raise Exception("keypoint y coordinate must be valid int/float")
                if not isinstance(name, str) or len(name) == 0:
                    raise Exception("keypoint name must be non-zero length string")
                if name in keypoint_names_set:
                    raise Exception("keypoint names must be unique within a label")
                keypoint_names_set.add(name)

            attributes["keypoints"] = keypoints

        box = {"top": top, "left": left, "width": width, "height": height}
        non_none_dims = [dim != None for dim in box.values()]
        if any(non_none_dims) and (update_type != "ADD" or all(non_none_dims)):
            for key, dim in box.items():
                if update_type == "MODIFY" and dim is None:
                    continue
                if not is_valid_number(dim):
                    raise Exception(
                        "all bounding box dimensions must be valid int/float"
                    )
                attributes[key] = dim

        if polygons:
            for polygon in polygons:
                for vertex in polygon["vertices"]:
                    for num in vertex:
                        if not is_valid_number(num):
                            raise Exception(
                                "all polygon vertex coordinates must be valid int/float"
                            )
            attributes["polygons"] = polygons

        if center is not None:
            for num in center:
                if not is_valid_number(num):
                    raise Exception(
                        "polygon center coordinates must be valid int/float"
                    )
            attributes["center"] = center

        super().__init__(
            id,
            update_type,
            label_type="KEYPOINTS_2D",
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            iscrowd=iscrowd,
            attributes=attributes,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class _PolygonList2D(_BaseSingleCrop):
    """The base class for 2D polygon lists (labels and inferences) to attach to frames

    :meta private:
    """

    _valid_sd_classes = {_BaseSensor}

    def __init__(
        self,
        update_type: UpdateType,
        id: str,
        classification: Optional[str] = None,
        sensor_id: Optional[str] = None,
        confidence: Optional[float] = None,
        polygons: Optional[
            List[Dict[POLYGON_VERTICES_KEYS, List[Coordinate2D]]]
        ] = None,
        center: Optional[List[Union[int, float]]] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = None,
        embedding: Optional[List[float]] = None,
    ):
        if polygons:
            for polygon in polygons:
                for vertex in polygon["vertices"]:
                    for num in vertex:
                        if not is_valid_number(num):
                            raise Exception(
                                "all polygon vertex coordinates must be valid int/float"
                            )

        if center is not None:
            for num in center:
                if not is_valid_number(num):
                    raise Exception(
                        "polygon center coordinates must be valid int/float"
                    )

        attributes: Dict[str, Any] = {"polygons": polygons, "center": center}

        super().__init__(
            id,
            update_type,
            label_type="POLYGON_LIST_2D",
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            iscrowd=iscrowd,
            attributes=attributes,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class _Semseg2D(_BaseSingleCrop):
    """The base class for segmentation masks (labels and inferences) to attach to frames

    :meta private:
    """

    _valid_sd_classes = {_BaseSensor}

    # TODO: start supporting mask_data again
    def __init__(
        self,
        update_type: UpdateType,
        id: str,
        sensor_id: Optional[str] = None,
        mask_url: Optional[str] = None,
        resize_mode: Optional[ResizeMode] = None,
    ):
        attributes = {}
        if mask_url:
            attributes["url"] = mask_url
        if resize_mode:
            attributes["resize_mode"] = resize_mode

        super().__init__(
            id,
            update_type,
            label_type="SEMANTIC_LABEL_URL_2D",
            classification="__mask",
            sensor_id=sensor_id,
            confidence=None,
            iscrowd=None,
            attributes=attributes,
        )


class _InstanceSegMask2D(_BaseSingleCrop):
    """The base class for instance segmentation masks (labels and inferences) to attach to frames

    :meta private:
    """

    _valid_sd_classes = {_BaseSensor}

    # TODO: start supporting mask_data again
    def __init__(
        self,
        update_type: UpdateType,
        id: str,
        sensor_id: Optional[str] = None,
        mask_url: Optional[str] = None,
        resize_mode: Optional[ResizeMode] = None,
    ):
        attributes = {}
        if mask_url:
            attributes["url"] = mask_url
        if resize_mode:
            attributes["resize_mode"] = resize_mode

        super().__init__(
            id,
            update_type,
            label_type="INSTANCE_LABEL_URL_2D",
            classification="__mask",
            sensor_id=sensor_id,
            confidence=None,
            iscrowd=None,
            attributes=attributes,
        )


class _InstanceSegInstance(_BaseSingleCrop):
    """The base class for instance segmentation instances (labels and inferences) to attach to frames

    :meta private:
    """

    _valid_sd_classes = {_BaseSensor}


class _InstanceSeg2D(_BaseMultiCrop):
    """The base class for instance segmentation masks and instances (labels and inferences) to attach to frames

    :meta private:
    """

    def __init__(
        self,
        update_type: UpdateType,
        id: str,
        sensor_id: Optional[str] = None,
        mask_url: Optional[str] = None,
        instances: Optional[
            Union[
                List[InstanceSegInstance],
                List[Union[PartialInstanceSegInstance, InstanceSegInstance]],
            ]
        ] = None,
        resize_mode: Optional[ResizeMode] = None,
    ):
        super().__init__(id)
        if mask_url:
            self._crops.append(
                _InstanceSegMask2D(
                    id=id,
                    update_type=update_type,
                    sensor_id=sensor_id,
                    mask_url=mask_url,
                    resize_mode=resize_mode,
                )
            )
        if instances:
            for instance in instances:
                attributes: Dict[str, Any] = {"id": instance.id}
                if resize_mode is not None:
                    attributes["resize_mode"] = resize_mode
                instance_crop = _InstanceSegInstance(
                    f"{id}_{instance.id}",
                    update_type,
                    label_type="INSTANCE_LABEL_2D",
                    classification=instance.classification,
                    sensor_id=sensor_id,
                    confidence=None,
                    iscrowd=None,
                    attributes=attributes,
                    user_attrs=instance.attributes,
                )
                self._crops.append(instance_crop)


class _Classification2D(_BaseSingleCrop):
    _valid_sd_classes = {_BaseSensor}

    def __init__(
        self,
        update_type: UpdateType,
        id: str,
        classification: Optional[str] = None,
        sensor_id: Optional[str] = None,
        confidence: Optional[float] = None,
        secondary_labels: Optional[Dict[str, Any]] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
    ):
        attributes = {}
        if secondary_labels:
            for k, v in secondary_labels.items():
                attributes[k] = v
        super().__init__(
            id,
            update_type,
            label_type="CLASSIFICATION_2D",
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            attributes=attributes,
            user_attrs=user_attrs,
        )


class _Classification3D(_BaseSingleCrop):
    _valid_sd_classes = {_BaseSensor}

    def __init__(
        self,
        update_type: UpdateType,
        id: str,
        classification: Optional[str] = None,
        sensor_id: Optional[str] = None,
        confidence: Optional[float] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
    ):
        super().__init__(
            id,
            update_type,
            label_type="CLASSIFICATION_3D",
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            attributes={},
            user_attrs=user_attrs,
        )


class _Cuboid3D(_BaseSingleCrop):
    """The base class for 3D Cuboids (labels and inferences) to attach to frames

    :meta private:
    """

    _valid_cf_classes = {_BaseCoordinateFrame3D}
    _add_to_sensor = False
    _add_to_coordinate_frame = True

    def __init__(
        self,
        update_type: UpdateType,
        id: str,
        classification: Optional[str] = None,
        coordinate_frame_id: Optional[str] = None,
        confidence: Optional[float] = None,
        position: Optional[List[float]] = None,
        dimensions: Optional[List[float]] = None,
        rotation: Optional[List[float]] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
        embedding: Optional[List[float]] = None,
    ):
        poses: Dict[str, Any] = {
            "pos_x": position[0] if position is not None else None,
            "pos_y": position[1] if position is not None else None,
            "pos_z": position[2] if position is not None else None,
            "dim_x": dimensions[0] if dimensions is not None else None,
            "dim_y": dimensions[1] if dimensions is not None else None,
            "dim_z": dimensions[2] if dimensions is not None else None,
            "rot_x": rotation[0] if rotation is not None else None,
            "rot_y": rotation[1] if rotation is not None else None,
            "rot_z": rotation[2] if rotation is not None else None,
            "rot_w": rotation[3] if rotation is not None else None,
        }

        for k, v in poses.items():
            if update_type == "MODIFY" and v is None:
                continue
            if not is_valid_float(v):
                raise Exception(k + " must be valid float")

        attributes = {k: v for k, v in poses.items() if v is not None}

        super().__init__(
            id,
            update_type,
            label_type="CUBOID_3D",
            classification=classification,
            coordinate_frame_id=coordinate_frame_id,
            confidence=confidence,
            iscrowd=iscrowd,
            attributes=attributes,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class _TextToken(_BaseSingleCrop):
    """The base class for text tokens (labels and inferences) to attach to frames

    :meta private:
    """

    _valid_sd_classes = {_BaseSensor}

    def __init__(
        self,
        update_type: UpdateType,
        id: str,
        classification: Optional[str] = None,
        sensor_id: Optional[str] = None,
        confidence: Optional[float] = None,
        index: Optional[int] = None,
        token: Optional[str] = None,
        visible: Optional[bool] = None,
        iscrowd: Optional[bool] = None,
        user_attrs: Optional[Dict[str, Any]] = {},
        embedding: Optional[List[float]] = None,
    ):
        attributes = {
            "index": index,
            "token": token,
            "visible": visible,
        }
        super().__init__(
            id,
            update_type,
            label_type="TEXT_TOKEN",
            classification=classification,
            sensor_id=sensor_id,
            confidence=confidence,
            iscrowd=iscrowd,
            attributes=attributes,
            user_attrs=user_attrs,
            embedding=embedding,
        )


class _BaseCropSet(_BaseEntity):
    """The base class for crop lists (labels and inferences) to attach to frames

    :meta private:
    """

    crops: List[_BaseSingleCrop]
    crop_assets: List[BaseLabelAssetDict]
    crop_embedding_dim: Optional[int]
    update_type: UpdateType
    _crop_ids_set: Set[str]
    _crop_class_name_set: Set[str]
    _crop_class_id_set: Set[int]
    _dataset_client: DatasetClient

    def __init__(
        self,
        frame_id: str,
        crop_type: CropType,
        update_type: UpdateType,
        dataset_client: DatasetClient,
    ):
        super().__init__(id=frame_id)

        self.crop_type = crop_type
        self.crops = []
        self.crop_assets = []
        self.update_type = update_type
        self._crop_ids_set = set()
        self._crop_class_name_set = set()
        self._crop_class_id_set = set()
        self.crop_embedding_dim = None
        self._dataset_client = dataset_client

    def __len__(self) -> int:
        return len(self.crops)

    def to_dict(self) -> Dict[str, Any]:
        crop_data = [crop.to_dict() for crop in self.crops]
        return {
            "task_id": self.id,
            "label_data": crop_data,
            "type": self.crop_type,
        }

    def _to_summary(self) -> LabelFrameSummary:
        crop_counts: Dict[LabelType, int] = {}
        for crop in self.crops:
            if not crop_counts.get(crop.label_type):
                crop_counts[crop.label_type] = 0
            crop_counts[crop.label_type] += 1

        return {
            "frame_id": self.id,
            "label_counts": crop_counts,
            "update_type": self.update_type,
        }

    def _add_crop(self, crop: _BaseCrop) -> None:
        if isinstance(crop, _BaseMultiCrop):
            crops = crop._crops
        else:
            crops = [crop]

        for crop in crops:
            if crop.id in self._crop_ids_set:
                raise Exception(
                    f"{crop.id} has already been added to frame {self.id} for this upload"
                )

            if crop.embedding:
                if not self.crop_embedding_dim:
                    self.crop_embedding_dim = crop.embedding_dim
                elif self.crop_embedding_dim != crop.embedding_dim:
                    raise Exception(
                        f"Length of embeddings must be the same, existing embeddings are of dimension {self.crop_embedding_dim} but new embedding has dimension {crop.embedding_dim}"
                    )
            elif (
                self.crop_embedding_dim
                and self.crop_embedding_dim > 0
                and not crop.reuse_latest_embedding
            ):
                raise Exception(
                    f"Length of embeddings must be the same, existing embeddings are of dimension {self.crop_embedding_dim} but new embedding has dimension {0 if crop.embedding_dim == -1 else crop.embedding_dim}"
                )

            if crop.classification and not isinstance(
                crop, (_Semseg2D, _InstanceSegMask2D)
            ):
                all_classifications = (
                    self._dataset_client._get_project_classes_by_classname()
                )
                if crop.classification not in all_classifications:
                    raise Exception(
                        f"Class {crop.classification} is not in the project classmap. "
                        f"Label Class Maps can be updated using append-only logic as specified here. "
                        f"https://aquarium.gitbook.io/aquarium-changelog/changelog-entries/2021-01-22#updating-label-class-maps"
                    )
                classification_id = all_classifications[crop.classification].class_id
                crop.classification_id = classification_id
                self._crop_class_name_set.add(crop.classification)
                self._crop_class_id_set.add(classification_id)

            self.crops.append(crop)
            self._crop_ids_set.add(crop.id)

    def _add_crop_embedding(
        self, crop: _BaseSingleCrop, embedding: List[float]
    ) -> None:
        crop._add_embedding(embedding)
        if not self.crop_embedding_dim:
            self.crop_embedding_dim = crop.embedding_dim
        elif self.crop_embedding_dim != crop.embedding_dim:
            raise Exception(
                f"Length of embeddings must be the same, existing embeddings are of dimension {self.crop_embedding_dim} but new embedding has dimension {crop.embedding_dim}"
            )

    def _all_label_class_ids(self) -> List[int]:
        return list(
            set(
                [
                    crop.classification_id
                    for crop in self.crops
                    if crop.classification_id is not None
                    and crop.classification
                    and crop.classification != "__mask"
                ]
            )
        )
