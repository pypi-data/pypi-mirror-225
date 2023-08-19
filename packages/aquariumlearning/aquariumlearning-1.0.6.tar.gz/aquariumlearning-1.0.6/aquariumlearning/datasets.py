import datetime
import json
import numpy as np
import pandas as pd
import pyarrow as pa
from tempfile import NamedTemporaryFile
from warnings import warn

from typing import Any, Callable, Dict, List, Optional, IO, Set, Union, TYPE_CHECKING
from typing_extensions import Literal

from .coordinate_frames import CoordinateFrame
from .dataset_client import DatasetClient
from .datasharing import _check_urls, _get_errors, _get_mode
from .frames import (
    CustomMetricsEntry,
    Frame,
    FrameType,
    GeoData,
    DeletedFrame,
    LabeledFrame,
    InferenceFrame,
    ModifiedLabeledFrame,
    UnlabeledFrame,
    UnlabeledFrameV2,
    UserMetadataEntry,
)
from .inferences import Inference
from .labels import Label
from .modified_labels import ModifiedLabel
from .sensor_data import SensorData
from .util import (
    DUMMY_FRAME_EMBEDDING,
    MAX_FRAMES_PER_BATCH,
    MAX_DATAPOINTS_PER_BATCH,
    _BaseEntity,
    _is_one_gb_available,
    EmbeddingDistanceMetric,
    assert_valid_name,
    create_temp_directory,
    mark_temp_directory_complete,
)

if TYPE_CHECKING:
    from .client import Client

_PipelineMode = Union[Literal["STREAMING"], Literal["BATCH"]]


