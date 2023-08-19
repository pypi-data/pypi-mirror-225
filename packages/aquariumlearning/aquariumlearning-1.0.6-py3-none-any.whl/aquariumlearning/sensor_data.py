import datetime
from typing import Any, Dict, Optional, Set, Type, TypeVar, Union
from .coordinate_frames import (
    CoordinateFrame,
    CoordinateFrame2D,
    CoordinateFrame3D,
    _BaseCoordinateFrame,
    _BaseCoordinateFrame2D,
    _BaseCoordinateFrame3D,
    _AudioCoordinateFrame,
    _ImageCoordinateFrame,
    _TextCoordinateFrame,
    _VideoCoordinateFrame,
    _WorldCoordinateFrame,
)
from .util import (
    DEFAULT_SENSOR_ID,
    ResizeMode,
    _BaseEntity,
    assert_and_get_valid_iso_date,
)

_SensorCoordinateFrame = Union[
    Type[_BaseCoordinateFrame2D],
    Type[_BaseCoordinateFrame3D],
    Type[_BaseCoordinateFrame],
]

FRIENDLY_CF_NAMES: Dict[_SensorCoordinateFrame, str] = {
    _BaseCoordinateFrame2D: CoordinateFrame2D.__name__,
    _BaseCoordinateFrame3D: CoordinateFrame3D.__name__,
    _BaseCoordinateFrame: ", ".join(
        [CoordinateFrame2D.__name__, CoordinateFrame3D.__name__]
    ),
}

_DefaultCoordinateFrame = Union[
    _AudioCoordinateFrame,
    _ImageCoordinateFrame,
    _TextCoordinateFrame,
    _VideoCoordinateFrame,
    _WorldCoordinateFrame,
]


class _BaseSensor(_BaseEntity):
    """The base class for all sensors. includes generalized validation of coordinate frames

    :meta private:
    """

    # at instantiation time, make sure that this sensor is attached to a supported coordinate_frame type
    _valid_cf_classes: Optional[Set[_SensorCoordinateFrame]] = None
    # at instantiation time, make sure that this sensor is attached to a supported coordinate_frame type
    _valid_cf_types: Optional[Set[str]] = None
    # at frame validation time, if this sensor does not have a coordinate_frame, find or create one of this type for it
    _default_cf_class: Type[_DefaultCoordinateFrame] = _WorldCoordinateFrame

    def __init__(
        self,
        id: str,
        type: str,
        data_urls: Dict[str, str],
        mirror_asset: bool,
        metadata: Optional[Dict[str, Any]] = None,
        coordinate_frame: Optional[_BaseCoordinateFrame] = None,
        date_captured: Optional[str] = None,
    ):
        super(_BaseSensor, self).__init__(id)

        if coordinate_frame:
            self._validate_coordinate_frame(coordinate_frame)

        self.type = type
        self.data_urls = data_urls
        self.mirror_asset = mirror_asset
        self.coordinate_frame = coordinate_frame

        populated_date_captured = (
            str(datetime.datetime.now()) if date_captured is None else date_captured
        )
        self.date_captured = assert_and_get_valid_iso_date(populated_date_captured)
        self.metadata = metadata

    def _set_coordinate_frame(self, coordinate_frame: _BaseCoordinateFrame) -> None:
        self._validate_coordinate_frame(coordinate_frame)
        self.coordinate_frame = coordinate_frame

    def _validate_coordinate_frame(
        self, coordinate_frame: _BaseCoordinateFrame
    ) -> None:
        class_name = type(self).__name__
        # check that it's inheriting from the right class
        if not self._valid_cf_classes:
            raise Exception(f"{class_name} cannot be added to any coordinate frame")
        if not any(
            [isinstance(coordinate_frame, cf_cls) for cf_cls in self._valid_cf_classes]
        ):
            raise Exception(
                f"{class_name} can only be added to a coordinate frame of a class in {[FRIENDLY_CF_NAMES[cf_cls] for cf_cls in self._valid_cf_classes]}"
            )

        if self._valid_cf_types and not any(
            [coordinate_frame.type == cf_type for cf_type in self._valid_cf_types]
        ):
            raise Exception(
                f"{class_name} can only be added to a coordinate frame of a type in {self._valid_cf_types}"
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "coordinate_frame": self.coordinate_frame.id
            if self.coordinate_frame is not None
            else None,
            "data_urls": self.data_urls,
            "date_captured": self.date_captured,
            "sensor_id": self.id,
            "sensor_metadata": self.metadata,
            "sensor_type": self.type,
            "mirror_asset": self.mirror_asset,
        }


