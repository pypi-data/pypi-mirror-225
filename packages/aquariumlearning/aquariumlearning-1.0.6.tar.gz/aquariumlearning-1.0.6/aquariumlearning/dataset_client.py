from typing import Any, Dict, List, Optional, cast, TYPE_CHECKING

from .class_map import ClassMapEntry, LabelClassMap
from .util import PrimaryTaskTypes, raise_resp_exception_error, requests_retry

if TYPE_CHECKING:
    from .client import Client
    from .datasharing import UrlCheckResult


class DatasetClient:
    """An internal class to manage dataset validation functions when building a dataset for upload

    :meta private:
    """

    _project_classes_by_name: Optional[Dict[str, ClassMapEntry]] = None
    _project_primary_task: Optional[PrimaryTaskTypes] = None
    project_name: str
    dataset_name: str
    client: "Client"

    @staticmethod
    def get_or_init(
        client: "Client", project_name: str, dataset_name: str
    ) -> "DatasetClient":
        key = (project_name, dataset_name)
        if key in client._dataset_clients:
            return client._dataset_clients[key]

        dc = DatasetClient(client, project_name, dataset_name)
        client._dataset_clients[key] = dc
        return dc

    def __init__(
        self,
        client: "Client",
        project_name: str,
        dataset_name: str,
    ):
        self.client = client
        self.project_name = project_name
        self.dataset_name = dataset_name

    def _populate_project_fields(self) -> None:
        r = requests_retry.get(
            self.client.api_endpoint + "/projects/" + self.project_name,
            headers=self.client._get_creds_headers(),
        )

        raise_resp_exception_error(r)
        result: Dict[str, Any] = r.json()

        pt = result.get("primary_task") or PrimaryTaskTypes.ObjectDetection.value
        try:
            self._project_primary_task = PrimaryTaskTypes(pt)
        except Exception as e:
            # an invalid string! we would have treated this like an object detection task in the app, so let's just go with that for now
            self._project_primary_task = PrimaryTaskTypes.ObjectDetection
        existing_class_map: List[Dict[str, Any]] = result["label_class_map"]
        class_map = LabelClassMap()
        for lc in existing_class_map:
            color = lc["color"][:3]
            train_color = lc.get("train_color")
            train_color = train_color[:3] if train_color else None
            lc_instance = ClassMapEntry(
                name=lc["name"],
                class_id=lc["id"],
                color=color,
                train_name=lc.get("train_name"),
                train_id=lc.get("train_id"),
                category=lc.get("category"),
                category_id=lc.get("category_id"),
                has_instances=lc.get("has_instances", True),
                ignore_in_eval=lc.get("ignore_in_eval", False),
                train_color=train_color,
                keypoint_names=lc.get("keypoint_names"),
                skeleton=lc.get("skeleton"),
            )
            class_map.add_entry(lc_instance)
        self._project_classes_by_name = class_map.arrange_entries_by_classname()

    def _get_primary_task(self) -> PrimaryTaskTypes:
        if not self._project_primary_task:
            self._populate_project_fields()

        # TODO: find a less manual way to assert that _populate_project_fields sets multiple fields?
        return cast(PrimaryTaskTypes, self._project_primary_task)

    def _get_project_classes_by_classname(self) -> Dict[str, ClassMapEntry]:
        if not self._project_classes_by_name:
            self._populate_project_fields()

        return cast(Dict[str, ClassMapEntry], self._project_classes_by_name)

    def _verify_urls(self, urls: List[str]) -> Dict[str, "UrlCheckResult"]:
        r = requests_retry.post(
            self.client.api_endpoint + "/datasets/verify_urls",
            headers=self.client._get_creds_headers(),
            json={"urls": urls},
        )
        server_results = r.json()
        return server_results

    def _get_latest_frame_windows(self, frame_ids: List[str]) -> List[List[str]]:
        frames_r = requests_retry.post(
            f"{self.client.api_endpoint}/projects/{self.project_name}/datasets/{self.dataset_name}/frame_windows/LATEST",
            headers=self.client._get_creds_headers(),
            json={"frame_ids": frame_ids},
        )

        raise_resp_exception_error(frames_r)
        result: List[List[str]] = frames_r.json()
        return result
