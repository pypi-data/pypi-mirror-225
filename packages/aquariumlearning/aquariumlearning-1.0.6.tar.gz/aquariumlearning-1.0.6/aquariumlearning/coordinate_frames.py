import json
from typing import Any, Dict, List, Optional, Tuple, Union

from .util import (
    ALL_CAMERA_MODELS,
    ALL_ORIENTATION_KEYS,
    ALL_POSITION_KEYS,
    CAMERA_MODELS,
    ORIENTATION_KEYS,
    POSITION_KEYS,
    _BaseEntity,
    is_valid_number,
)


class _BaseCoordinateFrame(_BaseEntity):
    """The base class for all coordinate frames

    :meta private:
    """

    _optional_metadata_keys: List[str] = []

    def __init__(
        self,
        id: str,
        type: str,
        default_metadata: Dict[str, Any] = {},
        parent_coordinate_frame: Optional["_BaseCoordinateFrame"] = None,
    ):
        if id == "world" and self.__class__.__name__ != "_WorldCoordinateFrame":
            class_name = self.__class__.__name__
            raise Exception(
                f"{class_name} id cannot be the same as reserved id 'world'"
            )
        super().__init__(id)

        self.type = type
        self.parent_coordinate_frame = parent_coordinate_frame
        self.default_metadata = default_metadata

    def _set_parent(
        self,
        parent: Union[
            "_BaseCoordinateFrame2D", "_BaseCoordinateFrame3D", "_BaseCoordinateFrame"
        ],
    ) -> None:
        if isinstance(self, _BaseCoordinateFrame3D) and not isinstance(
            parent, _BaseCoordinateFrame3D
        ):
            raise Exception(
                f"{self.__class__.__name__} cannot have a parent of type {parent.__class__.__name__}; 3D coordinate frames can only descend from other 3D coordinate frames"
            )

        self.parent_coordinate_frame = parent

    def to_dict(self) -> Dict[str, Any]:
        metadata = {**self.default_metadata}
        metadata["parent_frame_id"] = (
            self.parent_coordinate_frame.id if self.parent_coordinate_frame else None
        )

        for key in self._optional_metadata_keys:
            self_value = getattr(self, key, None)
            if self_value is not None:
                metadata[key] = self_value

        return {
            "coordinate_frame_id": self.id,
            "coordinate_frame_type": self.type,
            "coordinate_frame_metadata": json.dumps(metadata),
        }


class _BaseCoordinateFrame2D(_BaseCoordinateFrame):
    """A base 2D coordinate frame so that we can do validation on any kind of 2D sensor data

    :meta private:
    """

    pass


class _BaseCoordinateFrame3D(_BaseCoordinateFrame):
    """A base 3D coordinate frame so that we can do validation on any kind of 3D sensor data

    :meta private:
    """

    pass


class _WorldCoordinateFrame(_BaseCoordinateFrame3D):
    """Internal WORLD coordinate frame to auto-associate with 3D sensor data

    :meta private:
    """

    # pass a dummy _id to match the interface
    def __init__(self, _id: str = "world") -> None:
        super().__init__("world", "WORLD", {})


class _ImageCoordinateFrame(_BaseCoordinateFrame2D):
    """Internal IMAGE coordinate frame to auto-associate with image sensor data

    :meta private:
    """

    def __init__(self, sensor_id: str) -> None:
        super().__init__(sensor_id, "IMAGE", {})


class _AudioCoordinateFrame(_BaseCoordinateFrame):
    """Internal AUDIO coordinate frame to auto-associate with audio sensor data

    :meta private:
    """

    def __init__(self, sensor_id: str) -> None:
        super().__init__(sensor_id, "AUDIO", {})


class _TextCoordinateFrame(_BaseCoordinateFrame):
    """Internal TEXT coordinate frame to auto-associate with text sensor data

    :meta private:
    """

    def __init__(sel, sensor_id: str) -> None:
        super().__init__(sensor_id, "TEXT", {})


class _VideoCoordinateFrame(_BaseCoordinateFrame):
    """Internal VIDEO coordinate frame to auto-associate with video sensor data

    :meta private:
    """

    def __init__(self, sensor_id: str) -> None:
        super().__init__(sensor_id, "VIDEO", {})


