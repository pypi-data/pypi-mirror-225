import datetime
import numbers
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Sequence,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    TYPE_CHECKING,
)

from .coordinate_frames import (
    CoordinateFrame,
    _BaseCoordinateFrame,
    _WorldCoordinateFrame,
)
from .sensor_data import SensorData

from .dataset_client import DatasetClient

from .base_labels import (
    _BaseCrop,
    _BaseCropSet,
    _BaseMultiCrop,
    _BaseSingleCrop,
    FRIENDLY_SENSOR_NAMES,
)
from .labels import _LabeledSet, Label
from .modified_labels import _ModifiedLabelsSet, ModifiedLabel
from .inferences import _InferenceSet, Inference
from .sensor_data import FRIENDLY_CF_NAMES
from .util import (
    _BaseEntity,
    PrimaryTaskTypes,
    UpdateType,
    TYPE_PRIMITIVE_TO_STRING_MAP,
    USER_METADATA_PRIMITIVE_TYPES,
    USER_METADATA_MODE_TYPES,
    USER_METADATA_SEQUENCE,
    assert_and_get_valid_iso_date,
    assert_valid_name,
    is_valid_float,
)

if TYPE_CHECKING:
    from .client import Client
    from .datasets import (
        _Dataset,
        LabeledDataset,
        InferenceSet,
        UnlabeledDataset,
        UnlabeledDatasetV2,
    )

MetadataValue = Union[str, int, float, bool, USER_METADATA_SEQUENCE]

T = TypeVar("T")
C = TypeVar("C")


def _find_first_instance(entity_list: Sequence[T], cls: Type[C]) -> Optional[C]:
    for entity in entity_list:
        if isinstance(entity, cls):
            return entity
    return None


CustomMetricsEntry = Union[float, List[List[Union[float, int]]]]


