import os
import datetime
import json
from importlib_metadata import version
import time
from uuid import uuid4
from io import BytesIO
from warnings import warn

from .viridis import viridis_rgb as viridis_rgb
from .turbo import turbo_rgb as turbo_rgb
from .segments import SegmentManager as SegmentManager
from .metrics_manager import MetricsManager as MetricsManager
from .work_queues import WorkQueueManager as WorkQueueManager
from typing import Any, Optional, Union, List, Dict, Tuple, Iterable, cast
from typing_extensions import TypedDict

from .util import (
    PrimaryTaskTypes,
    _upload_local_files,
    requests_retry,
    assert_valid_name,
    raise_resp_exception_error,
    maybe_parse_json_vals,
    split_user_attrs,
    USER_METADATA_SEQUENCE,
)

# All imports here necessary for referencing and compatiblity
from .class_map import (
    LabelClassMap as LabelClassMap,
    ClassMapEntry as ClassMapEntry,
    ClassMapUpdateEntry as ClassMapUpdateEntry,
    tableau_colors as tableau_colors,
    orig_label_color_list as orig_label_color_list,
)
from .coordinate_frames import _get_coordinate_frame_from_json
from .dataset_client import DatasetClient
from .datasets import (
    LabeledDataset,
    InferenceSet,
    UnlabeledDataset,
    UnlabeledDatasetV2,
)
from .frames import (
    GeoData,
    LabeledFrame,
    InferenceFrame,
    UserMetadataEntry,
)
from .labels import _get_single_label_from_json, _get_instance_seg_label_from_jsons
from .sensor_data import _get_sensor_data_from_json