class _BaseSensor2D(_BaseSensor):
    """The base class for all strictly 2D sensors

    :meta private:
    """

    _valid_cf_classes = {_BaseCoordinateFrame2D}


class _BaseSensor3D(_BaseSensor):
    """The base class for all strictly 3D sensors

    :meta private:
    """

    _valid_cf_classes = {_BaseCoordinateFrame3D}
    _default_cf_class = _WorldCoordinateFrame


class Image(_BaseSensor2D):
    """Create an image to add to a frame.

    Args:
        image_url: URL to where the object is located.
        id: id of sensor that generates this datapoint (defaults to "DEFAULT").
        preview_url: A URL to a compressed version of the image. It must be the same pixel dimensions as the original image. Defaults to None.
        width: The width of the image in pixels. Defaults to None.
        height: The height of the image in pixels. Defaults to None.
        coordinate_frame: The coordinate frame. Defaults to None.
        date_captured: ISO formatted date. Defaults to None.
        mirror_asset: request this asset to be saved to Aquarium Storage. Useful for Short duration signed URL assets.
    """

    _valid_cf_types = {"IMAGE", "IMAGE_PROJECTION"}
    _default_cf_class = _ImageCoordinateFrame

    def __init__(
        self,
        *,
        image_url: str,
        id: str = DEFAULT_SENSOR_ID,
        preview_url: Optional[str] = None,
        width: Optional[int] = None,
        height: Optional[int] = None,
        coordinate_frame: Optional[CoordinateFrame2D] = None,
        date_captured: Optional[str] = None,
        mirror_asset: bool = False,
    ):
        sensor_metadata = {}
        if width is not None:
            if not isinstance(width, int):
                raise Exception("width must be an int")
            sensor_metadata["width"] = width

        if height is not None:
            if not isinstance(height, int):
                raise Exception("height must be an int")
            sensor_metadata["height"] = height

        data_urls = {"image_url": image_url}

        if preview_url is not None:
            data_urls["preview_url"] = preview_url

        super(Image, self).__init__(
            id,
            "IMAGE_V0",
            data_urls,
            mirror_asset,
            metadata=sensor_metadata,
            coordinate_frame=coordinate_frame,
            date_captured=date_captured,
        )