class UserMetadataEntry:
    """Create a metadata entry to add to a frame

    Args:
        key: the key of the entry
        val: the value
        val_type (Optional[Literal['str', 'int', 'float', 'bool']]): (optional) a string representation of the type of the value or, if the value is a list, the first entry in the list
    """

    key: str
    val: MetadataValue
    val_type: USER_METADATA_PRIMITIVE_TYPES
    mode: USER_METADATA_MODE_TYPES

    def __init__(
        self,
        key: str,
        val: MetadataValue,
        val_type: Optional[USER_METADATA_PRIMITIVE_TYPES] = None,
    ):
        assert_valid_name(key)

        is_list = False
        if isinstance(val, (list, tuple)):
            is_list = True
            inferred_val_type = self._validate_list(key, val, val_type)
        elif isinstance(val, (str, int, float, bool)):
            inferred_val_type = self._validate_scalar(key, val, val_type)
        else:
            raise Exception(f"Metadata of type {type(val)} are not supported")

        self.key = key
        self.val = val
        self.val_type = inferred_val_type
        self.mode = "list" if is_list else "scalar"

    def _validate_list(
        self,
        key: str,
        val: MetadataValue,
        list_elt_type: Optional[USER_METADATA_PRIMITIVE_TYPES] = None,
    ) -> USER_METADATA_PRIMITIVE_TYPES:
        if val is not None and not isinstance(val, (list, tuple)):
            # we've already validated this -- this just appeases mypy
            return "str"

        if val is None and list_elt_type is None:
            raise Exception(
                f"User Metadata list key {key} must provide "
                f"list or expected type of list elements if None"
            )

        # Validates that val has an accepted type
        if val is not None:
            if type(val) not in (list, tuple):
                raise Exception(
                    f"User Metadata list value {val} "
                    f"is not in accepted sequence types list, tuple."
                )
            if len(val) == 0 and not list_elt_type:
                raise Exception(
                    f"User Metadata list value {val} "
                    f"is an empty {type(val).__name__}. "
                    "Please specify the expected scalar value type for its elements by passing a list_elt_type"
                )

            # validate that all elements in the list are the same primitive type, based on the first element
            if len(val) > 0:
                found_val_types = {type(el) for el in val}

                if len(found_val_types) > 1:
                    raise Exception(
                        f"User Metadata list value {val} "
                        f"has elements of invalid type. Expected all elements to be of the same type, found types of {found_val_types}"
                    )

                inferred_val_type = found_val_types.pop()
                if inferred_val_type not in TYPE_PRIMITIVE_TO_STRING_MAP:
                    raise Exception(
                        f"User Metadata list value {val} contains elements "
                        f"not in accepted scalar value types {TYPE_PRIMITIVE_TO_STRING_MAP.values()}"
                    )

        # Validates that list_elt_type has an accepted type
        if list_elt_type and list_elt_type not in TYPE_PRIMITIVE_TO_STRING_MAP.values():
            raise Exception(
                f"User Metadata list element type {list_elt_type} "
                f"not in accepted scalar value types {TYPE_PRIMITIVE_TO_STRING_MAP.values()}"
            )

        # Checks that inferred type matches what the user put in list_elt_type
        if list_elt_type is not None and val is not None and len(val) > 0:
            inferred_val_type = type(val[0])
            for (
                primitive,
                type_string,
            ) in TYPE_PRIMITIVE_TO_STRING_MAP.items():
                if inferred_val_type is primitive and list_elt_type != type_string:
                    raise Exception(
                        f"For User Metadata key {key}, value {val}, "
                        f"element type is inferred as {type_string} but provided type was {list_elt_type}"
                    )

        # Sets list_elt_type if it is not set
        if list_elt_type is None:
            inferred_val_type = type(val[0])
            list_elt_type = TYPE_PRIMITIVE_TO_STRING_MAP[inferred_val_type]

        # If element type is float, ensure that all elements are valid floats
        if val is not None and list_elt_type == "float":
            for val_elt in val:
                if not is_valid_float(val_elt):
                    raise Exception(
                        f"For User Metadata key {key}, value {val}, "
                        f"element type is inferred as float but is not a valid float"
                    )
        return list_elt_type

    def _validate_scalar(
        self,
        key: str,
        val: MetadataValue,
        val_type: Optional[USER_METADATA_PRIMITIVE_TYPES] = None,
    ) -> USER_METADATA_PRIMITIVE_TYPES:
        if val is not None and not isinstance(val, (str, int, float, bool)):
            # we've already validated this -- this just appeases mypy
            return "str"

        if val is None and val_type is None:
            raise Exception(
                f"User Metadata key {key} must provide "
                f"scalar value or expected type of scalar value if None"
            )
        # Validates that val has an accepted type
        if val is not None and type(val) not in TYPE_PRIMITIVE_TO_STRING_MAP:
            raise Exception(
                f"User Metadata Value {val} "
                f"not in accepted scalar value types {TYPE_PRIMITIVE_TO_STRING_MAP.values()}"
            )
        # Validates that val_type has an accepted type
        if val_type and val_type not in TYPE_PRIMITIVE_TO_STRING_MAP.values():
            raise Exception(
                f"User Metadata Value Type {val_type} "
                f"not in accepted scalar value types {TYPE_PRIMITIVE_TO_STRING_MAP.values()}"
            )

        # Sets val_type if it is not set
        if val_type is None:
            val_type = TYPE_PRIMITIVE_TO_STRING_MAP[type(val)]

        # If type is float, ensure that it is a valid float
        if val is not None and val_type == "float" and not is_valid_float(val):
            raise Exception(
                f"For User Metadata key {key}, value {val}, "
                f"type is inferred as float but is not a valid float"
            )

        # Checks that inferred type matches what the user put in val_type
        if val is not None:
            for (
                primitive,
                type_string,
            ) in TYPE_PRIMITIVE_TO_STRING_MAP.items():
                if type(val) is primitive and val_type != type_string:
                    raise Exception(
                        f"For User Metadata key {key}, value {val}, "
                        f"type is inferred as {type_string} but provided type was {val_type}"
                    )
        return val_type

    def to_tuple(
        self,
    ) -> Tuple[
        str,
        Union[str, int, float, bool, USER_METADATA_SEQUENCE],
        USER_METADATA_PRIMITIVE_TYPES,
        USER_METADATA_MODE_TYPES,
    ]:
        return (self.key, self.val, self.val_type, self.mode)