class Client:
    """Client class that interacts with the Aquarium REST API.

    Args:
        api_endpoint (str, optional): The API endpoint to hit. Defaults to "https://illume.aquariumlearning.com/api/v1".
    """

    _creds_token: Optional[str]
    _creds_app_id: Optional[str]
    _creds_app_key: Optional[str]
    _creds_api_key: Optional[str]
    _dataset_clients: Dict[Tuple[str, str], DatasetClient]
    _client_version: str
    api_endpoint: str

    def __init__(
        self,
        *,
        api_endpoint: str = "https://illume.aquariumlearning.com/api/v1",
        **kwargs: Any,
    ) -> None:
        self._creds_token = None
        self._creds_app_id = None
        self._creds_app_key = None
        self._creds_api_key = None
        self._dataset_clients = {}
        self._client_version = version(__package__)
        self.api_endpoint = api_endpoint

    def _get_creds_headers(self) -> Dict[str, str]:
        """Get appropriate request headers for the currently set credentials.

        Raises:
            Exception: No credentials set.

        Returns:
            dict: Dictionary of headers
        """
        default_headers = {"x-illume-client-version": self._client_version}
        if self._creds_token:
            return {
                **default_headers,
                "Authorization": "Bearer {token}".format(token=self._creds_token),
            }
        elif self._creds_api_key:
            return {**default_headers, "x-illume-api-key": self._creds_api_key}
        elif self._creds_app_id and self._creds_app_key:
            return {
                **default_headers,
                "x-illume-app": self._creds_app_id,
                "x-illume-key": self._creds_app_key,
            }
        else:
            raise Exception("No credentials set.")

    def set_credentials(
        self,
        *,
        token: Optional[str] = None,
        app_id: Optional[str] = None,
        app_key: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        """Set credentials for the client.

        Args:
            api_key (str, optional): A string for a long lived API key. Defaults to None.
            token (str, optional): A JWT providing auth credentials. Defaults to None.
            app_id (str, optional): Application ID string. Defaults to None.
            app_key (str, optional): Application secret key. Defaults to None.

        Raises:
            Exception: Invalid credential combination provided.
        """
        if api_key is not None:
            self._creds_api_key = api_key
        elif token is not None:
            self._creds_token = token
        elif app_id is not None and app_key is not None:
            self._creds_app_id = app_id
            self._creds_app_key = app_key
        else:
            raise Exception(
                "Please provide either an api_key, token, or app_id and app_key"
            )

    def _format_error_logs(self, raw_error_logs: List[Dict[str, str]]) -> List[str]:
        """Format error log data into strings.

        Args:
            raw_error_logs (list[dict]): Error log data.

        Returns:
            list[str]: list of string formatted error messages.
        """
        formatted_lines = []
        for raw in raw_error_logs:
            formatted_lines.append(
                f"    {raw.get('aquarium_dataflow_step', '')}: {raw.get('msg', '')}"
            )
        return formatted_lines

    def get_segment_manager(self, project_name: str) -> SegmentManager:
        """Get a segment manager object.

        Args:
            project_name (str): Project ID to manage.

        Returns:
            SegmentManager: The segment manager object.
        """
        return SegmentManager(self, project_name)

    def get_metrics_manager(self, project_name: str) -> MetricsManager:
        """Get a metrics manager object.

        Args:
            project_name (str): Project ID to manage.

        Returns:
            MetricsManager: The metrics manager object.
        """
        return MetricsManager(self, project_name)

    def get_work_queue_manager(self, project_name: str) -> WorkQueueManager:
        """Get a work queue manager object.

        Args:
            project_name (str): Project ID to manage.

        Returns:
            WorkQueueManager: The work queue manager object.
        """
        return WorkQueueManager(self, project_name)

    def get_projects(self) -> List[Dict[str, Any]]:
        """Get info about existing projects

        Returns:
            list of dict: Project Info
        """
        r = requests_retry.get(
            self.api_endpoint + "/projects", headers=self._get_creds_headers()
        )

        raise_resp_exception_error(r)
        result: List[Dict[str, Any]] = r.json()
        return result

    def get_project(self, project_name: str) -> Dict[str, Any]:
        """Get detailed info about a specific project

        Returns:
            Dict[str, Any]: detailed info about a project
        """
        r = requests_retry.get(
            self.api_endpoint + "/projects/" + project_name,
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        result: Dict[str, Any] = r.json()
        return result

    def delete_project(self, project_name: str) -> None:
        """Mark a project for deletion

        Args:
            project_name (str): project_name
        """
        if not self.project_exists(project_name):
            raise Exception("Project {} does not exist.".format(project_name))

        url = self.api_endpoint + "/projects/{}".format(project_name)
        r = requests_retry.delete(url, headers=self._get_creds_headers())

        raise_resp_exception_error(r)

    def project_exists(self, project_name: str) -> bool:
        """Checks whether a project exists.

        Args:
            project_name (str): project_name

        Returns:
            bool: Does project exist
        """
        projects = self.get_projects()
        existing_project_names = [project["id"] for project in projects]
        return project_name in existing_project_names

    def create_project(
        self,
        project_name: str,
        label_class_map: LabelClassMap,
        primary_task: Optional[PrimaryTaskTypes] = PrimaryTaskTypes.Null,
        secondary_labels: Optional[Any] = None,
        frame_links: Optional[List[str]] = None,
        label_links: Optional[List[str]] = None,
        default_camera_target: Optional[List[float]] = None,
        default_camera_position: Optional[List[float]] = None,
        custom_metrics: Optional[
            Union["CustomMetricsDefinition", List["CustomMetricsDefinition"]]
        ] = None,
        max_shown_categories: Optional[int] = None,
        stratified_metrics: Optional[List["StratifiedMetricsDefinition"]] = None,
        include_no_gt: Optional[bool] = None,
        metrics_confidence_threshold: Optional[float] = None,
        metrics_iou_threshold: Optional[float] = None,
        external_metadata: Optional[Dict[str, Any]] = None,
        binary_classification_negative_class: Optional[str] = None,
    ) -> None:
        """Create a new project via the REST API.

        Args:
            project_name (str): project_name
            label_class_map (LabelClassMap): The label class map used to interpret classifications.
            primary_task: Any specific primary task for a non-object detection or classification task. Can be PrimaryTaskTypes.SemSeg or PrimaryTaskTypes.InstanceSegmentation or PrimaryTaskTypes.Classification or PrimaryTaskTypes.ClassificationWithGeometry or PrimaryTaskTypes.BinaryClassification or PrimaryTaskTypes.ObjectDetection or PrimaryTaskTypes.Null
            secondary_labels ([type], optional): List of secondary labels in classification tasks
            frame_links (Optional[List[str]], optional): List of string keys for links between frames
            label_links (Optional[List[str]], optional): List of string keys for links between labels
            default_camera_target (Optional[List[float]], optional): For 3D scenes, the default camera target
            default_camera_position (Optional[List[float]], optional): For 3D scenes, the default camera position
            custom_metrics (Optional[ Union[CustomMetricsDefinition, List[CustomMetricsDefinition]] ], optional): Defines which custom metrics exist for this project, defaults to None.
            max_shown_categories (Optional[int], optional): For categorical visualizations, set the maximum shown simultaneously. Max 100.
            stratified_metrics (Optional[List[StratifiedMetricsDefinition]], optional): Defines what object-level attributes to stratify metrics over.
            metrics_confidence_threshold (Optional[float], optional): In order to calculate metrics + confusion matrices, Aquarium uses this threshold (in combination with IOU) to match your ground truth (GT) labels with your inference labels. Defaults to 0.1 if not specified.
            metrics_iou_threshold(Optional[float], optional): In order to calculate metrics + confusion matrices, Aquarium uses this threshold (in combination with confidence) to match your ground truth (GT) labels with your inference labels. Defaults to 0.5 if not specified.
            external_metadata (Optional[Dict[str, Any]], optional): A JSON object that can be used to attach metadata to the project itself
            binary_classification_negative_class (Optional[str]): Required when primary_task is 'BINARY_CLASSIFICATION'. The name of the negative class.
        """

        assert_valid_name(project_name)

        if not isinstance(label_class_map, LabelClassMap):
            raise Exception("label_class_map must be a LabelClassMap")

        if not label_class_map.entries:
            raise Exception("label_class_map must have at least one class")

        dumped_classmap = [x.to_dict() for x in label_class_map.entries]
        payload = {"project_id": project_name, "label_class_map": dumped_classmap}

        if primary_task not in (None, PrimaryTaskTypes.Null):
            try:
                primary_task = PrimaryTaskTypes(primary_task)
            except ValueError:
                valid_tasks = [t._name_ for t in PrimaryTaskTypes]
                raise Exception(f"primary_task must be one of {valid_tasks}")

            payload["primary_task"] = primary_task.value
            if primary_task == PrimaryTaskTypes.BinaryClassification:
                if binary_classification_negative_class is None:
                    raise Exception(
                        "Must specify negative class for binary classification"
                    )
                if len(label_class_map.entries) != 2:
                    raise Exception(
                        "Binary classification tasks must have exactly two classes"
                    )
                if (
                    len(
                        [
                            x
                            for x in label_class_map.entries
                            if x.name == binary_classification_negative_class
                        ]
                    )
                    != 1
                ):
                    raise Exception("Negative class must be in classmap")
                payload[
                    "binary_classification_negative_class"
                ] = binary_classification_negative_class

        if secondary_labels is not None:
            dumped_secondary_labels = []
            for raw in secondary_labels:
                dumped_classmap = [x.to_dict() for x in raw["label_class_map"].entries]
                raw["label_class_map"] = dumped_classmap
                dumped_secondary_labels.append(raw)

            payload["secondary_labels"] = dumped_secondary_labels
        if frame_links is not None:
            if not isinstance(frame_links, list) or not all(
                isinstance(fl, str) for fl in frame_links
            ):
                raise Exception("frame_links must be a list of strings")
            payload["frame_links"] = frame_links
        if label_links is not None:
            if not isinstance(label_links, list) or not all(
                isinstance(ll, str) for ll in label_links
            ):
                raise Exception("label_links must be a list of strings")
            payload["label_links"] = label_links
        if default_camera_position is not None:
            if not isinstance(default_camera_position, list) or not all(
                isinstance(pos, float) for pos in default_camera_position
            ):
                raise Exception("default_camera_position must be a list of floats")
            payload["default_camera_position"] = default_camera_position
        if default_camera_target is not None:
            if not isinstance(default_camera_target, list) or not all(
                isinstance(tar, float) for tar in default_camera_target
            ):
                raise Exception("default_camera_target must be a list of floats")
            payload["default_camera_target"] = default_camera_target
        if custom_metrics is not None:
            if isinstance(custom_metrics, CustomMetricsDefinition):
                custom_metrics = [custom_metrics]

            if (
                not custom_metrics
                or (not isinstance(custom_metrics, list))
                or (not isinstance(custom_metrics[0], CustomMetricsDefinition))
            ):
                raise Exception(
                    "custom_metrics must be a CustomMetricsDefinition or list of CustomMetricsDefinition."
                )

            serializable_custom = [x.to_dict() for x in custom_metrics]
            payload["custom_metrics"] = serializable_custom

        if stratified_metrics is not None:
            if (
                not stratified_metrics
                or (not isinstance(stratified_metrics, list))
                or (not isinstance(stratified_metrics[0], StratifiedMetricsDefinition))
            ):
                raise Exception(
                    "stratified_metrics must be a list of StratifiedMetricsDefinition."
                )
            serializable_strat = [x.to_dict() for x in stratified_metrics]
            payload["stratified_metrics"] = serializable_strat

        if max_shown_categories is not None:
            if not isinstance(max_shown_categories, int):
                raise Exception("max_shown_categories must be an int")
            if max_shown_categories < 1 or max_shown_categories > 100:
                raise Exception("max_shown_categories must be between 1 and 100")
            payload["max_shown_categories"] = max_shown_categories

        if include_no_gt is not None:
            payload["include_no_gt"] = include_no_gt

        if metrics_confidence_threshold is not None:
            if not isinstance(metrics_confidence_threshold, float):
                raise Exception("metrics_confidence_threshold must be a float")
            payload["confidence_threshold"] = metrics_confidence_threshold

        if metrics_iou_threshold is not None:
            if not isinstance(metrics_iou_threshold, float):
                raise Exception("metrics_iou_threshold must be a float")
            payload["iou_threshold"] = metrics_iou_threshold

        if external_metadata is not None:
            if not isinstance(external_metadata, dict) or (
                external_metadata and not isinstance(next(iter(external_metadata)), str)
            ):
                raise Exception("external_metadata must be a dict with string keys")
            payload["external_metadata"] = external_metadata

        r = requests_retry.post(
            self.api_endpoint + "/projects",
            headers=self._get_creds_headers(),
            json=payload,
        )
        raise_resp_exception_error(r)

    def update_project_metadata(
        self, project_name: str, external_metadata: Dict[str, Any]
    ) -> None:
        """Update project metadata

        Args:
            project_name (str): The project id.
            external_metadata (Dict[Any, Any]): The new metadata
        """
        if not isinstance(external_metadata, dict) or (
            external_metadata and not isinstance(next(iter(external_metadata)), str)
        ):
            raise Exception("external_metadata must be a dict with string keys")

        payload = {"external_metadata": external_metadata}
        r = requests_retry.post(
            f"{self.api_endpoint}/projects/{project_name}/metadata",
            headers=self._get_creds_headers(),
            json=payload,
        )
        raise_resp_exception_error(r)

    def update_label_class_map_colors(
        self, project_name: str, changed_label_classes: List[ClassMapUpdateEntry]
    ) -> None:
        """Updates label class colors of a specific project

        Args:
            project_name (str): The project id.
            changed_label_classes (List[ClassMapUpdateEntry]): The list of label classes with changed colors. Must be a subset of the project's overall label class map
        """
        project = self.get_project(project_name)
        label_class_map_dict_by_id = {
            label_class["id"]: label_class for label_class in project["label_class_map"]
        }
        label_class_map_dict_by_name = {
            label_class["name"]: label_class
            for label_class in project["label_class_map"]
        }

        seen_ids = set()
        dumped_changes = []
        for entry in changed_label_classes:
            if not entry.class_id:
                known_label_class = label_class_map_dict_by_name.get(entry.name)
                if not known_label_class:
                    raise Exception(
                        f"Label class with name {entry.name} could not be found in the project's label class map. "
                        "This method only allows changing an existing label class map. "
                        "To append new label classes please use create_project."
                    )
                entry.class_id = known_label_class["id"]

            known_label_class = label_class_map_dict_by_id.get(entry.class_id)

            if not known_label_class:
                raise Exception(
                    f"Label class with id {entry.class_id} could not be found in the project's label class map. "
                    "This method only allows changing an existing label class map. "
                    "To append new label classes please use create_project."
                )

            if entry.class_id in seen_ids:
                raise Exception(
                    f"Label class with id {entry.class_id} ({known_label_class['name']}) has multiple change entries. "
                    "Please consolidate into one change."
                )

            seen_ids.add(entry.class_id)
            dumped_entry = entry.to_dict()

            # lazy shallow None check to avoid overwriting with a null
            dumped_patch_entry = {
                k: v for k, v in dumped_entry.items() if v is not None
            }

            dumped_changes.append(dumped_patch_entry)

        payload = {"label_class_map": dumped_changes}
        r = requests_retry.patch(
            f"{self.api_endpoint}/projects/{project_name}/label_class_map",
            headers=self._get_creds_headers(),
            json=payload,
        )
        raise_resp_exception_error(r)

    def get_datasets(
        self, project_name: str, include_archived: Optional[bool]
    ) -> List[Dict[str, Any]]:
        """Get existing datasets for a project.

        Args:
            project_name (str): The project id.

        Returns:
            list: A list of dataset info for the project.
        """
        datasets_api_root = self.api_endpoint + "/projects/{}/datasets".format(
            project_name
        )
        params = {"include_archived": include_archived} if include_archived else {}
        r = requests_retry.get(
            datasets_api_root, headers=self._get_creds_headers(), params=params
        )
        raise_resp_exception_error(r)
        result: List[Dict[str, Any]] = r.json()
        return result

    def get_dataset(self, project_name: str, dataset_name: str) -> Dict[str, Any]:
        """Get existing dataset for a project.

        Args:
            project_name (str): The project id.
            dataset_name (str): dataset_name

        Returns:
            dict: The dataset info.
        """
        url = self.api_endpoint + "/projects/{}/datasets/{}".format(
            project_name, dataset_name
        )
        r = requests_retry.get(url, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        result: Dict[str, Any] = r.json()
        return result

    def delete_dataset(self, project_name: str, dataset_name: str) -> None:
        """Mark a dataset for deletion

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name
        """
        if not self.dataset_exists(project_name, dataset_name):
            raise Exception("Dataset {} does not exist.".format(dataset_name))

        url = self.api_endpoint + "/projects/{}/datasets/{}".format(
            project_name, dataset_name
        )
        r = requests_retry.delete(url, headers=self._get_creds_headers())

        raise_resp_exception_error(r)

    def dataset_exists(self, project_name: str, dataset_name: str) -> bool:
        """Check if a dataset exists. This includes datasets that have been archived.

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name

        Returns:
            bool: Whether the dataset already exists.
        """
        datasets = self.get_datasets(project_name, include_archived=True)
        existing_dataset_names = [dataset.get("id") for dataset in datasets]
        return dataset_name in existing_dataset_names

    def is_dataset_processed(self, project_name: str, dataset_name: str) -> bool:
        """Check if a dataset is fully processed.

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name

        Returns:
            bool: If the dataset is done processing.
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/is_processed".format(project_name, dataset_name)
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed: Dict[str, bool] = r.json()
        return parsed["processed"]

    def is_dataset_archived(self, project_name: str, dataset_name: str) -> bool:
        """Check if a dataset has been archived.

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name

        Returns:
            bool: If the dataset is archived. Returns False if dataset does not exist
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/is_archived".format(project_name, dataset_name)
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed: Dict[str, bool] = r.json()
        return parsed["archived"]

    def get_dataset_ingest_error_logs(
        self, project_name: str, dataset_name: str
    ) -> List[Dict[str, Any]]:
        """Get ingest error log entries for a dataset.

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name

        Returns:
            list[dict]: List of error entries
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/ingest_error_logs".format(
                project_name, dataset_name
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed: List[Dict[str, Any]] = r.json()
        return parsed

    def current_dataset_process_state(
        self, project_name: str, dataset_name: str
    ) -> Tuple[str, float]:
        """Current processing state of a dataset.

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name

        Returns:
            Tuple[str, float]: semantic name of state of processing, percent done of job
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/process_state".format(
                project_name, dataset_name
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed["current_state"], parsed["percent_done"]

    def current_abstract_dataset_process_step_status(
        self, project_name: str, dataset_name: str
    ) -> Dict[str, Any]:
        """Returns the process steps statuses for a given dataset or inferenceset

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name

        Returns:
            Dict[str, Any]: A set of process step statuses that exist for a given abstract dataset
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/process_step_status".format(
                project_name, dataset_name
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed: Dict[str, Any] = r.json()
        return parsed

    @staticmethod
    def parse_normalize_process_step_status(
        process_step_status_payload: Dict[str, Any]
    ) -> str:
        result: str = process_step_status_payload["process_step_statuses"]["normalize"][
            "status"
        ]
        return result

    def inferences_exists(
        self, project_name: str, dataset_name: str, inferences_name: str
    ) -> bool:
        """Check if a set of inferences exists.

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name
            inferences_name (str): inferences_name

        Returns:
            bool: Whether the inferences id already exists.
        """
        # TODO: FIXME: We need a first class model for inferences,
        # not just name gluing
        inferences_dataset_name = "_".join(
            ["inferences", dataset_name, inferences_name]
        )
        datasets = self.get_datasets(project_name, include_archived=True)
        existing_dataset_names = [dataset.get("id") for dataset in datasets]
        return inferences_dataset_name in existing_dataset_names

    def is_inferences_processed(
        self, project_name: str, dataset_name: str, inferences_name: str
    ) -> bool:
        """Check if a set of inferences is fully processed.

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name
            inferences_name(str): inferences_name

        Returns:
            bool: If the inference set is done processing.
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences/{}/is_processed".format(
                project_name, dataset_name, inferences_name
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        processed: bool = parsed["processed"]
        return processed

    def get_inferences_ingest_error_logs(
        self, project_name: str, dataset_name: str, inferences_name: str
    ) -> List[Dict[str, Any]]:
        """Get ingest error log entries for an inference set.

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name
            inferences_name(str): inferences_name

        Returns:
            list[dict]: List of error entries
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences/{}/ingest_error_logs".format(
                project_name, dataset_name, inferences_name
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed: List[Dict[str, Any]] = r.json()
        return parsed

    def current_inferences_process_state(
        self, project_name: str, dataset_name: str, inferences_name: str
    ) -> Tuple[str, float]:
        """current processing state of inferences.

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name
            inferences_name(str): inferences_name

        Returns:
            Tuple[str, float]: semantic name of state of processing, percent done of job
        """
        endpoint_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences/{}/process_state".format(
                project_name, dataset_name, inferences_name
            )
        )

        r = requests_retry.get(endpoint_path, headers=self._get_creds_headers())
        raise_resp_exception_error(r)
        parsed = r.json()
        return parsed["current_state"], parsed["percent_done"]

    def upload_asset_from_filepath(
        self, project_name: str, dataset_name: str, filepath: str
    ) -> str:
        """Upload an asset from a local file path.
        This is useful in cases where you have data on your local machine that you want to mirror in aquarium.

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name
            filepath (str): The filepath to grab the assset data from

        Returns:
            str: The URL to the mirrored asset.
        """

        get_upload_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/get_upload_url".format(
                project_name, dataset_name
            )
        )

        upload_filename = os.path.basename(filepath)
        upload_filename = "{}_{}".format(str(uuid4()), upload_filename)

        params = {"upload_filename": upload_filename}
        upload_url_resp = requests_retry.get(
            get_upload_path, headers=self._get_creds_headers(), params=params
        )

        raise_resp_exception_error(upload_url_resp)
        urls = upload_url_resp.json()
        put_url = urls["put_url"]
        download_url: str = urls["download_url"]

        with open(filepath, "rb") as f:
            upload_resp = requests_retry.put(put_url, data=f)

        raise_resp_exception_error(upload_resp)
        return download_url

    def upload_asset_from_url(
        self, project_name: str, dataset_name: str, source_url: str
    ) -> str:
        """Upload an asset from a private url.
        This is useful in cases where you have data easily accessible on your network that you want to mirror in aquarium.

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name
            source_url (str): The source url to grab the assset data from

        Returns:
            str: The URL to the mirrored asset.
        """
        get_upload_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/get_upload_url".format(
                project_name, dataset_name
            )
        )

        upload_filename = os.path.basename(source_url)
        upload_filename = "{}_{}".format(str(uuid4()), upload_filename)

        params = {"upload_filename": upload_filename}
        upload_url_resp = requests_retry.get(
            get_upload_path, headers=self._get_creds_headers(), params=params
        )

        raise_resp_exception_error(upload_url_resp)
        urls = upload_url_resp.json()
        put_url = urls["put_url"]
        download_url: str = urls["download_url"]

        dl_resp = requests_retry.get(source_url)
        payload = BytesIO(dl_resp.content)

        upload_resp = requests_retry.put(put_url, data=payload)

        raise_resp_exception_error(upload_resp)
        return download_url

    def _upload_rows_from_files(
        self,
        project_name: str,
        dataset_name: str,
        upload_prefix: str,
        upload_suffix: str,
        file_names: List[str],
        delete_after_upload: bool = True,
        bucket: str = "aquarium-dev",
        file_metadata: Optional[List[Dict[str, str]]] = None,
    ) -> List[str]:
        # Get upload / download URLs
        get_upload_path = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/get_upload_url".format(
                project_name, dataset_name
            )
        )

        download_urls = _upload_local_files(
            file_names,
            get_upload_path,
            self._get_creds_headers(),
            upload_prefix,
            upload_suffix,
            bucket=bucket,
            delete_after_upload=delete_after_upload,
            file_metadata=file_metadata,
            client_version=self._client_version,
        )

        return download_urls

    def _preview_frame_dict(
        self,
        project_name: str,
        both_frames_dict: Dict[str, Optional[Dict[str, Any]]],
        selected_label: Optional[str] = None,
    ) -> None:
        """Generate preview with both dataset frame and inference frame as dict

        Args:
            project_name (str): name of project to preview frame with
            both_frames_dict (dict): Dictionary containing the labeled and inference frame

        :meta private:
        """
        api_path = "/projects/{}/preview_frame".format(project_name)

        preview_frame_api_root = self.api_endpoint + api_path

        r = requests_retry.post(
            preview_frame_api_root,
            headers=self._get_creds_headers(),
            json=both_frames_dict,
        )
        response_data = r.json()
        if response_data.get("preview_frame_uuid"):
            print("Please visit the following url to preview your frame in the webapp")
            url = (
                self.api_endpoint[:-7]
                + api_path
                + "/"
                + response_data["preview_frame_uuid"]
            )
            if selected_label is not None:
                url += f"?selectedLabel={selected_label}"
            print(f"{url}\n")
        else:
            raise Exception(
                "Preview URL could not be constructed by server. "
                "Please make sure you're logged in and check frame data accordingly."
            )

    def preview_frame(
        self,
        project_name: str,
        labeled_frame: LabeledFrame,
        inference_frame: Optional[InferenceFrame] = None,
    ) -> None:
        """prints out a URL that lets you preview a provided frame in the web browser
        Useful for debugging data and image url issues.

        Args:
            project_name (str): Name of project to be associated for this frame preview (for label class association)
            labeled_frame (LabeledFrame): Labeled Frame desired for preview in web-app
            inference_frame (Optional[InferenceFrame], optional): Labeled Inference Desired for preview in web-app. Defaults to None.
        """

        both_frames: Dict[str, Optional[Dict[str, Any]]] = {}
        labeled_frame_dict = labeled_frame.to_dict()
        labeled_frame_dict["label_data"] = labeled_frame._crop_set.to_dict()[
            "label_data"
        ]
        both_frames["labeled_frame"] = labeled_frame_dict
        both_frames["inference_frame"] = (
            inference_frame.to_dict() if inference_frame else None
        )
        self._preview_frame_dict(project_name, both_frames)

    def initialize_labeled_dataset(
        self,
        dataset_name: str,
        project_name: str,
        frame_embedding_model: Optional[str] = None,
        label_embedding_model: Optional[str] = None,
        external_metadata: Optional[Dict[str, Any]] = None,
        is_anon_mode: bool = False,
    ) -> LabeledDataset:
        """Initializes a LabeledDataset to add LabeledFrames and ModifiedLabeledFrames to.
        Commit changes by calling :func:`create_or_update_labeled_dataset <create_or_update_labeled_dataset>`

        Args:
            dataset_name: The dataset_name.
            project_name: The project_name.
            frame_embedding_model: (optional) The name of the embedding model you used to generate frame embeddings, if you're providing custom embeddings
            label_embedding_model: (optional) The name of the embedding model you used to generate label embeddings, if you're providing custom embeddings
            external_metadata: (optional) A JSON object that can be used to attach metadata to the dataset itself
            is_anon_mode: (optional) flag to tell aquarium if url images are reachable from public internet or shared bucket. False if reachable, True if Not.
        """
        return LabeledDataset(
            self,
            name=dataset_name,
            project_name=project_name,
            frame_embedding_model=frame_embedding_model,
            label_embedding_model=label_embedding_model,
            external_metadata=external_metadata,
            is_anon_mode=is_anon_mode,
        )

    def initialize_inference_set(
        self,
        inference_set_name: str,
        project_name: str,
        base_dataset_name: str,
        frame_embedding_model: Optional[str] = None,
        inference_embedding_model: Optional[str] = None,
        external_metadata: Optional[Dict[str, Any]] = None,
        is_anon_mode: bool = False,
    ) -> InferenceSet:
        """Initializes an InferenceSet to add InferenceFrames to.
                Commit changes by calling :func:`create_or_update_inference_set <create_or_update_inference_set>`

                Args:
                    inference_set_name (str): A unique identifier for this set of inferences.
                    project_name (str): The project_name.
                    base_dataset_name (str): The name of the labeled dataset that these inferences are based on.
                    frame_embedding_model: (optional) The name of the embedding model you used to generate frame embeddings, if you're providing custom embeddings
                    inference_embedding_model: (optional) The name of the embedding model you used to generate label embeddings, if you're providing custom embeddings
        =            external_metadata: (optional) A JSON object that can be used to attach metadata to the dataset itself
                    is_anon_mode: (optional) flag to tell aquarium if url images are reachable from public internet or shared bucket. False if reachable, True if Not.
        """
        return InferenceSet(
            self,
            name=inference_set_name,
            project_name=project_name,
            base_dataset_name=base_dataset_name,
            frame_embedding_model=frame_embedding_model,
            inference_embedding_model=inference_embedding_model,
            external_metadata=external_metadata,
            is_anon_mode=is_anon_mode,
        )

    def initialize_unlabeled_dataset(
        self,
        unlabeled_dataset_name: str,
        project_name: str,
        frame_embedding_model: Optional[str] = None,
        inference_embedding_model: Optional[str] = None,
        external_metadata: Optional[Dict[str, Any]] = None,
        is_anon_mode: bool = False,
    ) -> UnlabeledDataset:
        """Initializes an UnlabeledDataset to add UnlabeledFrames to.
        Commit changes by calling :func:`create_or_update_unlabeled_dataset <create_or_update_unlabeled_dataset>`

        Args:
            unlabeled_dataset_name: The unlabeled_dataset_name.
            project_name: The project_name.
            frame_embedding_model: (optional) The name of the embedding model you used to generate frame embeddings, if you're providing custom embeddings
            inference_embedding_model: (optional) The name of the embedding model you used to generate label embeddings, if you're providing custom embeddings
            external_metadata: (optional) A JSON object that can be used to attach metadata to the dataset itself
            is_anon_mode: (optional) flag to tell aquarium if url images are reachable from public internet or shared bucket. False if reachable, True if Not.
        """
        return UnlabeledDataset(
            self,
            name=unlabeled_dataset_name,
            project_name=project_name,
            frame_embedding_model=frame_embedding_model,
            inference_embedding_model=inference_embedding_model,
            external_metadata=external_metadata,
            is_anon_mode=is_anon_mode,
        )

    def initialize_unlabeled_datasetV2(
        self,
        unlabeled_dataset_name: str,
        project_name: str,
        external_metadata: Optional[Dict[str, Any]] = None,
    ) -> UnlabeledDatasetV2:
        """.. experimental::

        Initializes an UnlabeledDatasetV2 to add UnlabeledFrameV2s to.
        Commit changes by calling :func:`create_or_update_unlabeled_datasetV2 <create_or_update_unlabeled_datasetV2>`

        Args:
            unlabeled_dataset_names: The dataset_name.
            project_name: The project_name.
            external_metadata: (optional) A JSON object that can be used to attach metadata to the dataset itself.
        """
        return UnlabeledDatasetV2(
            self,
            name=unlabeled_dataset_name,
            project_name=project_name,
            external_metadata=external_metadata,
        )

    def _validate_base_streaming_dataset(
        self,
        project_name: str,
        dataset: Union[LabeledDataset, InferenceSet, UnlabeledDataset],
        wait_until_finish: bool = False,
        wait_timeout: datetime.timedelta = datetime.timedelta(hours=2),
        preview_first_frame: bool = False,
    ) -> bool:
        assert_valid_name(dataset.id)

        if wait_until_finish and not isinstance(wait_timeout, datetime.timedelta):
            raise Exception("wait_timeout must be a datetime.timedelta object")

        if self.is_dataset_archived(project_name, dataset.id):
            raise Exception("Cannot upload streaming frames to archived dataset")

        if len(dataset._frame_ids_set) == 0:
            raise Exception("Dataset contains no frames and cannot be empty.")

        if (
            len(dataset._temp_frame_file_names_streaming) == 0
            and len(dataset._temp_frame_file_names) == 0
        ):
            raise Exception("Cannot add 0 frames to dataset")

        if preview_first_frame and dataset.first_frame:
            project_name = dataset.project_name
            first_frame_dict = dataset.first_frame.to_dict()
            first_frame_dict["label_data"] = dataset.first_frame._crop_set.to_dict()[
                "label_data"
            ]
            self._preview_frame_dict(
                project_name,
                {"labeled_frame": first_frame_dict, "inference_frame": None},
            )
            user_response = input(
                "Please vist above URL to see your Preview frame.\n\n"
                "Press ENTER to continue or type `exit` and press ENTER "
                "to cancel dataset upload.\n"
            )
            if user_response == "exit":
                print("Canceling dataset upload!")
                return False

        return True

    def _wait_until_finish(
        self,
        timeout: datetime.timedelta,
        project_name: str,
        dataset_name: str,
        upload_version: str,
        entity_name: str,
    ) -> None:
        # Wait for windows to finish on the dataset
        print(f"Waiting for {entity_name.lower()} to finish processing...")
        all_upload_version_windows_done = False
        start_time = datetime.datetime.now()
        dataset_upload_version_windows = []
        while not all_upload_version_windows_done:
            r = requests_retry.get(
                self.api_endpoint
                + "/streaming/projects/{}/datasets/{}/upload_version/{}/windows".format(
                    project_name,
                    dataset_name,
                    upload_version,
                ),
                headers=self._get_creds_headers(),
            )
            if r.ok:
                dataset_upload_version_windows = r.json()
                all_upload_version_windows_done = len(
                    dataset_upload_version_windows
                ) > 0 and all(
                    window.get("status") == "DONE"
                    or window.get("status") == "WINDOW_ERRORED"
                    or window.get("status") == "AGG_ERRORED"
                    for window in dataset_upload_version_windows
                )
            if datetime.datetime.now() - start_time >= timeout:
                print(
                    f"Waited over {str(timeout)} for {entity_name.lower()} to finish. Exiting now; check the project uploads page for more details around upload progress."
                )
                return
            time.sleep(10)
        errored_window_uuids = [
            window.get("uuid")
            for window in dataset_upload_version_windows
            if (
                (window.get("status") == "WINDOW_ERRORED")
                or (window.get("status") == "AGG_ERRORED")
            )
        ]
        if len(errored_window_uuids) > 0:
            print(
                "{} processing has {}failed.".format(
                    entity_name.capitalize(),
                    "partially "
                    if len(errored_window_uuids) < len(dataset_upload_version_windows)
                    else "",
                )
            )
            print(
                "Check project uploads to see more details and which frames need reuploading."
            )
            print(
                "Failed Upload IDs: {}".format(
                    ", ".join(str(x) for x in errored_window_uuids)
                )
            )
            print(
                "{}/projects/{}/details?tab=streaming_uploads".format(
                    self.api_endpoint[:-7], project_name
                )
            )
        else:
            print(f"{entity_name.capitalize()} is fully processed.")

    def create_or_update_labeled_dataset(
        self,
        dataset: LabeledDataset,
        wait_until_finish: bool = False,
        wait_timeout: datetime.timedelta = datetime.timedelta(hours=2),
        preview_first_frame: bool = False,
        delete_cache_files_after_upload: bool = True,
    ) -> None:
        """Create or update a labeled dataset with the provided frames and labels.

        Args:
            dataset: The LabeledDataset to upload.
            wait_until_finish: (optional) Block until the dataset processing job finishes. This generally takes at least 5 minutes, and scales with the size of the dataset. Defaults to False.
            wait_timeout: (optional) Maximum time to wait for. Defaults to 2 hours.
            preview_first_frame: (optional) preview the first frame of the dataset in the webapp before continuing. Requires interaction.
            delete_cache_files_after_upload: (optional)flag to turn off automatic deletion of cache files after upload. Useful for ipython notebook users that reload/re-attempt uploads. Defaults to True.
        """
        if not isinstance(dataset, LabeledDataset):
            raise Exception(
                f"Cannot upload a {dataset.__class__.__name__} using create_or_update_labeled_dataset. Please use the correct corresponding create_or_update client method."
            )

        assert_valid_name(dataset.id)
        project_name = dataset.project_name
        dataset._flush_to_disk()
        if not self._validate_base_streaming_dataset(
            project_name, dataset, wait_until_finish, wait_timeout, preview_first_frame
        ):
            return

        upload_version = str(uuid4())

        print("Uploading Dataset...")
        uuid_prefix = str(uuid4())
        upload_prefix_frame = "{}_frame_data".format(uuid_prefix)
        upload_prefix_crop = "{}_crop_data".format(uuid_prefix)
        upload_suffix = ".jsonl"

        frame_urls = self._upload_rows_from_files(
            project_name,
            dataset.id,
            upload_prefix_frame,
            upload_suffix,
            dataset._temp_frame_file_names_streaming,
            delete_after_upload=delete_cache_files_after_upload,
        )
        crop_urls = self._upload_rows_from_files(
            project_name,
            dataset.id,
            upload_prefix_crop,
            upload_suffix,
            dataset._temp_crop_file_names_streaming,
            delete_after_upload=delete_cache_files_after_upload,
        )
        final_urls = {
            "frame": frame_urls,
            "crop": crop_urls,
            "frame_url_counts": dataset._temp_frame_count_per_file_streaming,
            "crop_url_counts": dataset._temp_crop_count_per_file_streaming,
        }

        if dataset._temp_frame_embeddings_file_names_streaming:
            print("Uploading Dataset Embeddings...")
            upload_frame_prefix = "{}_frame_embeddings".format(str(uuid4()))
            upload_crop_prefix = "{}_crop_embeddings".format(str(uuid4()))
            upload_suffix = ".arrow"
            uploaded_frame_urls = self._upload_rows_from_files(
                project_name,
                dataset.id,
                upload_frame_prefix,
                upload_suffix,
                dataset._temp_frame_embeddings_file_names_streaming,
                delete_after_upload=delete_cache_files_after_upload,
            )
            uploaded_crop_urls = self._upload_rows_from_files(
                project_name,
                dataset.id,
                upload_crop_prefix,
                upload_suffix,
                dataset._temp_crop_embeddings_file_names_streaming,
                delete_after_upload=delete_cache_files_after_upload,
            )
            if uploaded_frame_urls:  # not empty list
                final_urls["frame_embeddings"] = uploaded_frame_urls
            if uploaded_crop_urls:  # not empty list
                final_urls["crop_embeddings"] = uploaded_crop_urls

        if dataset._temp_frame_asset_file_names:
            print("Uploading Labeled Frame Assets...")
            upload_prefix = "{}_assets".format(str(uuid4()))
            upload_suffix = ".arrow"
            uploaded_urls = self._upload_rows_from_files(
                project_name,
                dataset.id,
                upload_prefix,
                upload_suffix,
                dataset._temp_frame_asset_file_names,
                delete_after_upload=delete_cache_files_after_upload,
            )
            if uploaded_urls:  # not empty list
                final_urls["frame_asset_url"] = uploaded_urls

        datasets_api_root = self.api_endpoint + "/projects/{}/datasets".format(
            project_name
        )
        payload = {
            "dataset_id": dataset.id,
            "data_url": final_urls,
            "embedding_distance_metric": dataset.embedding_distance_metric,
            "embedding_upload_version": 1,
            "upload_version": upload_version,
            "pipeline_mode": "STREAMING",
            "is_anon_mode": dataset.is_anon_mode,
            "is_unlabeled_indexed_dataset": False,
            "frame_model_version": dataset.frame_embedding_model,
            "crop_model_version": dataset.crop_embedding_model,
            "frame_embedding_dim": dataset.frame_embedding_dim,
            "crop_embedding_dim": dataset.crop_embedding_dim,
            "sample_frame_embeddings": dataset.sample_frame_embeddings,
            "sample_crop_embeddings": dataset.sample_crop_embeddings,
            "total_num_frames": len(dataset._frame_ids_set),
            "total_num_crops": len(dataset._crop_ids_set),
            "streaming_version": dataset._streaming_version,
            "reuse_embeddings": dataset._reuses_embeddings,
        }

        if dataset.external_metadata is not None:
            payload["external_metadata"] = dataset.external_metadata

        dataset._cleanup_temp_dir()

        print("Dataset Processing Initiating...")
        r = requests_retry.post(
            datasets_api_root, headers=self._get_creds_headers(), json=payload
        )
        raise_resp_exception_error(r)
        print("Dataset Processing Initiated Successfully")

        if wait_until_finish:
            self._wait_until_finish(
                wait_timeout,
                project_name,
                dataset.id,
                upload_version,
                "labeled dataset",
            )

    def create_or_update_inference_set(
        self,
        inference_set: InferenceSet,
        wait_until_finish: bool = False,
        wait_timeout: datetime.timedelta = datetime.timedelta(hours=2),
        delete_cache_files_after_upload: bool = True,
    ) -> None:
        """Create or update an inference set.

        Args:
            inference_set: the InferenceSet to upload.
            wait_until_finish: (optional) Block until the dataset processing job finishes. This generally takes at least 5 minutes, and scales with the size of the dataset. Defaults to False.
            wait_timeout: (optional) Maximum time to wait for. Defaults to 2 hours.
            delete_cache_files_after_upload: (optional)flag to turn off automatic deletion of cache files after upload. Useful for ipython notebook users that reload/re-attempt uploads. Defaults to True.
        """
        if not isinstance(inference_set, InferenceSet):
            raise Exception(
                f"Cannot upload a {inference_set.__class__.__name__} using create_or_update_inference_set. Please use the correct corresponding create_or_update client method."
            )

        assert_valid_name(inference_set.id)
        project_name = inference_set._dataset_client.project_name
        inference_set._flush_to_disk()
        if not self._validate_base_streaming_dataset(
            project_name,
            inference_set,
            wait_until_finish,
            wait_timeout,
            preview_first_frame=False,
        ):
            return

        queue_after_dataset = not self.is_dataset_processed(
            project_name, inference_set.base_dataset_name
        )
        upload_version = str(uuid4())
        inferences_api_root = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/inferences".format(
                project_name, inference_set.base_dataset_name
            )
        )

        print("Uploading Inferences...")

        upload_prefix = "{}_data".format(str(uuid4()))
        upload_suffix = ".jsonl"
        final_urls = self._upload_rows_from_files(
            project_name,
            inference_set.base_dataset_name,
            upload_prefix,
            upload_suffix,
            inference_set._temp_frame_file_names,
            delete_after_upload=delete_cache_files_after_upload,
        )

        payload = {
            "inferences_id": inference_set.id,
            "data_url": final_urls,
            "embedding_distance_metric": inference_set.embedding_distance_metric,
            "embedding_upload_version": 1,
            "queue_after_dataset": queue_after_dataset,
            "upload_version": upload_version,
            "pipeline_mode": "STREAMING",
            "frame_embedding_dim": inference_set.frame_embedding_dim,
            "crop_embedding_dim": inference_set.crop_embedding_dim,
            "total_num_frames": len(inference_set._frame_ids_set),
            "total_num_crops": len(inference_set._crop_ids_set),
            "streaming_version": inference_set._streaming_version,
            "frame_model_version": inference_set.frame_embedding_model,
            "crop_model_version": inference_set.crop_embedding_model,
        }

        if inference_set.external_metadata is not None:
            payload["external_metadata"] = inference_set.external_metadata

        if inference_set._temp_frame_embeddings_file_names:
            print("Uploading Inference Embeddings...")
            upload_prefix = "{}_embeddings".format(str(uuid4()))
            upload_suffix = ".arrow"
            uploaded_urls = self._upload_rows_from_files(
                project_name,
                inference_set.base_dataset_name,
                upload_prefix,
                upload_suffix,
                inference_set._temp_frame_embeddings_file_names,
                delete_after_upload=delete_cache_files_after_upload,
            )
            if uploaded_urls:  # not empty list
                payload["embeddings_url"] = uploaded_urls

        if inference_set._temp_frame_asset_file_names:
            print("Uploading Inference Assets...")
            upload_prefix = "{}_assets".format(str(uuid4()))
            upload_suffix = ".arrow"
            uploaded_urls = self._upload_rows_from_files(
                project_name,
                inference_set.base_dataset_name,
                upload_prefix,
                upload_suffix,
                inference_set._temp_frame_asset_file_names,
                delete_after_upload=delete_cache_files_after_upload,
            )
            if uploaded_urls:  # not empty list
                payload["frame_asset_url"] = uploaded_urls

        payload["frame_url_counts"] = inference_set._temp_frame_count_per_file
        payload["crop_url_counts"] = inference_set._temp_crop_count_per_file

        inference_set._cleanup_temp_dir()

        total_inferences_name = (
            f"inferences_{inference_set.base_dataset_name}_{inference_set.id}"
        )

        print(f"Inferences Processing Queuing...")

        r = requests_retry.post(
            inferences_api_root, headers=self._get_creds_headers(), json=payload
        )
        raise_resp_exception_error(r)
        print(f"Inferences Processing Queued Successfully")

        if wait_until_finish:
            self._wait_until_finish(
                wait_timeout,
                project_name,
                total_inferences_name,
                upload_version,
                "inferences",
            )

    def create_or_update_unlabeled_dataset(
        self,
        unlabeled_dataset: UnlabeledDataset,
        wait_until_finish: bool = False,
        wait_timeout: datetime.timedelta = datetime.timedelta(hours=2),
        preview_first_frame: bool = False,
        delete_cache_files_after_upload: bool = True,
    ) -> None:
        """Create or update an unlabeled dataset with the provided frames and inferences.

        Args:
            unlabeled_dataset: The UnlabeledDataset to upload.
            wait_until_finish: (optional) Block until the dataset processing job finishes. This generally takes at least 5 minutes, and scales with the size of the dataset. Defaults to False.
            wait_timeout: (optional) Maximum time to wait for. Defaults to 2 hours.
            preview_first_frame: (optional) preview the first frame of the dataset in the webapp before continuing. Requires interaction.
            delete_cache_files_after_upload: (optional)flag to turn off automatic deletion of cache files after upload. Useful for ipython notebook users that reload/re-attempt uploads. Defaults to True.
        """
        if not isinstance(unlabeled_dataset, UnlabeledDataset):
            raise Exception(
                f"Cannot upload a {unlabeled_dataset.__class__.__name__} using create_or_update_unlabeled_dataset. Please use the correct corresponding create_or_update client method."
            )

        assert_valid_name(unlabeled_dataset.id)
        project_name = unlabeled_dataset.project_name
        unlabeled_dataset._flush_to_disk()
        if not self._validate_base_streaming_dataset(
            project_name,
            unlabeled_dataset,
            wait_until_finish,
            wait_timeout,
            preview_first_frame,
        ):
            return

        upload_version = str(uuid4())

        print("Uploading Unlabeled Dataset...")
        uuid_prefix = str(uuid4())
        upload_prefix_frame = "{}_frame_data".format(uuid_prefix)
        upload_prefix_crop = "{}_crop_data".format(uuid_prefix)
        upload_suffix = ".jsonl"

        frame_urls = self._upload_rows_from_files(
            project_name,
            unlabeled_dataset.id,
            upload_prefix_frame,
            upload_suffix,
            unlabeled_dataset._temp_frame_file_names_streaming,
            delete_after_upload=delete_cache_files_after_upload,
        )
        crop_urls = self._upload_rows_from_files(
            project_name,
            unlabeled_dataset.id,
            upload_prefix_crop,
            upload_suffix,
            unlabeled_dataset._temp_crop_file_names_streaming,
            delete_after_upload=delete_cache_files_after_upload,
        )
        final_urls = {
            "frame": frame_urls,
            "crop": crop_urls,
            "frame_url_counts": unlabeled_dataset._temp_frame_count_per_file_streaming,
            "crop_url_counts": unlabeled_dataset._temp_crop_count_per_file_streaming,
        }

        if unlabeled_dataset._temp_frame_embeddings_file_names_streaming:
            print("Uploading Unlabeled Dataset Embeddings...")
            upload_frame_prefix = "{}_frame_embeddings".format(str(uuid4()))
            upload_crop_prefix = "{}_crop_embeddings".format(str(uuid4()))
            upload_suffix = ".arrow"
            uploaded_frame_urls = self._upload_rows_from_files(
                project_name,
                unlabeled_dataset.id,
                upload_frame_prefix,
                upload_suffix,
                unlabeled_dataset._temp_frame_embeddings_file_names_streaming,
                delete_after_upload=delete_cache_files_after_upload,
            )
            uploaded_crop_urls = self._upload_rows_from_files(
                project_name,
                unlabeled_dataset.id,
                upload_crop_prefix,
                upload_suffix,
                unlabeled_dataset._temp_crop_embeddings_file_names_streaming,
                delete_after_upload=delete_cache_files_after_upload,
            )
            if uploaded_frame_urls:  # not empty list
                final_urls["frame_embeddings"] = uploaded_frame_urls
            if uploaded_crop_urls:  # not empty list
                final_urls["crop_embeddings"] = uploaded_crop_urls

        if unlabeled_dataset._temp_frame_asset_file_names:
            print("Uploading Unlabeled Frame Assets...")
            upload_prefix = "{}_assets".format(str(uuid4()))
            upload_suffix = ".arrow"
            uploaded_urls = self._upload_rows_from_files(
                project_name,
                unlabeled_dataset.id,
                upload_prefix,
                upload_suffix,
                unlabeled_dataset._temp_frame_asset_file_names,
                delete_after_upload=delete_cache_files_after_upload,
            )
            if uploaded_urls:  # not empty list
                final_urls["frame_asset_url"] = uploaded_urls

        datasets_api_root = self.api_endpoint + "/projects/{}/datasets".format(
            project_name
        )
        payload = {
            "dataset_id": unlabeled_dataset.id,
            "data_url": final_urls,
            "embedding_distance_metric": unlabeled_dataset.embedding_distance_metric,
            "embedding_upload_version": 1,
            "upload_version": upload_version,
            "pipeline_mode": "STREAMING",
            "is_anon_mode": unlabeled_dataset.is_anon_mode,
            "is_unlabeled_indexed_dataset": True,
            "frame_model_version": unlabeled_dataset.frame_embedding_model,
            "crop_model_version": unlabeled_dataset.crop_embedding_model,
            "frame_embedding_dim": unlabeled_dataset.frame_embedding_dim,
            "crop_embedding_dim": unlabeled_dataset.crop_embedding_dim,
            "sample_frame_embeddings": unlabeled_dataset.sample_frame_embeddings,
            "sample_crop_embeddings": unlabeled_dataset.sample_crop_embeddings,
            "total_num_frames": len(unlabeled_dataset._frame_ids_set),
            "total_num_crops": len(unlabeled_dataset._crop_ids_set),
            "streaming_version": unlabeled_dataset._streaming_version,
        }

        if unlabeled_dataset.external_metadata is not None:
            payload["external_metadata"] = unlabeled_dataset.external_metadata

        unlabeled_dataset._cleanup_temp_dir()

        print("Dataset Processing Initiating...")
        r = requests_retry.post(
            datasets_api_root, headers=self._get_creds_headers(), json=payload
        )
        raise_resp_exception_error(r)
        print("Unlabeled Dataset Processing Initiated Successfully")

        if wait_until_finish:
            self._wait_until_finish(
                wait_timeout,
                project_name,
                unlabeled_dataset.id,
                upload_version,
                "unlabeled dataset",
            )

    def _upload_unlabeled_datasetV2_files(
        self,
        project_name: str,
        dataset_name: str,
        dataset: UnlabeledDatasetV2,
        delete_cache_files_after_upload: bool = True,
    ) -> Dict[str, List[str]]:
        if len(dataset._frame_ids_set) == 0:
            raise Exception("Dataset contains no frames and cannot be empty.")

        dataset._flush_to_disk()

        if len(dataset._temp_frame_file_names) == 0:
            raise Exception("Cannot upload dataset with 0 frames")

        print("Uploading Unlabeled Dataset Files...")
        upload_prefix = "{}_data".format(str(uuid4()))
        upload_suffix = ".jsonl"
        file_summaries = [
            {**s, "project_name": project_name, "dataset_name": dataset_name}
            for s in dataset._file_summaries
        ]
        final_urls = self._upload_rows_from_files(
            project_name,
            dataset_name,
            upload_prefix,
            upload_suffix,
            dataset._temp_frame_file_names,
            file_metadata=file_summaries,
            delete_after_upload=delete_cache_files_after_upload,
            bucket="unlabeled-dataset-uploads",
        )

        uploaded_files = {
            "data_url": final_urls,
        }

        dataset._cleanup_temp_dir()
        print("Uploaded all Unlabeled Dataset Files")
        return uploaded_files

    def create_or_update_unlabeled_datasetV2(
        self,
        unlabeled_dataset: UnlabeledDatasetV2,
        delete_cache_files_after_upload: bool = True,
    ) -> None:
        """Create or update an unlabeled dataset

        Args:
            unlabeled_dataset: The UnlabeledDatasetV2 to upload.
            delete_cache_files_after_upload: (optional) flag to turn off automatic deletion of cache files after upload. Useful for ipython notebook users that reload/re-attempt uploads. Defaults to True.
        """
        assert_valid_name(unlabeled_dataset.id)
        if not isinstance(unlabeled_dataset, UnlabeledDatasetV2):
            raise Exception(
                f"Cannot upload a {unlabeled_dataset.__class__.__name__} using create_or_update_unlabeled_datasetV2. Please use the correct corresponding create_or_update client method."
            )

        project_name = unlabeled_dataset.project_name

        if not self.dataset_exists(project_name, unlabeled_dataset.id):
            create_endpoint = (
                f"{self.api_endpoint}/projects/{project_name}/datasets/unlabeled_v2"
            )
            payload = {
                "dataset_name": unlabeled_dataset.id,
                "external_metadata": unlabeled_dataset.external_metadata,
                "frame_model_version": None,
                "crop_model_version": None,
            }
            r = requests_retry.post(
                create_endpoint, headers=self._get_creds_headers(), json=payload
            )
            raise_resp_exception_error(r)
        else:
            existing_dataset = self.get_dataset(project_name, unlabeled_dataset.id)
            is_already_unlabeled_dataset = existing_dataset.get(
                "is_unlabeled_indexed_dataset"
            )
            if not is_already_unlabeled_dataset:
                raise Exception("Cannot append unlabeled data to a labeled dataset")

            unlabeled_dataset_version = existing_dataset.get(
                "unlabeled_dataset_version"
            )
            if not unlabeled_dataset_version or unlabeled_dataset_version < 2:
                raise Exception(
                    "Cannot append unlabeled data to a legacy unlabeled dataset. "
                    "Use initialize_unlabeled_dataset and create_or_update_unlabeled_dataset instead."
                )

        uploaded_files = self._upload_unlabeled_datasetV2_files(
            project_name,
            unlabeled_dataset.id,
            unlabeled_dataset,
            delete_cache_files_after_upload,
        )
        upload_payload = {
            "dataset_name": unlabeled_dataset.id,
            "total_num_frames": len(unlabeled_dataset._frame_ids_set),
            "total_num_crops": len(unlabeled_dataset._crop_ids_set),
            "is_unlabeled_indexed_dataset": True,
            "file_summaries": unlabeled_dataset._file_summaries,
            "client_version": self._client_version,
            **uploaded_files,
        }
        print("Unlabeled Dataset Processing Initiating...")
        upload_endpoint = f"{self.api_endpoint}/projects/{project_name}/datasets/unlabeled_v2/{unlabeled_dataset.id}/upload"
        r = requests_retry.post(
            upload_endpoint, headers=self._get_creds_headers(), json=upload_payload
        )
        raise_resp_exception_error(r)
        print("Unlabeled Dataset Processing Initiated Successfully")

    # Even though this is the same implementation as `update_dataset_metadata`, we split it out
    # because users have been working with inference-specific functions
    def update_inferences_metadata(
        self, project_name: str, inferences_name: str, external_metadata: Dict[str, Any]
    ) -> None:
        """Update inference set metadata

        Args:
            project_name (str): The project id.
            inferences_name (str): The inferences id.
            external_metadata (Dict[Any, Any]): The new metadata
        """
        if not isinstance(external_metadata, dict) or (
            external_metadata and not isinstance(next(iter(external_metadata)), str)
        ):
            raise Exception("external_metadata must be a dict with string keys")

        payload = {"external_metadata": external_metadata}
        r = requests_retry.post(
            f"{self.api_endpoint}/projects/{project_name}/datasets/{inferences_name}/metadata",
            headers=self._get_creds_headers(),
            json=payload,
        )
        raise_resp_exception_error(r)

    def _rehydrate_frame_object(
        self,
        dataset: LabeledDataset,
        frame_dict: Dict[str, Any],
        include_user_metadata: bool = True,
    ) -> LabeledFrame:
        """Recreated a labeled frame object from Dict

        Returns:
            LabeledFrame

        :meta private:
        """
        pipeline_keys = ["_idx", "window", "table", "reuse_latest_embedding"]
        app_keys = ["issues"]
        for key in pipeline_keys:
            frame_dict.pop(key, None)
        for key in app_keys:
            frame_dict.pop(key, None)

        frame_id = frame_dict.pop("task_id")
        date_captured = frame_dict.pop("date_captured")
        device_id = frame_dict.pop("device_id")

        coordinate_frames = frame_dict.pop("coordinate_frames")
        sensor_data = frame_dict.pop("sensor_data")
        label_data = frame_dict.pop("label_data")
        geo_data = frame_dict.pop("geo_data", "{}")

        user_metadata = split_user_attrs(frame_dict)
        for key in user_metadata:
            frame_dict.pop(key, None)

        # warn if there are more fields left in the frame
        if frame_dict:
            keys = ",".join(list(frame_dict.keys()))
            print(
                f"WARNING! Rehydrating a frame resulted in unexpected unused keys: {keys}"
            )
            print("Please reach out to Aquarium if this occurs.")

        # rehydrate explicitly-set coordinate frames
        coordinate_frames_by_id = {}
        for coordinate_frame_json in coordinate_frames:
            coordinate_frame = _get_coordinate_frame_from_json(
                maybe_parse_json_vals(coordinate_frame_json)
            )
            if coordinate_frame:
                coordinate_frames_by_id[coordinate_frame.id] = coordinate_frame

        sensor_data_by_id = {}
        for sensor_json in sensor_data:
            sensor = _get_sensor_data_from_json(
                maybe_parse_json_vals(sensor_json), coordinate_frames_by_id
            )
            sensor_data_by_id[sensor.id] = sensor

        geo_data_instance = None
        if geo_data:
            try:
                geo_dict = json.loads(geo_data)
                if geo_data:
                    geo_data_instance = GeoData(
                        geo_dict["geo_EPSG4326_lat"], geo_dict["geo_EPSG4326_lon"]
                    )
            except:
                pass

        user_metadata_entries = []
        if include_user_metadata:
            # TODO: pull this schema from the server?
            for key, value in user_metadata.items():
                if isinstance(value, (list, tuple)):
                    if not value:
                        continue
                    user_metadata_entries.append(
                        UserMetadataEntry(key, cast(USER_METADATA_SEQUENCE, value))
                    )
                else:
                    user_metadata_entries.append(UserMetadataEntry(key, value))

        instance_seg_instances = []
        instance_seg_masks_by_id = {}
        labels = []
        for label in label_data:
            label_dict = maybe_parse_json_vals(label)
            if label_dict["label_type"] == "INSTANCE_LABEL_URL_2D":
                instance_seg_masks_by_id[label_dict["uuid"]] = label_dict
            elif label_dict["label_type"] == "INSTANCE_LABEL_2D":
                instance_seg_instances.append(label_dict)
            else:
                label = _get_single_label_from_json(label_dict)
                labels.append(label)
        if instance_seg_masks_by_id:
            for id, mask in instance_seg_masks_by_id.items():
                instances = [
                    si
                    for si in instance_seg_instances
                    if si["uuid"].startswith(f"{id}_")
                ]
                label = _get_instance_seg_label_from_jsons(mask, instances)
                labels.append(label)

        labeled_frame = LabeledFrame(
            frame_id=frame_id,
            labels=labels,
            dataset=dataset,
            device_id=device_id,
            date_captured=date_captured,
            coordinate_frames=list(coordinate_frames_by_id.values()),
            sensor_data=list(sensor_data_by_id.values()),
            geo_data=geo_data_instance,
            user_metadata=user_metadata_entries,
        )
        return labeled_frame

    def get_frame_ids(self, project_name: str, dataset_name: str) -> List[str]:
        """Get frame ids in a dataset (for datasets only, not inferences)

        Args:
            project_name (str): The project id.
            dataset_name (str): The dataset id.
        """
        r = requests_retry.get(
            f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}/frame_ids/LATEST",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        result: List[str] = r.json()
        return result

    def get_frame(
        self, project_name: str, dataset_name: str, frame_id: str
    ) -> LabeledFrame:
        """Get frame info (for datasets only, not inferences)

        Args:
            project_name (str): The project id.
            dataset_name (str): The dataset id.
            frame_id (str): The frame id.
        """
        r = requests_retry.get(
            f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}/frame/{frame_id}/LATEST",
            headers=self._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        dataset_object = LabeledDataset(self, dataset_name, project_name)
        result: Dict[str, Any] = r.json()
        result_frame = self._rehydrate_frame_object(dataset_object, result)
        return result_frame

    def get_frames(
        self, project_name: str, dataset_name: str, frame_ids: List[str]
    ) -> Dict[str, LabeledFrame]:
        """Get multple frame infos (for datasets only, not inferences)

        Args:
            project_name (str): The project id.
            dataset_name (str): The dataset id.
            frame_ids (List[str]): The list of frame ids.
        """
        frames_r = requests_retry.post(
            f"{self.api_endpoint}/projects/{project_name}/datasets/{dataset_name}/frames/LATEST",
            headers=self._get_creds_headers(),
            json={"frame_ids": frame_ids},
        )
        raise_resp_exception_error(frames_r)
        dataset_object = LabeledDataset(self, dataset_name, project_name)
        result: List[Dict[str, Any]] = frames_r.json()
        frames = [self._rehydrate_frame_object(dataset_object, f) for f in result]
        return {f.id: f for f in frames}

    def update_dataset_object_metadata_schema(
        self,
        project_name: str,
        dataset_name: str,
        object_metadata_fields: List[Dict[str, str]],
    ) -> None:
        """Update dataset object metadata schema

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name
            object_metadata_fields (List[Dict[str, Any]]): list of object metadata fields, formatted {"name": "width_bucket", "type": "STRING"}
                Type must be one of STRING, BOOL, NUMERIC, INTEGER, FLOAT, or an array of a valid type ARRAY<type>.
        """
        endpoint = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/object_metadata_schema".format(
                project_name, dataset_name
            )
        )
        payload = {"schema": object_metadata_fields}
        r = requests_retry.post(
            endpoint,
            headers=self._get_creds_headers(),
            json=payload,
        )
        raise_resp_exception_error(r)
        print("Object metadata schema updated.")

    def get_dataset_object_metadata_schema(
        self, project_name: str, dataset_name: str
    ) -> List[Dict[str, str]]:
        """Get dataset object metadata schema

        Args:
            project_name (str): project_name
            dataset_name (str): dataset_name
        """
        endpoint = (
            self.api_endpoint
            + "/projects/{}/datasets/{}/object_metadata_schema".format(
                project_name, dataset_name
            )
        )
        r = requests_retry.get(
            endpoint,
            headers=self._get_creds_headers(),
        )
        raise_resp_exception_error(r)
        result: List[Dict[str, str]] = r.json()
        return result


class StratifiedMetricsDict(TypedDict):
    name: str
    ordered_values: List[str]


class StratifiedMetricsDefinition:
    """Definitions for stratified metrics given object-level attributes

    Args:
        name (str): The name of this attribute, which should match the attribute on object labels.
        ordered_values (List[str]): The ordered list of valid values to group by.
    """

    def __init__(self, name: str, ordered_values: Iterable[str]) -> None:
        self.name = name
        self.ordered_values = list(ordered_values)  # In case it's a tuple

    def to_dict(self) -> StratifiedMetricsDict:
        return {"name": self.name, "ordered_values": self.ordered_values}


class CustomMetricsDefinition:
    """Definitions for custom user provided metrics.

    Args:
        name (str): The name of this metric.
        metrics_type (str): The metrics type, either 'objective' or 'confusion_matrix'.
    """

    # TODO: Make these literal types too in the type system?
    OBJECTIVE = "objective"
    CONFUSION_MATRIX = "confusion_matrix"

    def __init__(self, name: str, metrics_type: str) -> None:
        valid_metrics_types = set(["objective", "confusion_matrix"])
        self.name = name
        self.metrics_type = metrics_type

    def to_dict(self) -> Dict[str, str]:
        return {"name": self.name, "metrics_type": self.metrics_type}