class _Dataset(_BaseEntity):
    """Internal base class for labeled, unlabeled, and inference sets

    Args:
        client: an instance of Client that we can use to validate dataset & frames before upload
        id: the dataset id
        project_name: the project name
        crop_embedding_model (str, optional)
        frame_embedding_model (str, optional)
        embedding_distance_metric (str, optional) defaults to "cosine"
        external_metadata: A JSON object that can be used to attach metadata to the dataset itself
        is_anon_mode: flag to tell aquarium if url images are reachable from public internet or shared bucket. False if reachable, True if Not.
        pipeline_mode (Union[Literal["STREAMING], Literal["BATCH]): a strictly internal flag. the batch pipeline is fully deprecated except for unlabeled ingest v2
        experiment_streaming_v2: A flag that determines how frames are flushed & which version of the streaming ingest pipeline to use
    :meta private:
    """

    _checked_first_frame_urls: bool
    _split_frame_crop_files: bool
    _frames: List[Frame]
    _frame_ids_set: Set[str]
    _crop_ids_set: Set[str]
    _crop_class_id_set: Set[int]
    _crop_class_name_set: Set[str]
    _crop_count_total: int
    _temp_frame_file_names: List[str]
    _temp_frame_asset_file_names: List[str]
    _temp_frame_embeddings_file_names: List[str]
    _temp_frame_count_per_file: List[int]
    _temp_crop_count_per_file: List[int]
    _temp_frame_file_names_streaming: List[str]
    _temp_frame_embeddings_file_names_streaming: List[str]
    _temp_frame_count_per_file_streaming: List[int]
    _temp_crop_file_names_streaming: List[str]
    _temp_crop_embeddings_file_names_streaming: List[str]
    _temp_crop_count_per_file_streaming: List[int]

    first_frame: Optional[Frame]
    project_name: str
    crop_embedding_dim: Optional[int]
    frame_embedding_dim: Optional[int]
    crop_embedding_model: Optional[str]
    frame_embedding_model: Optional[str]
    sample_frame_embeddings: List[List[float]]
    sample_crop_embeddings: List[List[float]]
    embedding_distance_metric: str
    external_metadata: Optional[Dict[str, Any]]
    is_anon_mode: bool
    _dataset_client: DatasetClient
    _pipeline_mode: _PipelineMode
    _streaming_version: int

    _allowed_frame_types: Set[FrameType]

    def __init__(
        self,
        client: "Client",
        id: str,
        project_name: str,
        crop_embedding_model: Optional[str] = None,
        frame_embedding_model: Optional[str] = None,
        embedding_distance_metric: EmbeddingDistanceMetric = EmbeddingDistanceMetric.COSINE,
        external_metadata: Optional[Dict[str, Any]] = None,
        is_anon_mode: bool = False,
        pipeline_mode: _PipelineMode = "STREAMING",
        streaming_version: int = 0,
    ):
        assert_valid_name(id)
        super().__init__(id)
        if not isinstance(embedding_distance_metric, EmbeddingDistanceMetric):
            raise Exception(
                "embedding_distance_metric must be a member of EmbeddingDistanceMetric."
            )

        self.project_name = project_name
        self._dataset_client = DatasetClient.get_or_init(client, project_name, id)
        self._pipeline_mode = pipeline_mode
        self._streaming_version = streaming_version
        self.is_anon_mode = is_anon_mode

        if external_metadata is not None:
            if not isinstance(external_metadata, dict) or (
                external_metadata and not isinstance(next(iter(external_metadata)), str)
            ):
                raise Exception("external_metadata must be a dict with string keys")

        self.external_metadata = external_metadata

        self._frames = []
        self._frame_ids_set = set()
        self._crop_ids_set = set()
        self._crop_class_id_set = set()
        self._crop_class_name_set = set()

        current_time = datetime.datetime.now()
        self.temp_file_path = create_temp_directory()
        self._temp_frame_prefix = "al_{}_dataset_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_assets_prefix = "al_{}_dataset_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_embeddings_prefix = "al_{}_dataset_frame_embeddings_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_crop_prefix = "al_{}_dataset_crops_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_crop_embeddings_prefix = "al_{}_dataset_crop_embeddings_".format(
            current_time.strftime("%Y%m%d_%H%M%S_%f")
        )
        self._temp_frame_latest_window_prefix = (
            "al_{}_dataset_frame_latest_windows_".format(
                current_time.strftime("%Y%m%d_%H%M%S_%f")
            )
        )
        self._temp_frame_file_names = []
        self._temp_frame_embeddings_file_names = []
        self._temp_frame_asset_file_names = []
        self._temp_frame_count_per_file = []
        self._temp_crop_count_per_file = []
        self._temp_frame_file_names_streaming = []
        self._temp_frame_embeddings_file_names_streaming = []
        self._temp_frame_count_per_file_streaming = []
        self._temp_crop_file_names_streaming = []
        self._temp_crop_embeddings_file_names_streaming = []
        self._temp_crop_count_per_file_streaming = []
        self._crop_count_total = 0
        self._checked_first_frame_urls = False

        self.crop_embedding_dim = None
        self.frame_embedding_dim = None
        self.crop_embedding_model = crop_embedding_model
        self.frame_embedding_model = frame_embedding_model
        self.embedding_distance_metric = embedding_distance_metric.value
        self.sample_frame_embeddings = []
        self.sample_crop_embeddings = []
        self.first_frame = None

    def _cleanup_temp_dir(self) -> None:
        mark_temp_directory_complete(self.temp_file_path)

    def _save_rows_to_temp(
        self,
        file_name_prefix: str,
        writefunc: Callable[[IO[Any]], None],
        mode: str = "w",
    ) -> Optional[str]:
        """[summary]

        Args:
            file_name_prefix (str): prefix for the filename being saved
            writefunc ([filelike): function used to write data to the file opened

        Returns:
            str or None: path of file or none if nothing written
        """

        if not _is_one_gb_available():
            raise OSError(
                "Attempting to flush dataset to disk with less than 1 GB of available disk space. Exiting..."
            )

        data_rows_content = NamedTemporaryFile(
            mode=mode, delete=False, prefix=file_name_prefix, dir=self.temp_file_path
        )
        data_rows_content_path = data_rows_content.name
        writefunc(data_rows_content)

        # Nothing was written, return None
        if data_rows_content.tell() == 0:
            return None

        data_rows_content.seek(0)
        data_rows_content.close()
        return data_rows_content_path

    def _run_flush_to_disk_if_necessary(self) -> None:
        """Flushes the dataset to disk if the dataset is too large to fit in memory"""

        if len(self._frames) + self._crop_count_total > MAX_DATAPOINTS_PER_BATCH:
            self._flush_to_disk()

            self._frames = []
            self._crop_count_total = 0

    def _flush_to_disk(self) -> None:
        """Writes the all the frames in the frame buffer to temp file on disk"""
        if self._split_frame_crop_files:
            self._flush_to_disk_streaming()
        else:
            if len(self._frames) == 0:
                return
            frame_path = self._save_rows_to_temp(
                self._temp_frame_prefix, lambda x: self._write_batch_to_file(x)
            )
            if frame_path:
                self._temp_frame_file_names.append(frame_path)
                self._temp_frame_count_per_file.append(len(self._frames))
                self._temp_crop_count_per_file.append(self._crop_count_total)
            embeddings_path = self._save_rows_to_temp(
                self._temp_frame_embeddings_prefix,
                lambda x: self._write_batch_embeddings_to_file(x),
                mode="wb",
            )
            if embeddings_path:
                self._temp_frame_embeddings_file_names.append(embeddings_path)

            assets_path = self._save_rows_to_temp(
                self._temp_frame_assets_prefix,
                lambda x: self._write_batch_crop_assets_to_file(x),
                mode="wb",
            )
            if assets_path:
                self._temp_frame_asset_file_names.append(assets_path)

    def _flush_to_disk_streaming(self) -> None:
        """Writes the all the frames in the frame buffer to temp file on disk"""

        if len(self._frames) == 0:
            return
        frame_path = self._save_rows_to_temp(
            self._temp_frame_prefix, lambda x: self._write_frames_to_file_streaming(x)
        )
        crop_path = self._save_rows_to_temp(
            self._temp_crop_prefix, lambda x: self._write_crops_to_file_streaming(x)
        )
        if frame_path:
            self._temp_frame_file_names_streaming.append(frame_path)
            self._temp_frame_count_per_file_streaming.append(len(self._frames))
        if crop_path:
            self._temp_crop_file_names_streaming.append(crop_path)
            self._temp_crop_count_per_file_streaming.append(self._crop_count_total)

        frame_embeddings_path = self._save_rows_to_temp(
            self._temp_frame_embeddings_prefix,
            lambda x: self._write_frame_embeddings_to_file_streaming(x),
            mode="wb",
        )
        if frame_embeddings_path:
            self._temp_frame_embeddings_file_names_streaming.append(
                frame_embeddings_path
            )

        crop_embeddings_path = self._save_rows_to_temp(
            self._temp_crop_embeddings_prefix,
            lambda x: self._write_crop_embeddings_to_file_streaming(x),
            mode="wb",
        )
        if crop_embeddings_path:
            self._temp_crop_embeddings_file_names_streaming.append(crop_embeddings_path)

        assets_path = self._save_rows_to_temp(
            self._temp_frame_assets_prefix,
            lambda x: self._write_batch_crop_assets_to_file(
                x
            ),  # TODO: validate this even works??
            mode="wb",
        )
        if assets_path:
            self._temp_frame_asset_file_names.append(assets_path)

    def _check_frame_urls(
        self,
        frame: Frame,
    ) -> None:
        if frame.sensor_data:
            for sensor_datum in frame.sensor_data:
                urls = list(sensor_datum.data_urls.values())
                local_results = _check_urls(urls, None)
                server_results = self._dataset_client._verify_urls(urls)
                mode = _get_mode(urls, local_results, server_results)
                errors, warnings, is_anon = _get_errors(mode)
                if len(errors) > 0:
                    error_str = "\n".join(errors)
                    raise Exception(f"URL ACCESS ERRORS FOUND: {error_str}")
                if len(warnings) > 0:
                    warning_str = "\n".join(warnings)
                    print(f"WARNING: {warning_str}")

                if is_anon and not frame._is_derivative_frame and not frame.embedding:
                    class_name = self.__class__.__name__
                    if not self.is_anon_mode:
                        anon_urls = [
                            url
                            for url in mode
                            if mode[url] == "ANONYMOUS" or mode[url] == "S3_PATH"
                        ]
                        # require one or the other
                        raise Exception(
                            f"Could not access this frame {frame.id}'s urls {anon_urls} from Aquarium servers. "
                            "This means Aquarium will not be able to generate embeddings for your frames. "
                            f"Either reinitialize {class_name} with is_anon_mode=True or provide your own embeddings when initializing the frame. "
                        )
                    else:
                        print(
                            f"WARNING: is_anon_mode is True for {class_name} {self.id} but frame {frame.id} does not have provided embeddings. "
                            "Aquarium will not be able to compute these embeddings in anon mode since images are inaccessible from its server. "
                            "Please provide your own embeddings if you want to use the embedding view in the Aquarium app."
                        )

    def _add_frame(self, frame: Frame) -> None:
        if frame.id in self._frame_ids_set:
            raise Exception(f"Attempted to add duplicate frame id: {frame.id}.")

        duplicate_label_ids = frame._crop_set._crop_ids_set & self._crop_ids_set
        if duplicate_label_ids:
            raise Exception(
                f"Attempted to add duplicate label id(s): {duplicate_label_ids}"
            )

        if not isinstance(frame, tuple(self._allowed_frame_types)):
            allowed_frame_types = [
                fc.__class__.__name__ for fc in self._allowed_frame_types
            ]
            raise Exception(
                f"Cannot add frame of type {frame.__class__.__name__} to a {self.__class__.__name__}; valid frame types are {allowed_frame_types}"
            )

        if frame.embedding and not self.frame_embedding_model:
            class_name = self.__class__.__name__
            raise Exception(
                f"Cannot add a frame with embeddings without a defined embedding model. Please reinitialize {class_name} with frame_embedding_model set"
            )

        if not self._checked_first_frame_urls:
            self._check_frame_urls(frame)
            self._checked_first_frame_urls = True

        if self.frame_embedding_dim is None:
            self.frame_embedding_dim = frame.embedding_dim
        elif self.frame_embedding_dim != frame.embedding_dim:
            if not frame.reuse_latest_embedding:
                raise Exception(
                    f"Length of frame embeddings must be the same, existing embeddings are of dimension {self.frame_embedding_dim} but new embedding has dimension {frame.embedding_dim}"
                )

        if frame.embedding and len(self.sample_frame_embeddings) < 5:
            self.sample_frame_embeddings.append(frame.embedding)

        crop_embedding_dim = (
            frame._crop_set.crop_embedding_dim
            if frame._crop_set.crop_embedding_dim
            else -1
        )
        if self.crop_embedding_dim is None:
            self.crop_embedding_dim = crop_embedding_dim
        elif crop_embedding_dim > 0 and self.crop_embedding_dim != crop_embedding_dim:
            raise Exception(
                f"Length of label or inference embeddings must be the same, existing embeddings are of dimension {self.crop_embedding_dim} but new embedding has dimension {crop_embedding_dim}"
            )
        if crop_embedding_dim > 0 and not self.crop_embedding_model:
            class_name = self.__class__.__name__
            raise Exception(
                f"Cannot add a label with embeddings without a defined embedding model. Please reinitialize {class_name} with label_embedding_model or inference_embedding_model set"
            )

        if (
            frame._crop_set.crop_embedding_dim is not None
            and len(self.sample_crop_embeddings) < 5
        ):
            remaining = 5 - len(self.sample_crop_embeddings)
            self.sample_crop_embeddings += [
                c.embedding for c in frame._crop_set.crops[0:remaining] if c.embedding
            ]

        # very special casing: models of the same name must produce embeddings of the same length
        if (
            self.frame_embedding_dim is not None
            and self.crop_embedding_dim is not None
            and self.frame_embedding_dim != self.crop_embedding_dim
            and self.frame_embedding_model == self.crop_embedding_model
        ):
            class_name = self.__class__.__name__
            raise Exception(
                f"Cannot attribute embeddings of different length to the same embedding model name. "
                f"{self.frame_embedding_model} has produced embeddings of length {self.frame_embedding_dim} "
                f"while for labels or inferences it has produced embeddings of length {self.crop_embedding_dim}. "
                f"Please reinitialize {class_name} with different values for frame_embedding_model and label_embedding_model (or inference_embedding_model)"
            )

        # backfill crop embeddings if only frame embeddings are provided
        if not frame._crop_set.crop_embedding_dim and frame.embedding_dim != -1:
            for c in frame._crop_set.crops:
                if (
                    c.label_type in ["CLASSIFICATION_2D", "CLASSIFICATION_3D"]
                    or c.reuse_latest_embedding
                ):
                    continue
                frame._crop_set._add_crop_embedding(c, DUMMY_FRAME_EMBEDDING)
        # and inverse, backfill frame embeddings if only crop embeddings are provided
        elif (
            frame._crop_set.crop_embedding_dim
            and frame.embedding_dim == -1
            and not frame.reuse_latest_embedding
        ):
            frame._add_embedding(DUMMY_FRAME_EMBEDDING)

        self._frames.append(frame)
        self._frame_ids_set.add(frame.id)
        self._crop_ids_set.update(frame._crop_set._crop_ids_set)
        self._crop_class_id_set.update(frame._crop_set._crop_class_id_set)
        self._crop_class_name_set.update(frame._crop_set._crop_class_name_set)
        self._crop_count_total += frame.crop_count()

        if not self.first_frame:
            self.first_frame = frame

        self._run_flush_to_disk_if_necessary()

    def _write_batch_to_file(self, filelike: IO[Any]) -> None:
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        for frame in self._frames:
            if frame.update_type != "ADD":
                continue
            row = frame.to_dict()
            row["label_data"] = frame._crop_set.to_dict()["label_data"]
            filelike.write(json.dumps(row) + "\n")

    # TODO: Does this need a streaming equivalent?
    def _write_batch_crop_assets_to_file(self, filelike: IO[Any]) -> None:
        """Write the frame's crop assets to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        count = len(self._frames)
        with_label_assets_count = len(
            [frame for frame in self._frames if len(frame._crop_set.crop_assets) > 0]
        )
        if with_label_assets_count == 0:
            return

        frame_ids = np.empty((count), dtype=object)
        label_assets = np.empty((count), dtype=object)

        for i, frame in enumerate(self._frames):
            frame_ids[i] = frame.id
            label_assets[i] = [c for c in frame._crop_set.crop_assets]

        df = pd.DataFrame(
            {"frame_ids": pd.Series(frame_ids), "label_assets": pd.Series(label_assets)}
        )

        arrow_data = pa.Table.from_pandas(df)
        writer = pa.ipc.new_file(filelike, arrow_data.schema, use_legacy_format=False)
        writer.write(arrow_data)
        writer.close()

    def _write_batch_embeddings_to_file(self, filelike: IO[Any]) -> None:
        """Write the frame's embeddings to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        count = len([frame for frame in self._frames if frame.embedding is not None])

        if count == 0:
            return

        if count != len(self._frames):
            # walk through and backfill provided embeddings for derivative frames (no unique frame embeddings but also no crops to have triggered an earlier backfill)
            frame_embedding_dim = -1
            for frame in self._frames:
                if frame.embedding_dim > 0:
                    frame_embedding_dim = frame.embedding_dim
                    break
            for frame in self._frames:
                if not frame.embedding:
                    if not frame._is_derivative_frame:
                        raise Exception(
                            "If any frames have user provided embeddings, all frames must have embeddings."
                        )
                    fake_embedding = [0.0] * frame_embedding_dim
                    frame._add_embedding(fake_embedding)
                    count += 1

        frame_ids = np.empty((count), dtype=object)
        frame_embeddings = np.empty((count), dtype=object)
        crop_ids = np.empty((count), dtype=object)
        crop_embeddings = np.empty((count), dtype=object)

        for i, frame in enumerate(self._frames):
            frame_ids[i] = frame.id
            frame_embeddings[i] = frame.embedding
            crop_ids[i] = [x.id for x in frame._crop_set.crops]
            crop_embeddings[i] = [x.embedding for x in frame._crop_set.crops]

        df = pd.DataFrame(
            {
                "frame_ids": pd.Series(frame_ids),
                "frame_embeddings": pd.Series(frame_embeddings),
                "crop_ids": pd.Series(crop_ids),
                "crop_embeddings": pd.Series(crop_embeddings),
            }
        )

        arrow_data = pa.Table.from_pandas(df)
        writer = pa.ipc.new_file(filelike, arrow_data.schema, use_legacy_format=False)
        writer.write(arrow_data)
        writer.close()

    def _write_frames_to_file_streaming(self, filelike: IO[Any]) -> None:
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        for frame in self._frames:
            row = frame.to_dict()
            filelike.write(json.dumps(row) + "\n")

    def _write_crops_to_file_streaming(self, filelike: IO[Any]) -> None:
        """Write the frame content to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """
        for frame in self._frames:
            row = frame._crop_set.to_dict()
            filelike.write(json.dumps(row) + "\n")

    def _write_frame_embeddings_to_file_streaming(self, filelike: IO[Any]) -> None:
        """Write the frame's embeddings to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """

        count = len([frame for frame in self._frames if frame.embedding is not None])
        if count == 0:
            return

        frame_ids = np.empty((count), dtype=object)
        frame_embeddings = np.empty((count), dtype=object)

        for i, frame in enumerate(self._frames):
            if frame.embedding:
                frame_ids[i] = frame.id
                frame_embeddings[i] = frame.embedding
            elif frame.reuse_latest_embedding and self.frame_embedding_dim is not None:
                # for frames that are reusing embeddings, allow them to pass through client & server checks by writing dummy values; they will be dropped
                dummy_embeddings = [0.0] * self.frame_embedding_dim
                frame_ids[i] = frame.id
                frame_embeddings[i] = dummy_embeddings
            else:
                raise Exception(
                    "If any frames have user provided embeddings, all frames must have embeddings."
                )

        df = pd.DataFrame(
            {
                "frame_ids": pd.Series(frame_ids),
                "frame_embeddings": pd.Series(frame_embeddings),
            }
        )

        arrow_data = pa.Table.from_pandas(df)
        writer = pa.ipc.new_file(filelike, arrow_data.schema, use_legacy_format=False)
        writer.write(arrow_data)
        writer.close()

    def _write_crop_embeddings_to_file_streaming(self, filelike: IO[Any]) -> None:
        """Write the frame's crops' embeddings to a text filelike object (File handle, StringIO, etc.)

        Args:
            filelike (filelike): The destination file-like to write to.
        """

        count = len(
            [
                frame
                for frame in self._frames
                if frame.embedding is not None
                or frame._crop_set.crop_embedding_dim is not None
                and frame._crop_set.crop_embedding_dim > 0
            ]
        )

        if count == 0:
            return

        if count != len(self._frames):
            raise Exception(
                "If any frames have user provided embeddings, all frames must have embeddings."
            )

        # Get the first frame embedding dimension
        crop_ids = np.empty((count), dtype=object)
        crop_embeddings = np.empty((count), dtype=object)

        for i, frame in enumerate(self._frames):
            frame_crop_ids: List[str] = []
            frame_crop_embeddings: List[List[float]] = []
            # account for MODIFYs or label updates where some or all crops desire to reuse embeddings
            if (
                frame._crop_set.crop_embedding_dim is not None
                and frame._crop_set.crop_embedding_dim > 0
            ):
                for crop in frame._crop_set.crops:
                    if crop.embedding:
                        frame_crop_ids.append(crop.id)
                        frame_crop_embeddings.append(crop.embedding)
                    elif (
                        crop.reuse_latest_embedding
                        and frame._crop_set.crop_embedding_dim is not None
                    ):
                        dummy_label_emb = [0.0] * frame._crop_set.crop_embedding_dim
                        frame_crop_ids.append(crop.id)
                        frame_crop_embeddings.append(dummy_label_emb)
                    else:
                        raise Exception(
                            "If any crops have user provided embeddings, all crops must have embeddings."
                        )
            else:
                frame_crop_ids = []
                frame_crop_embeddings = []
            crop_ids[i] = frame_crop_ids
            crop_embeddings[i] = frame_crop_embeddings

        df = pd.DataFrame(
            {
                "crop_ids": pd.Series(crop_ids),
                "crop_embeddings": pd.Series(crop_embeddings),
            }
        )

        arrow_data = pa.Table.from_pandas(df)
        writer = pa.ipc.new_file(filelike, arrow_data.schema, use_legacy_format=False)
        writer.write(arrow_data)
        writer.close()