class GeoData:
    """Create a user provided EPSG:4326 WGS84 lat long pair

    We expect these values to be floats

    Args:
        lat (float): lattitude of Geo Location
        lon (float): longitude of Geo Location
    """

    def __init__(self, lat: float, lon: float):
        if not (isinstance(lat, float) and isinstance(lon, float)):
            raise Exception(
                f"Lattitude ({lat}) and Longitude ({lon}) must both be floats."
            )

        self.lat = lat
        self.lon = lon

    def to_dict(self) -> Dict[str, float]:
        return {"geo_EPSG4326_lat": self.lat, "geo_EPSG4326_lon": self.lon}


class _BaseFrame(_BaseEntity):
    """The base class for all frames

    :meta private:
    """

    embedding: Optional[List[float]] = None
    geo_data: Optional[GeoData] = None
    _previously_written_window: Optional[str] = None
    _sensor_data_by_id: Dict[str, SensorData]
    _crop_set: _BaseCropSet
    _explicitly_set_keys: Set[str]
    _dataset_client: DatasetClient
    _is_derivative_frame: bool  # True for inference frame and for modified frame objects, false otherwise

    def __init__(
        self,
        frame_id: str,
        dataset_client: DatasetClient,
        update_type: UpdateType,
        device_id: Optional[str] = None,
        date_captured: Optional[str] = None,
        coordinate_frames: List[CoordinateFrame] = [],
        sensor_data: List[SensorData] = [],
        crops: Union[
            Sequence[Label], Sequence[Union[Label, ModifiedLabel]], Sequence[Inference]
        ] = [],
        geo_data: Optional[GeoData] = None,
        user_metadata: Optional[List[UserMetadataEntry]] = [],
        embedding: Optional[List[float]] = None,
    ):
        super().__init__(frame_id)

        self._explicitly_set_keys = {"reuse_latest_embedding"}
        self.update_type = update_type
        self.embedding_dim = -1
        self._dataset_client = dataset_client

        if date_captured is not None:
            self.date_captured = assert_and_get_valid_iso_date(date_captured)
            self._explicitly_set_keys.add("date_captured")
        else:
            self.date_captured = str(datetime.datetime.now())

        if device_id is not None:
            self.device_id = device_id
            self._explicitly_set_keys.add("device_id")
        else:
            self.device_id = "default_device"

        if embedding:
            self._add_embedding(embedding)
            self.reuse_latest_embedding = False
        else:
            self.reuse_latest_embedding = update_type == "MODIFY"

        generated_cfs: List[_BaseCoordinateFrame] = []
        if sensor_data:
            new_cfs = self._validate_sensors_and_generate_cfs(
                sensor_data, coordinate_frames
            )
            generated_cfs += new_cfs
            self.sensor_data = sensor_data
            self._sensor_data_by_id = {sd.id: sd for sd in sensor_data}
            self._explicitly_set_keys.add("sensor_data")
        elif self.update_type == "ADD" and not self._is_derivative_frame:
            raise Exception("Cannot create a frame without sensor data")
        else:
            self.sensor_data = []
            self._sensor_data_by_id = {}

        if coordinate_frames or generated_cfs:
            all_coordinate_frames = self._validate_and_parent_cfs(
                coordinate_frames, generated_cfs
            )
            self.coordinate_frames = all_coordinate_frames
            self._explicitly_set_keys.add("coordinate_frames")
        elif update_type == "ADD":
            self.coordinate_frames = [_WorldCoordinateFrame()]
        else:
            self.coordinate_frames = []

        if geo_data:
            self.geo_data = geo_data
            self._explicitly_set_keys.add("geo_data")

        if user_metadata:
            self.user_metadata = user_metadata
        else:
            self.user_metadata = []

        if crops:
            for crop in crops:
                self._validate_crop(crop)
                self._crop_set._add_crop(crop)
            self._validate_crop_set()

    def _validate_sensors_and_generate_cfs(
        self,
        sensor_data: List[SensorData],
        coordinate_frames: Optional[List[CoordinateFrame]],
    ) -> List[_BaseCoordinateFrame]:
        seen_sensor_ids: Set[str] = set()
        new_coordinate_frames: List[_BaseCoordinateFrame] = []
        if coordinate_frames is None:
            coordinate_frames = []

        for sensor_datum in sensor_data:
            if sensor_datum.id in seen_sensor_ids:
                raise Exception(
                    f"Encountered multiple sensor_data with the same id {sensor_datum.id}"
                )
            seen_sensor_ids.add(sensor_datum.id)
            if not sensor_datum.coordinate_frame:
                # check if there are explicitly passed coordinate frames that this could feasibly belong to
                # in the case of someone just wanting to pass coordinates and sensors without having to predefine them
                existing = _find_first_instance(
                    coordinate_frames, sensor_datum._default_cf_class
                )
                if existing:
                    sensor_datum._set_coordinate_frame(existing)
                else:
                    # otherwise, assume that this is a separate sensor from other sensors that is looking at a different part of the world
                    new_cf = sensor_datum._default_cf_class(sensor_datum.id)
                    sensor_datum._set_coordinate_frame(new_cf)
                    new_coordinate_frames.append(new_cf)
        return new_coordinate_frames

    def _validate_and_parent_cf(
        self,
        coordinate_frame: _BaseCoordinateFrame,
        existing: Sequence[CoordinateFrame],
        generated: List[_BaseCoordinateFrame],
        seen_coordinate_frames: Set[str],
    ) -> Optional[_WorldCoordinateFrame]:
        if coordinate_frame.id in seen_coordinate_frames:
            raise Exception(
                f"Encountered multiple collection frames with the same id {coordinate_frame.id}"
            )
        if not coordinate_frame.parent_coordinate_frame and not isinstance(
            coordinate_frame, _WorldCoordinateFrame
        ):
            # find a parent instance or create it
            found_existing = _find_first_instance(existing, _WorldCoordinateFrame)
            found_generated = _find_first_instance(generated, _WorldCoordinateFrame)
            if found_existing:
                coordinate_frame._set_parent(found_existing)
            elif found_generated:
                coordinate_frame._set_parent(found_generated)
            else:
                new = _WorldCoordinateFrame()
                coordinate_frame._set_parent(new)
                return new
        return None

    def _validate_and_parent_cfs(
        self,
        coordinate_frames: Optional[List[CoordinateFrame]],
        generated_coordinate_frames: List[_BaseCoordinateFrame],
    ) -> List[_BaseCoordinateFrame]:
        if coordinate_frames is None:
            coordinate_frames = []

        seen_coordinate_frame_ids: Set[str] = set()
        for cf in coordinate_frames[:]:
            new_parent = self._validate_and_parent_cf(
                cf,
                coordinate_frames,
                generated_coordinate_frames,
                seen_coordinate_frame_ids,
            )
            seen_coordinate_frame_ids.add(cf.id)
            if new_parent:
                generated_coordinate_frames.append(new_parent)

        for gcf in generated_coordinate_frames:
            new_parent = self._validate_and_parent_cf(
                gcf,
                coordinate_frames,
                generated_coordinate_frames,
                seen_coordinate_frame_ids,
            )
            seen_coordinate_frame_ids.add(gcf.id)
            if new_parent:
                generated_coordinate_frames.append(new_parent)

        return [
            cast(_BaseCoordinateFrame, cf) for cf in coordinate_frames
        ] + generated_coordinate_frames

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
            self._explicitly_set_keys.update(["embedding"])
        else:
            raise Exception("An embedding has already been added to this frame")

    def _validate_crop(self, crop: _BaseCrop) -> None:
        if isinstance(crop, _BaseMultiCrop):
            crops = crop._crops
        else:
            crops = [crop]

        for single_crop in crops:
            class_name = single_crop.__class__.__name__
            # TODO: if self._is_derivative_frame, get candidate sensor ids & coordinate frame ids from the server somehow
            if single_crop._add_to_sensor and not self._is_derivative_frame:
                sensor_ids = [s.id for s in self.sensor_data]
                if not single_crop.sensor_id:
                    if len(sensor_ids) == 1:
                        single_crop.sensor_id = sensor_ids[0]
                    else:
                        raise Exception(
                            f"Cannot infer the correct sensor_id for {single_crop.id}; please reinitialize this {class_name} with sensor_id set to one of {sensor_ids}"
                        )
                # make sure the sensor id exists
                if single_crop.sensor_id not in self._sensor_data_by_id:
                    raise Exception(
                        f"{single_crop.id}'s sensor_id {single_crop.sensor_id} not found on frame. Make sure that the sensor_id is one of {sensor_ids}."
                    )
                sensor_data = self._sensor_data_by_id[single_crop.sensor_id]
                # check that sensor data is inheriting from the right class
                if single_crop._valid_sd_classes is None:
                    raise Exception(
                        f"{class_name} cannot be associated with any sensor data."
                    )
                elif not any(
                    [
                        isinstance(sensor_data, sd_cls)
                        for sd_cls in single_crop._valid_sd_classes
                    ]
                ):
                    raise Exception(
                        f"{class_name} can only be associated with a sensor data of a class in {[FRIENDLY_SENSOR_NAMES[sd_cls] for sd_cls in single_crop._valid_sd_classes]}"
                    )
            if single_crop._add_to_coordinate_frame and not self._is_derivative_frame:
                cfs_by_id = {cf.id: cf for cf in self.coordinate_frames}
                if not single_crop.coordinate_frame_id:
                    single_crop.coordinate_frame_id = "world"
                # make sure coordinate frame exists
                if single_crop.coordinate_frame_id not in cfs_by_id:
                    raise Exception(
                        f"{single_crop.id}'s coordinate_frame_id {single_crop.coordinate_frame_id} not found on frame. Make sure that the coordinate_frame_id is one of {list(cfs_by_id.keys())}."
                    )
                coordinate_frame = cfs_by_id[single_crop.coordinate_frame_id]
                # check that coordinate frame is inheriting from the right class
                if single_crop._valid_cf_classes is None:
                    raise Exception(
                        f"{class_name} cannot be associated with any coordinate frame."
                    )
                elif not any(
                    [
                        isinstance(coordinate_frame, cf_cls)
                        for cf_cls in single_crop._valid_cf_classes
                    ]
                ):
                    raise Exception(
                        f"{class_name} can only be associated with a coordinate frame of a class in {[FRIENDLY_CF_NAMES[sd_cls] for sd_cls in single_crop._valid_cf_classes]}"
                    )

    def _validate_crop_set(self) -> None:
        primary_task = self._dataset_client._get_primary_task()
        if primary_task == PrimaryTaskTypes.SemSeg:
            mask_types = ["SEMANTIC_LABEL_URL_2D"]
            mask_crops = len(
                [c for c in self._crop_set.crops if c.label_type in mask_types]
            )

            all_valid_types = mask_types
            extra_label_types = set(
                [
                    c.label_type
                    for c in self._crop_set.crops
                    if c.label_type not in all_valid_types
                ]
            )
            if mask_crops != 1 and self.update_type == "ADD":
                extra_label_text = (
                    "has no labels"
                    if not self.crop_count()
                    else f"has label types of {list(extra_label_types)}"
                )
                raise Exception(
                    f"Frame {self.id} {extra_label_text}. Dataset frames for {PrimaryTaskTypes.SemSeg.value} projects must have exactly one SemSeg2D label or inference"
                )
        elif primary_task == PrimaryTaskTypes.InstanceSegmentation:
            mask_types = ["INSTANCE_LABEL_URL_2D"]
            mask_crops = len(
                [c for c in self._crop_set.crops if c.label_type in mask_types]
            )

            all_valid_types = mask_types + ["INSTANCE_LABEL_2D"]
            extra_label_types = set(
                [
                    c.label_type
                    for c in self._crop_set.crops
                    if c.label_type not in all_valid_types
                ]
            )
            if mask_crops != 1 and self.update_type == "ADD":
                extra_label_text = (
                    "has no labels"
                    if not self.crop_count()
                    else f"has label types of {list(extra_label_types)}"
                )
                raise Exception(
                    f"Frame {self.id} {extra_label_text}. Dataset frames for {PrimaryTaskTypes.InstanceSegmentation.value} projects must have exactly one InstanceSeg2D label or inference"
                )
        elif primary_task._is_classification():
            if self.crop_count() > 1:
                raise Exception(
                    f"Frame {self.id} has more than one label. Dataset frames for {primary_task.value} projects must have at most one label or inference."
                )

    def crop_count(self) -> int:
        return len(self._crop_set.crops)

    def to_dict(self) -> Dict[str, Any]:
        row = {
            "task_id": self.id,
            "date_captured": self.date_captured,
            "device_id": self.device_id,
            "coordinate_frames": [cf.to_dict() for cf in self.coordinate_frames],
            "sensor_data": [sd.to_dict() for sd in self.sensor_data],
            "geo_data": self.geo_data.to_dict() if self.geo_data else {},
            "reuse_latest_embedding": self.reuse_latest_embedding,
            "change": self.update_type,
        }
        user_metadata_types = {}
        user_metadata_modes = {}

        for um in self.user_metadata:
            k, v, vt, vm = um.to_tuple()
            namespaced = k
            if "user__" not in namespaced:
                namespaced = "user__" + namespaced
            # cast to BQ-serializable list if tuple
            row[namespaced] = list(v) if isinstance(v, tuple) else v
            user_metadata_types[namespaced] = vt
            user_metadata_modes[namespaced] = vm
            self._explicitly_set_keys.add(namespaced)

        row["user_metadata_types"] = user_metadata_types
        row["user_metadata_modes"] = user_metadata_modes
        self._explicitly_set_keys.add("user_metadata_types")
        self._explicitly_set_keys.add("user_metadata_modes")

        if self.update_type == "MODIFY":
            row["explicitly_set_keys"] = list(self._explicitly_set_keys)
            row["previously_written_window"] = self._previously_written_window
        return row


