import requests
from collections.abc import Iterable
from .util import (
    ElementType,
    ElementCropType,
    SegmentState,
    all_segment_states,
    segment_template_type_mapping,
    raise_resp_exception_error,
)
from typing import Any, List, Dict, Optional, Tuple, TYPE_CHECKING
from typing_extensions import TypedDict

if TYPE_CHECKING:
    from .client import Client


class SegmentElement:
    """Definition for segment element.

    Args:
        element_id (str): The element id. Either the frame_id if element_type is 'frame' or the label_id or inference_id if element_type is 'crop'.
        frame_id (str): The frame id of the element.
        element_type (str): The element type of the segment element ("frame" or "crop").
        crop_type (str): The provenance of the segment element if it's a crop ("label", or "inference"). If it's a frame, leave as None.
        dataset (str): The base dataset an element is from. (Can be formatted as either "project_name.dataset_name" or just "dataset_name")
        inference_set (str): The inference set an element is from (if any). (Can be formatted as either "project_name.inference_set_name" or just "inference_set_name")
        status (str): (*For read purposes, not element modification*). The status of the element.
        frame_data: (*For read purposes, not element modification*). JSON object that is based on either a LabeledFrame or InferenceFrame
        crop_data: (*For read purposes, not element modification*). JSON object for the specific "frame_data" crop that a "crop"-type element is based on.
        label_metadata: (*For read purposes, not element modification*). JSON object with confidence and IOU info if the element was created from a ground truth/inference comparison.
        comments: (*For read purposes, not element modification*). JSON object with comments.
        updated_at: (str) (*For read purposes, not element modification*). The time this segment element was last updated.
    """

    def __init__(
        self,
        element_id: str,
        frame_id: str,
        element_type: str,
        dataset: str,
        crop_type: Optional[ElementCropType] = None,
        status: Optional[str] = None,
        inference_set: Optional[str] = None,
        # TODO: Type these three objects
        frame_data: Optional[Dict[str, Any]] = None,
        crop_data: Optional[Dict[str, Any]] = None,
        label_metadata: Optional[Dict[str, Any]] = None,
        comments: Optional[Dict[str, Any]] = None,
        updated_at: Optional[str] = None,
    ):
        if element_type != "crop" and element_type != "frame":
            raise Exception('element_type must be either "crop" or "frame"')

        if not isinstance(frame_id, str):
            raise Exception("frame ids must be strings")

        if element_type != "frame" and not crop_type:
            # see if we can infer this
            if not inference_set:
                crop_type = "label"
            else:
                raise Exception(
                    f"Cannot infer the crop type of element {element_id} -- please set crop_type to either 'label' or 'inference'"
                )

        self.element_id = element_id
        self.frame_id = frame_id
        self.element_type = element_type
        self.crop_type = crop_type
        self.status = status
        self.dataset = dataset
        self.inference_set = inference_set
        self.frame_data = frame_data
        self.crop_data = crop_data
        self.label_metadata = label_metadata
        self.comments = comments
        self.updated_at = updated_at

    def to_dict(self) -> Dict[str, Any]:
        return {
            "element_id": self.element_id,
            "frame_id": self.frame_id,
            "element_type": self.element_type,
            "status": self.status,
            "dataset": self.dataset,
            "inference_set": self.inference_set,
            "frame_data": self.frame_data,
            "crop_data": self.crop_data,
            "label_metadata": self.label_metadata,
            "comments": self.comments,
            "updated_at": self.updated_at,
        }

    # For element modification
    def _to_api_format(self, project_name: str) -> Dict[str, Any]:
        api_payload = {
            "id": self.element_id,
            "frameId": self.frame_id,
            "type": self.element_type,
        }

        dataset_address = (
            self.dataset
            if "." in self.dataset
            else ".".join([project_name, self.dataset])
        )
        api_payload["dataset"] = dataset_address

        if self.inference_set is not None:
            inference_set_address = (
                self.inference_set
                if "." in self.inference_set
                else ".".join([project_name, self.inference_set])
            )
            api_payload["inferenceSet"] = inference_set_address

        return api_payload