class _DatasetWithDeleteFrame(_Dataset):
    def delete_frame(self, frame_id: str) -> None:
        """Delete a frame from this dataset.

        Args:
            frame_id: A frame_id in the dataset.

        :meta public:
        """
        if frame_id in self._frame_ids_set:
            raise Exception("Attempted to add and delete the same frame id.")

        self._frames.append(DeletedFrame(frame_id=frame_id, dataset=self))
        self._frame_ids_set.add(frame_id)


class LabeledDataset(_DatasetWithDeleteFrame):
    """A collection of ground truth frames with which to create a new dataset or update an exisiting one in Aquarium

    Args:
        client: an instance of the Client that we can use to validate dataset & frames before upload
        name: the name of the dataset
        project_name: the name of the project this dataset belongs to
        frame_embedding_model: (optional) the model id that you used to generate the frame embeddings for this dataset
        label_embedding_model: (optional) the model id that you used to generate the label embeddings for this dataset
        external_metadata: (optional) A JSON object that can be used to attach metadata to the dataset itself
        is_anon_mode: (optional) flag to tell aquarium if url images are reachable from public internet or shared bucket. False if reachable, True if Not.
    """

    _reuses_embeddings: bool
    _allowed_frame_types = {ModifiedLabeledFrame, LabeledFrame}
    _split_frame_crop_files = True

    def __init__(
        self,
        client: "Client",
        name: str,
        project_name: str,
        frame_embedding_model: Optional[str] = None,
        label_embedding_model: Optional[str] = None,
        external_metadata: Optional[Dict[str, Any]] = None,
        is_anon_mode: bool = False,
        _streaming_version: int = 0,  # :meta hide-value:
    ):
        super().__init__(
            client,
            name,
            project_name,
            crop_embedding_model=label_embedding_model,
            frame_embedding_model=frame_embedding_model,
            external_metadata=external_metadata,
            is_anon_mode=is_anon_mode,
            pipeline_mode="STREAMING",
            streaming_version=_streaming_version,
        )
        self._reuses_embeddings = False

    def _flush_to_disk(self) -> None:
        # for modified frames, pull the latest existing windows
        modified_frames = [
            f for f in self._frames if isinstance(f, ModifiedLabeledFrame)
        ]
        chunked_modified_frames = [
            modified_frames[i * MAX_FRAMES_PER_BATCH : (i + 1) * MAX_FRAMES_PER_BATCH]
            for i in range(
                (len(modified_frames) + MAX_FRAMES_PER_BATCH - 1)
                // MAX_FRAMES_PER_BATCH
            )
        ]
        for chunk in chunked_modified_frames:
            frame_ids = [f.id for f in chunk]
            latest_frame_windows = self._dataset_client._get_latest_frame_windows(
                frame_ids
            )
            frame_to_latest_window = {
                frame_id: window_id for frame_id, window_id in latest_frame_windows
            }
            for frame in chunk:
                if frame.id not in frame_to_latest_window:
                    continue
                frame._previously_written_window = frame_to_latest_window[frame.id]
        super()._flush_to_disk()

    def create_and_add_labeled_frame(
        self,
        *,
        frame_id: str,
        sensor_data: List[SensorData],
        labels: List[Label],
        coordinate_frames: List[CoordinateFrame] = [],
        device_id: Optional[str] = None,
        date_captured: Optional[str] = None,
        geo_data: Optional[GeoData] = None,
        user_metadata: Optional[List[UserMetadataEntry]] = [],
        embedding: Optional[List[float]] = None,
    ) -> LabeledFrame:
        """Create a LabeledFrame with labels and add it to this dataset.

        Args:
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
        return LabeledFrame(
            dataset=self,
            frame_id=frame_id,
            sensor_data=sensor_data,
            labels=labels,
            coordinate_frames=coordinate_frames,
            device_id=device_id,
            date_captured=date_captured,
            geo_data=geo_data,
            user_metadata=user_metadata,
            embedding=embedding,
        )

    def create_and_add_modified_labeled_frame(
        self,
        *,
        frame_id: str,
        sensor_data: List[SensorData] = [],
        labels: List[Union[ModifiedLabel, Label]] = [],
        coordinate_frames: List[CoordinateFrame] = [],
        device_id: Optional[str] = None,
        date_captured: Optional[str] = None,
        geo_data: Optional[GeoData] = None,
        user_metadata: Optional[List[UserMetadataEntry]] = [],
        embedding: Optional[List[float]] = None,
    ) -> ModifiedLabeledFrame:
        """Create a ModifiedLabeledFrame with Labels and ModifiedLabels and add it to this dataset.

        Args:
            frame_id: A unique id for this frame.
            sensor_data: The list of sensor data to add to the frame.
            labels: The list of Labels and ModifiedLabel to add to the frame.
            coordinate_frames: (optional) The list of coordinate frames to add to the frame.
            device_id: (optional) The device that generated this frame. Defaults to None.
            date_captured: (optional) ISO formatted datetime string. Defaults to None.
            geo_data: (optional) A lat lon pair to assign to the pair
            user_metadata: (optional) A list of user-provided metadata
            embedding: (optional) A vector of floats of at least length 2.
        """
        modified_frame = ModifiedLabeledFrame(
            dataset=self,
            frame_id=frame_id,
            device_id=device_id,
            date_captured=date_captured,
            coordinate_frames=coordinate_frames,
            sensor_data=sensor_data,
            labels=labels,
            geo_data=geo_data,
            user_metadata=user_metadata,
            embedding=embedding,
        )
        if self._reuses_embeddings == False and modified_frame.reuse_latest_embedding:
            # only need one frame to be modified to set the flag
            self._reuses_embeddings = True
        return modified_frame


class InferenceSet(_Dataset):
    """A collection of inferences to be measured against an existing LabeledDataset

    Args:
        client: an instance of the Client that we can use to validate dataset & frames before upload
        name: the name of the inference set
        project_name: the name of the project this dataset belongs to
        base_dataset_name: the name of the labeled dataset these inferences should be associated with
        frame_embedding_model: (optional) the model id that you used to generate the frame embeddings for this dataset
        inference_embedding_model: (optional) the model id that you used to generate the inference embeddings for this dataset
        external_metadata: (optional) A JSON object that can be used to attach metadata to the dataset itself
        is_anon_mode: (optional) flag to tell aquarium if url images are reachable from public internet or shared bucket. False if reachable, True if Not.
    """

    _split_frame_crop_files = False
    _allowed_frame_types = {InferenceFrame}
    _split_frame_crop_files = False
    base_dataset_name: str

    def __init__(
        self,
        client: "Client",
        name: str,
        project_name: str,
        base_dataset_name: str,
        frame_embedding_model: Optional[str] = None,
        inference_embedding_model: Optional[str] = None,
        external_metadata: Optional[Dict[str, Any]] = None,
        is_anon_mode: bool = False,
        _streaming_version: int = 0,  # :meta hide-value:
    ):
        super().__init__(
            client,
            name,
            project_name,
            crop_embedding_model=inference_embedding_model,
            frame_embedding_model=frame_embedding_model,
            external_metadata=external_metadata,
            is_anon_mode=is_anon_mode,
            pipeline_mode="STREAMING",
            streaming_version=_streaming_version,
        )
        self.base_dataset_name = base_dataset_name

    def create_and_add_inference_frame(
        self,
        *,
        frame_id: str,
        inferences: List[Inference],
        user_metadata: Optional[List[UserMetadataEntry]] = None,
        custom_metrics: Optional[Dict[str, CustomMetricsEntry]] = None,
        embedding: Optional[List[float]] = None,
    ) -> InferenceFrame:
        """Create an InferenceFrame with inferences and add it to this inference set.

        Args:
            frame_id: A unique id for this frame.
            inferences: The list of Inferences to add to the frame.
            user_metadata: (optional) A list of user-provided metadata.
            custom_metrics: (optional) A dictionary of custom metrics to add to the frame.
            embedding: (optional) A vector of floats of at least length 2.
        """
        return InferenceFrame(
            inference_set=self,
            frame_id=frame_id,
            inferences=inferences,
            user_metadata=user_metadata,
            custom_metrics=custom_metrics,
            embedding=embedding,
        )


class UnlabeledDataset(_Dataset):
    """A collection of unlabeled frames

    Args:
        client: an instance of the Client that we can use to validate dataset & frames before upload
        name: the name of the dataset
        project_name: the name of the project this dataset belongs to
        frame_embedding_model: (optional) the model id that you used to generate the frame embeddings for this dataset
        proposal_embedding_model: (optional) the model id that you used to generate the proposal embeddings for this dataset
        external_metadata: (optional) A JSON object that can be used to attach metadata to the dataset itself
        is_anon_mode: (optional) flag to tell aquarium if url images are reachable from public internet or shared bucket. False if reachable, True if Not.
    """

    _split_frame_crop_files = True
    _allowed_frame_types = {UnlabeledFrame}
    _split_frame_crop_files = True

    def __init__(
        self,
        client: "Client",
        name: str,
        project_name: str,
        frame_embedding_model: Optional[str] = None,
        inference_embedding_model: Optional[str] = None,
        external_metadata: Optional[Dict[str, Any]] = None,
        is_anon_mode: bool = False,
        _streaming_version: int = 0,
    ):
        super().__init__(
            client,
            name,
            project_name,
            crop_embedding_model=inference_embedding_model,
            frame_embedding_model=frame_embedding_model,
            external_metadata=external_metadata,
            is_anon_mode=is_anon_mode,
            pipeline_mode="STREAMING",
            streaming_version=_streaming_version,
        )

    def create_and_add_unlabeled_frame(
        self,
        *,
        frame_id: str,
        sensor_data: List[SensorData],
        proposals: List[Inference],
        coordinate_frames: List[CoordinateFrame] = [],
        device_id: Optional[str] = None,
        date_captured: Optional[str] = None,
        geo_data: Optional[GeoData] = None,
        user_metadata: Optional[List[UserMetadataEntry]] = [],
        embedding: Optional[List[float]] = None,
    ) -> UnlabeledFrame:
        """Create an UnlabeledFrame with proposals and add it to this inference set.

        Args:
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
        return UnlabeledFrame(
            dataset=self,
            frame_id=frame_id,
            sensor_data=sensor_data,
            proposals=proposals,
            device_id=device_id,
            date_captured=date_captured,
            coordinate_frames=coordinate_frames,
            geo_data=geo_data,
            user_metadata=user_metadata,
            embedding=embedding,
        )