class LabeledFrame(_BaseFrame):
    """A labeled frame for a labeled dataset.

    Args:
        dataset: A LabeledDataset object that this frame belongs to.
        frame_id: A unique id for this frame.
        sensor_data: The list of sensor data to add to the frame.
        labels: The list of Labels to add to the frame.
        coordinate_frames: (optional) The list of coordinate frames to add to the frame.
        device_id: (optional) The device that generated this frame. Defaults to None.
        date_captured: (optional) ISO formatted datetime string. Defaults to None.
        geo_data: (optional) A lat lon pair to assign to the pair
        user_metadata: (optional) A list of user-provided metadata
        embedding: (optional) A vector of floats of at least length 2.
    """

    _is_derivative_frame = False
    _crop_set: _LabeledSet

    def __init__(
        self,
        *,
        dataset: "LabeledDataset",
        frame_id: str,
        sensor_data: List[SensorData],
        labels: List[Label],
        coordinate_frames: List[CoordinateFrame] = [],
        device_id: Optional[str] = None,
        date_captured: Optional[str] = None,
        geo_data: Optional[GeoData] = None,
        user_metadata: Optional[List[UserMetadataEntry]] = [],
        embedding: Optional[List[float]] = None,
    ):
        self._crop_set = _LabeledSet(frame_id, dataset_client=dataset._dataset_client)
        super().__init__(
            frame_id,
            dataset._dataset_client,
            "ADD",
            device_id,
            date_captured,
            coordinate_frames,
            sensor_data,
            labels,
            geo_data,
            user_metadata,
            embedding,
        )
        dataset._add_frame(self)