class ImageOverlay(_BaseSensor2D):
    """Create an image overlay to add to a frame.

    Args:
        overlay_id: The id of this overlay.
        image_url: URL to where the object is located.
        id: id of sensor that generates this datapoint (defaults to "DEFAULT").
        preview_url: A URL to a compressed version of the image. It must be the same pixel dimensions as the original image. Defaults to None.
        width: The width of the image in pixels. Defaults to None.
        height: The height of the image in pixels. Defaults to None.
        resize_mode (Optional[ResizeMode]): if the overlay is a different size from the base image, define how to display it. "fill" will stretch the overlay to fit the base image dimensions. None will do nothing.
        coordinate_frame: The coordinate frame. Defaults to None.
        date_captured: ISO formatted date. Defaults to None.
        mirror_asset: request this asset to be saved to Aquarium Storage. Useful for Short duration signed URL assets.
    """

    _valid_cf_types = {"IMAGE"}
    _default_cf_class = _ImageCoordinateFrame

    def __init__(
        self,
        *,
        overlay_id: str,
        image_url: str,
        id: str = DEFAULT_SENSOR_ID,
        width: Optional[int] = None,
        height: Optional[int] = None,
        resize_mode: Optional[ResizeMode] = None,
        coordinate_frame: Optional[CoordinateFrame2D] = None,
        date_captured: Optional[str] = None,
        mirror_asset: bool = False,
    ):
        if not isinstance(overlay_id, str):
            raise Exception("overlay ids must be strings")

        sensor_metadata: Dict[str, Union[str, int]] = {
            "overlay_id": overlay_id,
            "resize_mode": str(resize_mode),
        }

        if width is not None:
            if not isinstance(width, int):
                raise Exception("width must be an int")
            sensor_metadata["width"] = width

        if height is not None:
            if not isinstance(height, int):
                raise Exception("height must be an int")
            sensor_metadata["height"] = height

        data_urls = {"image_url": image_url}

        super().__init__(
            id,
            "IMAGE_OVERLAY_V0",
            data_urls,
            mirror_asset,
            metadata=sensor_metadata,
            coordinate_frame=coordinate_frame,
            date_captured=date_captured,
        )


class Text(_BaseSensor):
    """Create a text "sensor" datapoint to add to a frame.

    Args:
        text: The text body.
        id: id of sensor that generates this datapoint (defaults to "DEFAULT").
        date_captured: ISO formatted date. Defaults to None.
    """

    _valid_cf_classes = {_BaseCoordinateFrame}
    _valid_cf_types = {"TEXT"}
    _default_cf_class = _TextCoordinateFrame

    def __init__(
        self,
        *,
        text: str,
        id: str = DEFAULT_SENSOR_ID,
        date_captured: Optional[str] = None,
    ):
        super().__init__(
            id,
            "TEXT",
            {"text": text},
            False,
            date_captured=date_captured,
        )


class PointCloudPCD(_BaseSensor3D):
    """Create a point cloud sensor data point to add to a frame,
    contained in PCD format. ascii, binary, and binary_compressed formats are supported.
    Numeric values for the following column names are expected:
    x, y, z, intensity (optional), range (optional)

    Args:
        pcd_url: URL to PCD formated data.
        id: id of sensor that generates this datapoint (defaults to "DEFAULT").
        coordinate_frame: The coordinate frame id. Defaults to None.
        date_captured: ISO formatted date. Defaults to None.
        mirror_asset: request this asset to be saved to Aquarium Storage. Useful for Short duration signed URL assets.
    """

    def __init__(
        self,
        *,
        pcd_url: str,
        id: str = DEFAULT_SENSOR_ID,
        coordinate_frame: Optional[CoordinateFrame3D] = None,
        date_captured: Optional[str] = None,
        mirror_asset: bool = False,
    ):
        super().__init__(
            id,
            "POINTCLOUD_PCD_V0",
            {"pcd_url": pcd_url},
            mirror_asset,
            coordinate_frame=coordinate_frame,
            date_captured=date_captured,
        )