class CoordinateFrame2D(_BaseCoordinateFrame2D):
    """Create a 2D Coordinate Frame

    Args:
        id: String identifier for this coordinate frame.
        fx: focal length x in pixels.
        fy: focal length y in pixels.
        camera_model: Either "fisheye" for the fisheye model, or "brown_conrady" for the pinhole model with Brown-Conrady distortion. Defaults to "brown_conrady".
        position: Dict of the form {x, y, z}. Defaults to {x: 0, y: 0, z: 0}.
        orientation: Quaternion rotation dict of the form {w, x, y, z}. Defaults to {x: 0, y: 0, z: 0, w: 1}.
        camera_matrix: 4x4 row major order camera matrix mapping 3d world space to camera space (x right, y down, z forward). Keep in mind, if you pass in the camera matrix it will stack on top of the position/orientation you pass in as well. This is only needed if you cannot properly represent your camera using the position/orientation parameters. Defaults to None.
        cx: optical center pixel x coordinate. Defaults to x center of image.
        cy: optical center pixel y coordinate. Defaults to y center of image.
        k1: k1 radial distortion coefficient (Brown-Conrady, fisheye). Defaults to 0.
        k2: k2 radial distortion coefficient (Brown-Conrady, fisheye). Defaults to 0.
        k3: k3 radial distortion coefficient (Brown-Conrady, fisheye). Defaults to 0.
        k4: k4 radial distortion coefficient (Brown-Conrady, fisheye). Defaults to 0.
        k5: k5 radial distortion coefficient (Brown-Conrady). Defaults to 0.
        k6: k6 radial distortion coefficient (Brown-Conrady). Defaults to 0.
        p1: p1 tangential distortion coefficient (Brown-Conrady). Defaults to 0.
        p2: p2 tangential distortion coefficient (Brown-Conrady). Defaults to 0.
        s1: s1 thin prism distortion coefficient (Brown-Conrady). Defaults to 0.
        s2: s2 thin prism distortion coefficient (Brown-Conrady). Defaults to 0.
        s3: s3 thin prism distortion coefficient (Brown-Conrady). Defaults to 0.
        s4: s4 thin prism distortion coefficient (Brown-Conrady). Defaults to 0.
        skew: camera skew coefficient (fisheye). Defaults to 0.
        parent_coordinate_frame: The parent coordinate frame. Defaults to None.
    """

    _optional_metadata_keys = [
        "camera_matrix",
        "k1",
        "k2",
        "k3",
        "k4",
        "k5",
        "k6",
        "p1",
        "p2",
        "cx",
        "cy",
        "s1",
        "s2",
        "s3",
        "s4",
        "skew",
    ]

    def __init__(
        self,
        id: str,
        fx: Union[int, float],
        fy: Union[int, float],
        camera_model: Optional[CAMERA_MODELS] = None,
        position: Optional[Dict[POSITION_KEYS, Union[int, float]]] = None,
        orientation: Optional[Dict[ORIENTATION_KEYS, Union[int, float]]] = None,
        camera_matrix: Optional[List[List[Union[int, float]]]] = None,
        k1: Optional[Union[int, float]] = None,
        k2: Optional[Union[int, float]] = None,
        k3: Optional[Union[int, float]] = None,
        k4: Optional[Union[int, float]] = None,
        k5: Optional[Union[int, float]] = None,
        k6: Optional[Union[int, float]] = None,
        p1: Optional[Union[int, float]] = None,
        p2: Optional[Union[int, float]] = None,
        cx: Optional[Union[int, float]] = None,
        cy: Optional[Union[int, float]] = None,
        s1: Optional[Union[int, float]] = None,
        s2: Optional[Union[int, float]] = None,
        s3: Optional[Union[int, float]] = None,
        s4: Optional[Union[int, float]] = None,
        skew: Optional[Union[int, float]] = None,
        parent_coordinate_frame: Optional[
            Union["CoordinateFrame2D", "CoordinateFrame3D"]
        ] = None,
    ):
        super().__init__(
            id,
            "IMAGE_PROJECTION",
            default_metadata={
                "fx": fx,
                "fy": fy,
                "camera_model": camera_model,
                "position": position,
                "orientation": orientation,
            },
            parent_coordinate_frame=parent_coordinate_frame,
        )

        if position is None:
            position = {"x": 0, "y": 0, "z": 0}
        if type(position) is not dict:
            raise Exception("position improperly formatted")
        for position_key in ALL_POSITION_KEYS:
            if not is_valid_number(position[position_key]):
                raise Exception("position coordinates must be valid numbers")

        if orientation is None:
            orientation = {"w": 1, "x": 0, "y": 0, "z": 0}
        if type(orientation) is not dict:
            raise Exception("orientation improperly formatted")
        for orientation_key in ALL_ORIENTATION_KEYS:
            if not is_valid_number(orientation[orientation_key]):
                raise Exception("orientation coordinates must be valid numbers")

        if camera_matrix is not None:
            if type(camera_matrix) != list:
                raise Exception("camera matrix must be a python list of lists")
            if len(camera_matrix) != 4:
                raise Exception("camera matrix is not a properly formatted 4x4 matrix")
            for row in camera_matrix:
                if type(camera_matrix) != list:
                    raise Exception("camera matrix must be a python list of lists")
                if len(row) != 4:
                    raise Exception(
                        "camera matrix is not a properly formatted 4x4 matrix"
                    )
                for el in row:
                    if not is_valid_number(el):
                        raise Exception(
                            "element within camera matrix not a valid float/int"
                        )

        if not is_valid_number(fx) or not is_valid_number(fy):
            raise Exception("focal lengths are required and must be valid numbers")

        if fx == 0 or fy == 0:
            raise Exception("focal lengths cannot be 0")

        if camera_model is None:
            camera_model = "brown_conrady"

        if not isinstance(camera_model, str) or camera_model not in ALL_CAMERA_MODELS:
            raise Exception(
                "invalid camera model, valid values are {}".format(ALL_CAMERA_MODELS)
            )

        for coord in [k1, k2, k3, k4, k5, k6, p1, p2, cx, cy, s1, s2, s3, s4, skew]:
            if coord is not None and not is_valid_number(coord):
                raise Exception(
                    f"{coord} is not a valid 2D coordinate frame attribute. Must be float/int/None"
                )

        if (cx is None and cy is not None) or (cx is not None and cy is None):
            raise Exception("optical centers must both be None or both be numbers")
        if (cx is not None and cx <= 0) or (cy is not None and cy <= 0):
            raise Exception("optical centers must be greater than 0")

        self.fx = fx
        self.fy = fy
        self.camera_model = camera_model
        self.position = position
        self.orientation = orientation
        self.camera_matrix = camera_matrix
        self.k1 = k1
        self.k2 = k2
        self.k3 = k3
        self.k4 = k4
        self.k5 = k5
        self.k6 = k6
        self.p1 = p1
        self.p2 = p2
        self.cx = cx
        self.cy = cy
        self.s1 = s1
        self.s2 = s2
        self.s3 = s3
        self.s4 = s4
        self.skew = skew