class ModifiedLabeledFrame(_BaseFrame):
    """Create a modification of an existing LabeledFrame. If the frame_id does not already exist in the dataset, its update will be dropped during processing.
    Modifications are additive; new labels will be appended and existing labels will be updated with not-None values

    Args:
        dataset: A LabeledDataset object that this frame belongs to.
        frame_id: A unique id for this frame.
        sensor_data: The list of sensor data to add to the frame.
        labels: The list of Labels and ModifiedLabels to add to the frame.
        coordinate_frames: (optional) The list of coordinate frames to add to the frame.
        device_id: (optional) The device that generated this frame. Defaults to None.
        date_captured: (optional) ISO formatted datetime string. Defaults to None.
        geo_data: (optional) A lat lon pair to assign to the pair
        user_metadata: (optional) A list of user-provided metadata
        embedding: (optional) A vector of floats of at least length 2.
    """

    _is_derivative_frame = True
    _crop_set: _ModifiedLabelsSet

    def __init__(
        self,
        *,
        dataset: "LabeledDataset",
        frame_id: str,
        sensor_data: List[SensorData] = [],
        labels: List[Union[Label, ModifiedLabel]] = [],
        coordinate_frames: List[CoordinateFrame] = [],
        device_id: Optional[str] = None,
        date_captured: Optional[str] = None,
        geo_data: Optional[GeoData] = None,
        user_metadata: Optional[List[UserMetadataEntry]] = [],
        embedding: Optional[List[float]] = None,
    ):
        self._crop_set = _ModifiedLabelsSet(
            frame_id, dataset_client=dataset._dataset_client
        )
        super().__init__(
            frame_id,
            dataset._dataset_client,
            "MODIFY",
            device_id,
            date_captured,
            coordinate_frames,
            sensor_data,
            labels,
            geo_data,
            user_metadata,
            embedding,
        )
        dataset._add_frame(self)