# TODO: Which of these are specifically optional?
# TODO: Are they optional (as in, Nullable), or are they missing keys?


class SegmentElementApiResp(TypedDict):
    """:meta private:"""

    id: str
    frameId: str
    type: ElementType
    cropType: ElementCropType
    status: str  # TODO: Types
    dataset: str
    inferenceSet: Optional[str]
    frameData: Optional[Dict[str, Any]]
    cropData: Optional[Dict[str, Any]]
    labelMetadata: Optional[Dict[str, Any]]
    comments: Optional[Dict[str, Any]]
    updated_at: Optional[str]


class SegmentApiResp(TypedDict):
    """:meta private:"""

    id: str
    compare_dataset: Optional[str]
    dataset: Optional[str]
    name: str
    element_type: ElementType
    created_at: Optional[str]
    updated_at: Optional[str]
    reporter: Optional[str]
    assignee: Optional[str]
    state: Optional[SegmentState]
    segment_id: Optional[str]
    elements: List[SegmentElementApiResp]
    comments: Optional[Dict[str, Any]]
    template_type: Optional[str]
    custom_template_fields: Optional[Dict[str, Any]]


class SegmentSummary:
    """Definition for segment summary.

    Args:
        name (str): The segment name.
        dataset (Optional[str]): The dataset for this segment.
        element_type (str): The element type of the segment ("frame", "crop").
        created_at (str): The time of segment creation.
        updated_at (str): The time of last segment update.
        reporter (str): Email of segment creator.
        assignee (Optional[str], optional): Email of the person assigned the segment. Defaults to None.
        state (str): Current state of segment ("triage", "inProgress", "inReview", "resolved", "cancelled"). Defaults to "triage".
        segment_id (str): The segment id.
        inference_set (Optional[str], optional): The inference set for this segment. Defaults to None.
        template_type (Optional[str]): The template type for this segment. (read-only)
        custom_template_fields (Optional[Dict[str, Any]]): Custom fields associated with the segment template type. (read-only)
    """

    def __init__(
        self,
        name: str,
        dataset: Optional[str],
        element_type: ElementType,
        # TODO: This used to say datetime, but it looks like it should be a str?
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        reporter: Optional[str] = None,
        assignee: Optional[str] = None,
        state: Optional[str] = None,
        segment_id: Optional[str] = None,
        inference_set: Optional[str] = None,
        comments: Optional[Dict[str, Any]] = None,
        template_type: Optional[str] = None,
        custom_template_fields: Optional[Dict[str, Any]] = None,
    ):
        self.name = name
        self.dataset = dataset
        self.element_type = element_type
        self.created_at = created_at
        self.updated_at = updated_at
        self.reporter = reporter
        self.assignee = assignee
        self.state = state
        self.segment_id = segment_id
        self.inference_set = inference_set
        self.comments = comments
        self.template_type = template_type
        self.custom_template_fields = custom_template_fields

    def __repr__(self) -> str:
        return "Segment {} ({})".format(self.segment_id, self.name)

    def __str__(self) -> str:
        return "Segment {} ({})".format(self.segment_id, self.name)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "dataset": self.dataset,
            "element_type": self.element_type,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "reporter": self.reporter,
            "assignee": self.assignee,
            "state": self.state,
            "segment_id": self.segment_id,
            "inference_set": self.inference_set,
            "comments": self.comments,
            "template_type": self.template_type,
            "custom_template_fields": self.custom_template_fields,
        }