class PointCloudBins(_BaseSensor3D):
    """Create a point cloud sensor data point to this frame, contained in dense binary files of
    little-endian values, similar to the raw format of KITTI lidar data. You can provide
    a combination of the following values, as long as at least either kitti_format_url or
    pointcloud_url are provided.

    Args:
        id: id of sensor that generates this datapoint (defaults to "DEFAULT").
        pointcloud_url: URL for the pointcloud: float32 [x1, y1, z1, x2, y2, z2, ...].
        kitti_format_url: URL for the pointcloud + intensity: float32 [x1, y1, z1, i1, x2, y2, z2, i2, ...].
        intensity_url: URL for the Intensity Pointcloud: unsigned int32 [i1, i2, ...].
        range_url: URL for the Range Pointcloud: float32 [r1, r2, ...].
        coordinate_frame: The coordinate frame id. Defaults to None.
        date_captured: ISO formatted date. Defaults to None.
        mirror_asset: request this asset to be saved to Aquarium Storage. Useful for Short duration signed URL assets.
    """

    def __init__(
        self,
        *,
        id: str = DEFAULT_SENSOR_ID,
        pointcloud_url: Optional[str] = None,
        kitti_format_url: Optional[str] = None,
        intensity_url: Optional[str] = None,
        range_url: Optional[str] = None,
        coordinate_frame: Optional[CoordinateFrame3D] = None,
        date_captured: Optional[str] = None,
        mirror_asset: bool = False,
    ):
        if pointcloud_url is None and kitti_format_url is None:
            raise Exception(
                "Either pointcloud_url or kitti_format_url must be provided."
            )

        if pointcloud_url is not None and kitti_format_url is not None:
            raise Exception(
                "Only one of pointcloud_url or kitti_format_url must be provided."
            )

        data_urls = {}
        if pointcloud_url is not None:
            data_urls["pointcloud_url"] = pointcloud_url
        if kitti_format_url is not None:
            data_urls["kitti_format_url"] = kitti_format_url
        if range_url is not None:
            data_urls["range_url"] = range_url
        if intensity_url is not None:
            data_urls["intensity_url"] = intensity_url

        super().__init__(
            id,
            "POINTCLOUD_V0",
            data_urls,
            mirror_asset,
            coordinate_frame=coordinate_frame,
            date_captured=date_captured,
        )


class Obj(_BaseSensor3D):
    """Create a .obj file for text based geometry.

    Args:
        obj_url: URL to where the object is located.
        id: id of sensor that generates this datapoint (defaults to "DEFAULT").
        coordinate_frame: The coordinate frame. Defaults to None.
        date_captured: ISO formatted date. Defaults to None.
        mirror_asset: request this asset to be saved to Aquarium Storage. Useful for Short duration signed URL assets.
    """

    def __init__(
        self,
        *,
        obj_url: str,
        id: str = DEFAULT_SENSOR_ID,
        coordinate_frame: Optional[CoordinateFrame3D] = None,
        date_captured: Optional[str] = None,
        mirror_asset: bool = False,
    ):
        super().__init__(
            id,
            "OBJ_V0",
            {"obj_url": obj_url},
            mirror_asset,
            coordinate_frame=coordinate_frame,
            date_captured=date_captured,
        )


class Audio(_BaseSensor):
    """.. experimental::

    Create an audio "sensor" datapoint to add to a frame.

    Args:
        audio_url: The URL to load this audio data (mp3, etc.).
        id: id of sensor that generates this datapoint (defaults to "DEFAULT").
        date_captured: ISO formatted date. Defaults to None.
        mirror_asset: request this asset to be saved to Aquarium Storage. Useful for Short duration signed URL assets.
    """

    _valid_cf_classes = {_BaseCoordinateFrame}
    _valid_cf_types = {"AUDIO"}
    _default_cf_class = _AudioCoordinateFrame

    def __init__(
        self,
        *,
        audio_url: str,
        id: str = DEFAULT_SENSOR_ID,
        date_captured: Optional[str] = None,
        mirror_asset: bool = False,
    ):
        super().__init__(
            id,
            "AUDIO_V0",
            {"audio_url": audio_url},
            mirror_asset,
            date_captured=date_captured,
        )