class InferenceFrame(_BaseFrame):
    """Create a frame for inferences to add to an InferenceSet.

    Args:
        inference_set: An InferenceSet object that this frame belongs to.
        frame_id: A unique id for this frame.
        user_metadata: (optional) A list of user-provided metadata
        custom_metrics: (optional) A dictionary of custom metrics to add to the frame
        embedding: (optional) A vector of floats of at least length 2.
    """

    _is_derivative_frame = True
    _crop_set: _InferenceSet
    _inf_user_metadata: Dict[str, Any]
    custom_metrics: Dict[str, CustomMetricsEntry]

    def __init__(
        self,
        *,
        inference_set: "InferenceSet",
        frame_id: str,
        inferences: List[Inference],
        user_metadata: Optional[List[UserMetadataEntry]] = None,
        custom_metrics: Optional[Dict[str, CustomMetricsEntry]] = None,
        embedding: Optional[List[float]] = None,
    ):
        self._crop_set = _InferenceSet(
            frame_id=frame_id, dataset_client=inference_set._dataset_client
        )
        super().__init__(
            frame_id,
            inference_set._dataset_client,
            "ADD",
            crops=inferences,
            embedding=embedding,
        )
        if custom_metrics:
            self.custom_metrics = custom_metrics
            self._explicitly_set_keys.add("custom_metrics")
        else:
            self.custom_metrics = {}

        if user_metadata:
            formatted_um = {}
            for um in user_metadata:
                formatted_um[um.key] = um.val
            self._inf_user_metadata = formatted_um
        else:
            self._inf_user_metadata = {}

        inference_set._add_frame(self)

    def to_dict(self) -> Dict[str, Any]:
        row = super().to_dict()
        if self.custom_metrics:
            row["custom_metrics"] = self.custom_metrics

        row["inference_metadata"] = {}
        row["inference_data"] = [inf.to_dict() for inf in self._crop_set.crops]

        row["inference_metadata"]["user_metadata"] = self._inf_user_metadata
        return row