class UnlabeledDatasetV2(_Dataset):
    """A collection of unlabeled frames to upload via an experimental unlabeled dataset ingestion pipeline
    These versions of dataset and frame are still under development and may not support all task and label types.

    Args:
        client: an instance of the Client that we can use to validate dataset & frames before upload
        name: the name of the dataset
        project_name: the name of the project this dataset belongs to
        external_metadata: (optional) A JSON object that can be used to attach metadata to the dataset itself
    """

    _split_frame_crop_files = False
    _allowed_frame_types = {UnlabeledFrameV2}
    _split_frame_crop_files = False
    _file_summaries: List[Dict[str, str]]

    def __init__(
        self,
        client: "Client",
        name: str,
        project_name: str,
        external_metadata: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            client,
            name,
            project_name,
            external_metadata=external_metadata,
            pipeline_mode="BATCH",
            streaming_version=0,  # even though we ingest batch-wise, want to take advantage of the MAX_DATAPOINTS_PER_BATCH check
        )
        self._file_summaries = []

    def _flush_to_disk(self) -> None:
        frame_count = len(self._frames)
        crop_count = sum([f.crop_count() for f in self._frames])
        super()._flush_to_disk()
        self._file_summaries.append(
            {
                "frame_count": str(frame_count),
                "crop_count": str(crop_count),
                "partition_name": datetime.datetime.utcnow().strftime("%Y_%m"),
            }
        )

    def create_and_add_unlabeled_frame(
        self,
        *,
        frame_id: str,
        sensor_data: List[SensorData],
        proposals: List[Inference],
        coordinate_frames: List[CoordinateFrame] = [],
        device_id: Optional[str] = None,
        date_captured: Optional[str] = None,
        geo_data: Optional[GeoData] = None,
        user_metadata: Optional[List[UserMetadataEntry]] = [],
    ) -> UnlabeledFrameV2:
        """Create an UnlabeledFrameV2 with proposals and add it to this inference set.

        Args:
            frame_id: A unique id for this frame.
            sensor_data: The list of sensor data to add to the frame.
            proposals: The list of proposed labels with confidence (aka inferences) to add to the frame.
            coordinate_frames: (optional) The list of coordinate frames to add to the frame.
            device_id: (optional) The device that generated this frame. Defaults to None.
            date_captured: (optional) ISO formatted datetime string. Defaults to None.
            geo_data: (optional) A lat lon pair to assign to the pair
            user_metadata: (optional) A list of user-provided metadata
        """
        return UnlabeledFrameV2(
            dataset=self,
            frame_id=frame_id,
            sensor_data=sensor_data,
            proposals=proposals,
            coordinate_frames=coordinate_frames,
            device_id=device_id,
            date_captured=date_captured,
            geo_data=geo_data,
            user_metadata=user_metadata,
        )


Dataset = Union[LabeledDataset, InferenceSet, UnlabeledDataset, UnlabeledDatasetV2]