class Segment(SegmentSummary):
    """Definition for segment.

    Args:
        name (str): The segment name.
        dataset (Optional[str]): The dataset for this segment.
        element_type (str): The element type of the segment ("frame", "crop").
        created_at (str): The time of segment creation.
        updated_at (str): The time of last segment update.
        reporter (str): Email of segment creator.
        assignee (Optional[str], optional): Email of the person assigned the segment. Defaults to None.
        state (str): Current state of segment ("triage", "inProgress", "inReview", "resolved", "cancelled"). Defaults to "triage".
        segment_id (str): The segment id.
        inference_set (Optional[str], optional): The inference set for this segment. Defaults to None.
        template_type (Optional[str]): The template type for this segment. (read-only)
        custom_template_fields (Optional[Dict[str, Any]]): Custom fields associated with the segment template type. (read-only)
        elements (List[SegmentElement]): The elements of the segment.
    """

    def __init__(
        self,
        name: str,
        dataset: Optional[str],
        element_type: ElementType,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        reporter: Optional[str] = None,
        assignee: Optional[str] = None,
        state: Optional[str] = None,
        segment_id: Optional[str] = None,
        inference_set: Optional[str] = None,
        comments: Optional[Dict[str, Any]] = None,
        template_type: Optional[str] = None,
        custom_template_fields: Optional[Dict[str, Any]] = None,
        elements: (List[SegmentElement]) = [],
    ):
        super().__init__(
            name,
            dataset,
            element_type,
            created_at,
            updated_at,
            reporter,
            assignee,
            state,
            segment_id,
            inference_set,
            comments,
            template_type,
            custom_template_fields,
        )
        self.elements = elements

    def to_dict(self) -> Dict[str, Any]:
        summary_dict = super().to_dict()
        summary_dict["elements"] = [x.to_dict() for x in self.elements]
        return summary_dict