class UnlabeledFrame(_BaseFrame):
    """A frame for a dataset which is labeled with inferences rather than GT labels.
    Meant to be used with UnlabeledDataset.

    Args:
        dataset: An UnlabeledDataset object that this frame belongs to
        frame_id: A unique id for this frame.
        sensor_data: The list of sensor data to add to the frame.
        proposals: The list of proposed labels with confidence (aka inferences) to add to the frame.
        coordinate_frames: (optional) The list of coordinate frames to add to the frame.
        device_id: (optional) The device that generated this frame. Defaults to None.
        date_captured: (optional) ISO formatted datetime string. Defaults to None.
        geo_data: (optional) A lat lon pair to assign to the pair
        user_metadata: (optional) A list of user-provided metadata
        embedding: (optional) A vector of floats of at least length 2.
    """

    _is_derivative_frame = False
    _crop_set: _InferenceSet

    def __init__(
        self,
        *,
        dataset: "UnlabeledDataset",
        frame_id: str,
        sensor_data: List[SensorData],
        proposals: List[Inference],
        coordinate_frames: List[CoordinateFrame] = [],
        device_id: Optional[str] = None,
        date_captured: Optional[str] = None,
        geo_data: Optional[GeoData] = None,
        user_metadata: Optional[List[UserMetadataEntry]] = [],
        embedding: Optional[List[float]] = None,
    ):
        self._crop_set = _InferenceSet(
            frame_id=frame_id, dataset_client=dataset._dataset_client
        )
        super().__init__(
            frame_id,
            dataset._dataset_client,
            "ADD",
            device_id,
            date_captured,
            coordinate_frames,
            sensor_data,
            proposals,
            geo_data,
            user_metadata,
            embedding,
        )
        dataset._add_frame(self)


