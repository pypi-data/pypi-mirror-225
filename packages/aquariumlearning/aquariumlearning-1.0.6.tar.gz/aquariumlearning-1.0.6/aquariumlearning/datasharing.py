import requests
from typing import Any, Iterable, Dict, List, Callable, Optional, Tuple
from typing_extensions import Literal
from http import HTTPStatus

UrlCheckResult = Literal["SKIPPED", "FAILURE", "SUCCESS", "S3_PATH", "INVALID_URL"]


def _check_urls(
    urls: Iterable[str],
    gs_client: Any,
    requesting_func: Callable[..., requests.Response] = requests.get,
    signing_func: Optional[Callable[[str], Optional[str]]] = None,
) -> Dict[str, UrlCheckResult]:
    result = {}
    for url in urls:
        result[url] = _check_url(
            url, gs_client, requesting_func=requesting_func, signing_func=signing_func
        )
    return result


def _check_url(
    url: str,
    gs_client: Any,
    requesting_func: Callable[..., requests.Response] = requests.get,
    signing_func: Optional[Callable[[str], Optional[str]]] = None,
) -> UrlCheckResult:
    if url.lower().startswith("gs://"):
        if gs_client is None:
            return "SKIPPED"
        else:
            bucket_name, path = url.replace("gs://", "").split("/", 1)
            try:
                bucket = gs_client.get_bucket(bucket_name)
                blob = bucket.get_blob(path)

                if blob is None:
                    return "FAILURE"
                else:
                    return "SUCCESS"
            except:
                return "FAILURE"
    elif url.lower().startswith("http"):
        try:
            # we use stream=True to avoid downloading the entire file for SSRF check
            with requesting_func(url, timeout=5, stream=True) as response:
                code = response.status_code
                if code == HTTPStatus.OK:
                    return "SUCCESS"
                else:
                    return "FAILURE"
        except:
            return "FAILURE"
    # We support S3 paths but only the user can access them from the app, and only if they provide their S3 creds
    # See client/src/util/bucketSigning.tsx
    elif url.lower().startswith("s3://"):
        if not signing_func:
            return "S3_PATH"
        try:
            signed_url = signing_func(url)
            if signed_url:
                return "SUCCESS"
            return "FAILURE"
        except:
            return "FAILURE"
    else:
        return "INVALID_URL"


UrlMode = Literal[
    "ANONYMOUS", "INACCESSIBLE", "VALID", "INVALID_URL", "S3_PATH", "UNSIGNABLE"
]


def _get_mode(
    urls: Iterable[str],
    local_results: Dict[str, UrlCheckResult],
    server_results: Dict[str, UrlCheckResult],
) -> Dict[str, UrlMode]:
    modes: Dict[str, UrlMode] = {}
    for url in urls:
        if server_results[url] == "FAILURE":
            if local_results[url] == "SUCCESS":
                modes[url] = "ANONYMOUS"
            elif local_results[url] == "SKIPPED":
                modes[url] = "INACCESSIBLE"
            elif local_results[url] == "FAILURE":
                modes[url] = "INACCESSIBLE"
            elif local_results[url] == "S3_PATH":
                modes[url] = "UNSIGNABLE"
        elif server_results[url] == "SUCCESS":
            modes[url] = "VALID"
        elif server_results[url] == "INVALID_URL":
            modes[url] = "INVALID_URL"
        elif server_results[url] == "S3_PATH":
            modes[url] = "S3_PATH"
    return modes


def _get_errors(mode: Dict[str, UrlMode]) -> Tuple[List[str], List[str], bool]:
    errors = []
    warnings = []

    is_anon = False
    for url in mode:
        if mode[url] == "INVALID_URL":
            errors += [
                f"{url} is not a supported URL format. Please provide a URL starting with gs://, s3://, http://, or https://"
            ]
        elif mode[url] == "INACCESSIBLE":
            errors += [
                f"{url} is not an accessible URL from Aquarium servers or this machine. Please verify the URL path."
            ]
        elif mode[url] == "UNSIGNABLE":
            errors += [
                f"{url} is not an accessible URL from Aquarium servers. Please verify that Aquarium has access to this URL path."
            ]
        elif mode[url] == "S3_PATH":
            is_anon = True
            warnings += [
                f"{url} is not an accessible URL from Aquarium servers. You will need to set your S3 creds in the web app to view your assets."
            ]
        elif mode[url] == "ANONYMOUS":
            is_anon = True

    return errors, warnings, is_anon