class SegmentManager:
    """An segment manager for interacting with segments within a given project.

    Args:
        client (Client): An Aquarium Learning Python Client object.
        project_name (str): The project id associated with this manager.
    """

    def __init__(self, client: "Client", project_name: str) -> None:
        self.client = client
        self.project_name = project_name

    @staticmethod
    def _kwargs_from_api_resp(
        api_resp: SegmentApiResp,
    ) -> Tuple[Dict[str, Any], List[SegmentElement]]:
        # TODO: Hack because internal data model for segments is still dataset/compare dataset,
        # not dataset + inference set + other inference set.

        compare_dataset = api_resp.get("compare_dataset")
        raw_dataset = api_resp.get("dataset")
        dataset: Optional[str] = None
        inference_set: Optional[str] = None

        if compare_dataset and raw_dataset:
            dataset = compare_dataset.split(".")[1]
            inference_set = raw_dataset.split(".")[1]
        elif raw_dataset:
            dataset = raw_dataset.split(".")[1]
            inference_set = None
        else:  # in the case of an segment with no elements
            dataset = None
            inference_set = None

        elements = []
        for raw_el in api_resp.get("elements", []):
            # TODO: Is the change to explicit accesses vs nullable gets correct?
            elements.append(
                SegmentElement(
                    element_id=raw_el["id"],
                    frame_id=raw_el["frameId"],
                    element_type=raw_el["type"],
                    crop_type=raw_el.get("cropType"),
                    dataset=raw_el["dataset"],
                    status=raw_el.get("status"),
                    inference_set=raw_el.get("inferenceSet"),
                    frame_data=raw_el.get("frameData"),
                    crop_data=raw_el.get("cropData"),
                    label_metadata=raw_el.get("labelMetadata"),
                    comments=raw_el.get("comments"),
                    updated_at=raw_el.get("updated_at"),
                )
            )

        return (
            dict(
                name=api_resp["name"],
                element_type=api_resp["element_type"],
                created_at=api_resp.get("created_at"),
                updated_at=api_resp.get("updated_at"),
                reporter=api_resp.get("reporter"),
                assignee=api_resp.get("assignee"),
                state=api_resp.get("state"),
                segment_id=api_resp["id"],
                comments=api_resp.get("comments"),
                dataset=dataset,
                inference_set=inference_set,
                template_type=api_resp.get("template_type"),
                custom_template_fields=api_resp.get("custom_template_fields"),
            ),
            elements,
        )

    @classmethod
    def _segment_from_api_resp(cls, api_resp: SegmentApiResp) -> Segment:
        kwargs, elements = cls._kwargs_from_api_resp(api_resp)
        kwargs["elements"] = elements
        return Segment(**kwargs)

    @classmethod
    def _segment_summary_from_api_resp(cls, api_resp: SegmentApiResp) -> SegmentSummary:
        kwargs, _ = cls._kwargs_from_api_resp(api_resp)
        return SegmentSummary(**kwargs)

    def add_elements_to_segment(
        self, segment_id: str, elements: List[SegmentElement]
    ) -> None:
        """Add elements to an segment.

        Args:
            segment_id (str): The segment id.
            elements (List[SegmentElement]): The elements to add to the segment.
        """
        if not isinstance(elements, Iterable):
            raise Exception("elements must be an iterable of SegmentElement")

        # Validate contents of iterables:
        element_type_set = set()
        for element in elements:
            if not isinstance(element, SegmentElement):
                raise Exception("elements must be an iterable of SegmentElement")
            element_type_set.add(element.element_type)

        if len(element_type_set) != 1:
            raise Exception("Elements must contain exactly one element type")

        element_type = next(iter(element_type_set))
        payload = {
            "element_type": element_type,
            "elements": [x._to_api_format(self.project_name) for x in elements],
            "edit_type": "add",
        }

        url = "/projects/{}/issues/{}/elements".format(self.project_name, segment_id)
        r = requests.patch(
            self.client.api_endpoint + url,
            headers=self.client._get_creds_headers(),
            json=payload,
        )

        raise_resp_exception_error(r)

    def remove_elements_from_segment(
        self, segment_id: str, elements: List[SegmentElement]
    ) -> None:
        """Remove elements from an segment.

        Args:
            segment_id (str): The segment id.
            elements (List[SegmentElement]): The elements to remove from the segment.
        """
        if not isinstance(elements, Iterable):
            raise Exception("elements must be an iterable of SegmentElement")

        # Validate contents of iterables:
        element_type_set = set()
        for element in elements:
            if not isinstance(element, SegmentElement):
                raise Exception("elements must be an iterable of SegmentElement")
            element_type_set.add(element.element_type)

        if len(element_type_set) != 1:
            raise Exception("Elements must contain exactly one element type")

        element_type = next(iter(element_type_set))
        payload = {
            "element_type": element_type,
            "elements": [x._to_api_format(self.project_name) for x in elements],
            "edit_type": "remove",
        }

        url = "/projects/{}/issues/{}/elements".format(self.project_name, segment_id)
        r = requests.patch(
            self.client.api_endpoint + url,
            headers=self.client._get_creds_headers(),
            json=payload,
        )

        raise_resp_exception_error(r)

    def list_segment_summaries(self) -> List[SegmentSummary]:
        """List segment summaries in the associated project.

        NOTE: this does NOT include the segment elements. Use `get_segment` to fetch all the elements for a specific segment

        Returns:
            List[SegmentSummary]: List of all SegmentSummary.
        """
        url = "/projects/{}/issues".format(self.project_name)
        r = requests.get(
            self.client.api_endpoint + url, headers=self.client._get_creds_headers()
        )

        raise_resp_exception_error(r)
        return [self._segment_summary_from_api_resp(x) for x in r.json()]

    def create_segment(
        self,
        name: str,
        dataset: str,
        elements: List[SegmentElement],
        element_type: ElementType,
        inference_set: Optional[str] = None,
        segment_type: Optional[str] = "Bucket",
        work_queue_batch_size: Optional[int] = None,
    ) -> str:
        """Create an segment.

        Args:
            name (str): The segment name.
            dataset (str): The dataset for this segment.
            elements (List[SegmentElement]): The initial elements of the segment.
            element_type (str): The element type of the segment ("frame" or "crop").
            inference_set (Optional[str], optional): The inference set for this segment. Defaults to None.
            segment_type (Optional[str], optional): The type of this segment. Must be one of "Split", "Regression Test", "Scenario", "Collection Campaign", "Label Quality", "Bucket", "Frame Issue", or "Work Queue". Defaults to "Bucket".
        Returns:
            str: The created segment id.
        """
        if not isinstance(name, str):
            raise Exception("Segment names must be strings")

        if segment_type not in segment_template_type_mapping:
            valid_types = ", ".join(segment_template_type_mapping.keys())
            raise Exception(
                "Segment type {} is invalid. Must be {}".format(
                    segment_type, valid_types
                )
            )

        if not self.client.dataset_exists(self.project_name, dataset):
            raise Exception("Dataset {} does not exist".format(dataset))

        if inference_set is not None:
            if not self.client.dataset_exists(self.project_name, inference_set):
                raise Exception("Inference set {} does not exist".format(inference_set))

        if element_type != "frame" and element_type != "crop":
            raise Exception('element type must be "frame" or "crop"')

        if not isinstance(elements, Iterable):
            raise Exception("elements must be an iterable of SegmentElement")

        # Validate contents of iterables:
        for element in elements:
            if not isinstance(element, SegmentElement):
                raise Exception("elements must be an iterable of SegmentElement")
            if element.element_type != element_type:
                raise Exception(
                    "Child element {} has element type {} which conflicts with segment element type {}".format(
                        element.element_id, element.element_type, element_type
                    )
                )

        segment_type_info = segment_template_type_mapping[segment_type]

        payload = {
            "name": name,
            "elements": [x._to_api_format(self.project_name) for x in elements],
            "element_type": element_type,
            "issue_template_type": segment_type_info["type"],
            "issue_template_category": segment_type_info["category"],
        }

        if segment_type == "Work Queue":
            payload["issue_category"] = "work-queue"
            if work_queue_batch_size:
                payload["work_queue_batch_size"] = work_queue_batch_size

        # TODO: Hack because internal data model for segments is still dataset/compare dataset,
        # not dataset + inference set + other inference set.

        if inference_set is None:
            payload_dataset = ".".join([self.project_name, dataset])
            payload_compare_dataset = None
        else:
            payload_dataset = ".".join([self.project_name, inference_set])
            payload_compare_dataset = ".".join([self.project_name, dataset])

        payload["dataset"] = payload_dataset
        payload["compare_dataset"] = payload_compare_dataset

        url = "/projects/{}/issues".format(self.project_name)
        r = requests.post(
            self.client.api_endpoint + url,
            headers=self.client._get_creds_headers(),
            json=payload,
        )

        raise_resp_exception_error(r)
        resp_data: SegmentApiResp = r.json()

        segment_uuid = resp_data["id"]
        if segment_type_info.get("create_collection_campaign"):
            cache_campaign_data_url = "/collection_campaigns/cache_elt_data"
            elt_data_resp = requests.post(
                self.client.api_endpoint + cache_campaign_data_url,
                headers=self.client._get_creds_headers(),
                json={"issue_uuid": segment_uuid},
            )
            raise_resp_exception_error(elt_data_resp)
            elt_data_resp_json = elt_data_resp.json()

            collection_campaign_url = "/collection_campaigns"
            collection_campaign_resp = requests.post(
                self.client.api_endpoint + collection_campaign_url,
                headers=self.client._get_creds_headers(),
                json={
                    "issue_uuid": segment_uuid,
                    "dataset": payload_dataset,
                    "elt_data_gs_path": elt_data_resp_json["gs_path"],
                    "elt_data_format_version": elt_data_resp_json["format_version"],
                },
            )
            raise_resp_exception_error(collection_campaign_resp)

        return segment_uuid

    def create_work_queue(
        self,
        name: str,
        dataset: str,
        elements: List[SegmentElement],
        element_type: ElementType,
        inference_set: Optional[str] = None,
        work_queue_batch_size: int = 100,
    ) -> str:
        """Create a work queue segment.

        Args:
            name (str): The segment name.
            dataset (str): The dataset for this segment.
            elements (List[SegmentElement]): The initial elements of the segment.
            element_type (str): The element type of the segment ("frame" or "crop").
            inference_set (Optional[str], optional): The inference set for this segment. Defaults to None.
        Returns:
            str: The created segment id.
        """
        return self.create_segment(
            name=name,
            dataset=dataset,
            elements=elements,
            element_type=element_type,
            inference_set=inference_set,
            segment_type="Work Queue",
            work_queue_batch_size=work_queue_batch_size,
        )

    def get_segment(
        self,
        segment_id: str,
        exclude_frame_data: bool = False,
        include_comment_data: bool = False,
        exclude_frame_inferences: bool = False,
    ) -> Segment:
        """Get a specific segment in the associated project.
        This will also include all associated frame metadata associated with each element.

        Args:
            segment_id (str): The segment id.
            exclude_frame_data (bool): Set to True to exclude full frame data from the segment element (e.g. to cut down on download size).
            include_comment_data (bool): Set to True to include comments on the segment and segment elements.
            exclude_frame_inferences (bool): Set to True to exclude inferences (if any) from the full frame data (could cut down on download size if frame_data is still desired)

        Returns:
            Segment: The segment data (including frame_data, crop_data, label_metadata, and comments).
        """
        url = "/projects/{}/issues/{}/download_elements".format(
            self.project_name, segment_id
        )

        r = requests.get(
            self.client.api_endpoint + url,
            headers=self.client._get_creds_headers(),
            params={
                "get_as_gcs_file": True,
                "exclude_frame_data": exclude_frame_data,
                "include_comment_data": include_comment_data,
                "prefer_dataset_labels": exclude_frame_inferences,
            },
        )

        raise_resp_exception_error(r)
        signed_url = r.json()["signed_url"]
        r = requests.get(signed_url)
        return self._segment_from_api_resp(r.json())

    def delete_segment(self, segment_id: str) -> None:
        """Delete a segment.

        Args:
            segment_id (str): The segment id.
        """
        url = "/projects/{}/issues/{}".format(self.project_name, segment_id)
        r = requests.delete(
            self.client.api_endpoint + url, headers=self.client._get_creds_headers()
        )

        raise_resp_exception_error(r)

    def update_segment_state(
        self, segment_id: str, segment_state: SegmentState
    ) -> None:
        """Update segment state.

        Args:
            segment_id (str): The segment id.
            segment_state (str): The new segment state. ("triage", "inProgress", "inReview", "resolved", "cancelled")
        """

        if not isinstance(segment_id, str):
            raise Exception("Segment id must be a string")

        if not isinstance(segment_state, str):
            raise Exception("Segment state must be a string")

        if segment_state not in all_segment_states:
            raise Exception("Invalid segment state")

        payload = {"state": segment_state}

        url = "/projects/{}/issues/{}/update_state".format(
            self.project_name, segment_id
        )
        r = requests.patch(
            self.client.api_endpoint + url,
            headers=self.client._get_creds_headers(),
            json=payload,
        )

        raise_resp_exception_error(r)

    def update_segment_name(self, segment_id: str, segment_name: str) -> None:
        """Update segment name.

        Args:
            segment_id (str): The segment id.
            segment_name (str): The new segment name.
        """

        if not isinstance(segment_id, str):
            raise Exception("Segment id must be a string")

        if not isinstance(segment_name, str):
            raise Exception("Segment name must be a string")

        payload = {"name": segment_name}

        url = "/projects/{}/issues/{}/rename".format(self.project_name, segment_id)
        r = requests.patch(
            self.client.api_endpoint + url,
            headers=self.client._get_creds_headers(),
            json=payload,
        )

        raise_resp_exception_error(r)

    def update_elements_status(
        self, segment_id: str, element_ids: List[str], new_status: str
    ) -> None:
        """Update segment elements status.

        Args:
            segment_id (str): The segment id.
            new_status (str): The new status. ("unstarted", "done")
        """

        payload = {
            "edit_type": "update",
            "element_type": None,
            "elements": [{"id": element_id} for element_id in element_ids],
            "new_status": new_status,
        }

        url = "/projects/{}/issues/{}/elements".format(self.project_name, segment_id)

        r = requests.patch(
            self.client.api_endpoint + url,
            headers=self.client._get_creds_headers(),
            json=payload,
        )

        raise_resp_exception_error(r)