class UnlabeledFrameV2(_BaseFrame):
    """A frame for a dataset which is labeled with inferences rather than GT labels.
    Meant to be used with UnlabeledDatasetV2.

    Args:
        dataset: An UnlabeledDatasetV2 object that this frame belongs to
        frame_id: A unique id for this frame.
        sensor_data: The list of sensor data to add to the frame.
        proposals: The list of proposed labels with confidence (aka inferences) to add to the frame.
        coordinate_frames: (optional) The list of coordinate frames to add to the frame.
        device_id: (optional) The device that generated this frame. Defaults to None.
        date_captured: (optional) ISO formatted datetime string. Defaults to None.
        geo_data: (optional) A lat lon pair to assign to the pair
        user_metadata: (optional) A list of user-provided metadata
    """

    _is_derivative_frame = False
    _crop_set: _InferenceSet

    def __init__(
        self,
        *,
        dataset: "UnlabeledDatasetV2",
        frame_id: str,
        sensor_data: List[SensorData],
        proposals: List[Inference],
        coordinate_frames: List[CoordinateFrame] = [],
        device_id: Optional[str] = None,
        date_captured: Optional[str] = None,
        geo_data: Optional[GeoData] = None,
        user_metadata: Optional[List[UserMetadataEntry]] = [],
    ):
        self._crop_set = _InferenceSet(
            frame_id=frame_id, dataset_client=dataset._dataset_client
        )
        for inf in proposals:
            if isinstance(inf, _BaseSingleCrop) and inf.embedding:
                raise Exception(
                    "Custom embeddings are not supported for this iteration of UnlabeledFrame"
                )
            elif isinstance(inf, _BaseMultiCrop):
                if any([c.embedding is not None for c in inf._crops]):
                    raise Exception(
                        "Custom embeddings are not supported for this iteration of UnlabeledFrame"
                    )
        super().__init__(
            frame_id,
            dataset._dataset_client,
            "ADD",
            device_id,
            date_captured,
            coordinate_frames,
            sensor_data,
            proposals,
            geo_data,
            user_metadata,
        )
        dataset._add_frame(self)


class DeletedFrame(_BaseFrame):
    """For internal use: create a deleted frame entry

    :meta private:
    """

    def __init__(
        self,
        *,
        frame_id: str,
        dataset: "_Dataset",
    ):
        super().__init__(
            frame_id,
            dataset._dataset_client,
            "DELETE",
        )
        dataset._add_frame(self)


Frame = Union[
    DeletedFrame,
    LabeledFrame,
    InferenceFrame,
    ModifiedLabeledFrame,
    UnlabeledFrame,
    UnlabeledFrameV2,
]

FrameType = Union[
    Type[LabeledFrame],
    Type[InferenceFrame],
    Type[ModifiedLabeledFrame],
    Type[UnlabeledFrame],
    Type[UnlabeledFrameV2],
    Type[DeletedFrame],
]