class Video(_BaseSensor):
    """.. experimental::

    Create a video "sensor" datapoint to add to a frame.

    Args:
        video_url: The URL to load this video data (mp4, webm, etc.).
        id: id of sensor that generates this datapoint (defaults to "DEFAULT").
        date_captured: ISO formatted date. Defaults to None.
        mirror_asset: Request this asset to be saved to Aquarium Storage. Useful for Short duration signed URL assets.
    """

    _valid_cf_classes = {_BaseCoordinateFrame}
    _valid_cf_types = {"VIDEO"}
    _default_cf_class = _VideoCoordinateFrame

    def __init__(
        self,
        *,
        video_url: str,
        id: str = DEFAULT_SENSOR_ID,
        date_captured: Optional[str] = None,
        mirror_asset: bool = False,
    ):
        super().__init__(
            id,
            "VIDEO_V0",
            {"video_url": video_url},
            mirror_asset,
            date_captured=date_captured,
        )


SensorData2D = Union[Image, ImageOverlay]
SensorData3D = Union[PointCloudPCD, PointCloudBins, Obj]
SensorData = Union[SensorData2D, SensorData3D, Text, Audio, Video]


# TODO: figure out a less fragile way to do this? we're lucky in that we don't change any of the kwarg names when keying into metadata
def _get_sensor_data_from_json(
    sd_json: Dict[str, Any], coordinate_frames_by_id: Dict[str, CoordinateFrame] = {}
) -> SensorData:
    sensor_id = sd_json["sensor_id"]
    sensor_metadata = sd_json["sensor_metadata"]
    sensor_type = sd_json["sensor_type"]
    data_urls = sd_json["data_urls"]
    date_captured = sd_json["date_captured"]
    mirror_asset = sd_json["mirror_asset"]

    cf_id = sd_json["coordinate_frame"]
    coordinate_frame = coordinate_frames_by_id.get(cf_id)

    sensor_data: SensorData

    # set coordinate frames directly to bypass type checking
    # trust what we allowed in the past/reconstructed from the frame dict
    if sensor_type == "IMAGE_V0":
        sensor_data = Image(
            id=sensor_id,
            date_captured=date_captured,
            mirror_asset=mirror_asset,
            **data_urls,
            **sensor_metadata,
        )
        sensor_data.coordinate_frame = coordinate_frame
    elif sensor_type == "IMAGE_OVERLAY_V0":
        sensor_data = ImageOverlay(
            id=sensor_id,
            date_captured=date_captured,
            mirror_asset=mirror_asset,
            **data_urls,
            **sensor_metadata,
        )
        sensor_data.coordinate_frame = coordinate_frame
    elif sensor_type == "TEXT":
        sensor_data = Text(
            id=sensor_id,
            date_captured=date_captured,
            **data_urls,
            **sensor_metadata,
        )
    elif sensor_type == "POINT_CLOUD_PCD":
        sensor_data = PointCloudPCD(
            id=sensor_id,
            date_captured=date_captured,
            mirror_asset=mirror_asset,
            **data_urls,
            **sensor_metadata,
        )
        sensor_data.coordinate_frame = coordinate_frame
    elif sensor_type == "POINTCLOUD_V0":
        sensor_data = PointCloudBins(
            id=sensor_id,
            date_captured=date_captured,
            mirror_asset=mirror_asset,
            **data_urls,
            **sensor_metadata,
        )
        sensor_data.coordinate_frame = coordinate_frame
    elif sensor_type == "OBJ_V0":
        sensor_data = Obj(
            id=sensor_id,
            date_captured=date_captured,
            mirror_asset=mirror_asset,
            **data_urls,
            **sensor_metadata,
        )
        sensor_data.coordinate_frame = coordinate_frame
    elif sensor_type == "AUDIO_V0":
        sensor_data = Audio(
            id=sensor_id,
            date_captured=date_captured,
            mirror_asset=mirror_asset,
            **data_urls,
            **sensor_metadata,
        )
    elif sensor_type == "VIDEO_V0":
        sensor_data = Video(
            id=sensor_id,
            date_captured=date_captured,
            mirror_asset=mirror_asset,
            **data_urls,
            **sensor_metadata,
        )
    else:
        raise Exception(f"Cannot instantiate sensor data of type {sensor_type}")

    return sensor_data