class CoordinateFrame3D(_BaseCoordinateFrame3D):
    """Create a 3D Coordinate Frame

    Args:
        id: String identifier for this coordinate frame
        position: Dict of the form {x, y, z}. Defaults to None.
        orientation: Quaternion rotation dict of the form {w, x, y, z}. Defaults to None.
        parent_coordinate_frame: The parent coordinate frame. Defaults to None.
    """

    def __init__(
        self,
        id: str,
        position: Optional[Dict[POSITION_KEYS, Union[int, float]]] = None,
        orientation: Optional[Dict[ORIENTATION_KEYS, Union[int, float]]] = None,
        parent_coordinate_frame: Optional["CoordinateFrame3D"] = None,
    ):
        if position is None:
            position = {"x": 0, "y": 0, "z": 0}
        if type(position) is not dict:
            raise Exception("position improperly formatted")
        for position_key in ALL_POSITION_KEYS:
            if not is_valid_number(position[position_key]):
                raise Exception("position coordinates must be valid numbers")

        if orientation is None:
            orientation = {"w": 1, "x": 0, "y": 0, "z": 0}
        if type(orientation) is not dict:
            raise Exception("orientation improperly formatted")
        for orientation_key in ALL_ORIENTATION_KEYS:
            if not is_valid_number(orientation[orientation_key]):
                raise Exception("orientation coordinates must be valid numbers")

        super().__init__(
            id,
            "WORLD",
            default_metadata={
                "position": position,
                "orientation": orientation,
            },
            parent_coordinate_frame=parent_coordinate_frame,
        )


CoordinateFrame = Union[CoordinateFrame2D, CoordinateFrame3D]


def _get_coordinate_frame_from_json(
    cf_json: Dict[str, Any]
) -> Optional[CoordinateFrame]:
    cf_type = cf_json["coordinate_frame_type"]
    cf_id = cf_json["coordinate_frame_id"]
    cf_metadata = cf_json.get("coordinate_frame_metadata", "{}")

    try:
        cf_metadata = json.loads(cf_metadata)
    except:
        pass

    cf_metadata.pop("parent_frame_id", None)

    if cf_type == "IMAGE_PROJECTION":
        return CoordinateFrame2D(cf_id, **cf_metadata)
    elif cf_type == "WORLD" and cf_id != "world":
        return CoordinateFrame3D(cf_id, **cf_metadata)
    return None
