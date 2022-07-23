import os
from typing import Any

import httpx

from .source import DataReader

HTTPX_DISABLE_SSL_VERIFY = bool(os.environ.get("HTTPX_DISABLE_SSL_VERIFY"))

http_client = httpx.Client(verify=not HTTPX_DISABLE_SSL_VERIFY, timeout=20)


class FailedRequestError(Exception):
    def __init__(self, message) -> None:
        super().__init__(
            f"Failed request: {message}. "
            "Inspect the inner exception (__context__) for more information."
        )

    @property
    def inner_exception(self):
        return self.__context__


def ensure_success(response: httpx.Response) -> None:
    if response.status_code < 200 or response.status_code > 399:
        raise FailedRequestError(
            "Response status does not indicate success: "
            f"{response.status_code} {response.reason_phrase}"
        )


def http_get(url: str) -> httpx.Response:
    try:
        return http_client.get(url)
    except httpx.HTTPError as http_error:
        raise FailedRequestError(str(http_error)) from http_error


# def read_from_url(url: str):
#     """
#     Tries to read OpenAPI Documentation from the given source URL.
#     This method will try to fetch JSON or YAML from the given source, in case of
#     ambiguity regarding the content, it will to parse anyway the response as JSON or
#     YAML (using safe load when handling YAML).
#     """
#     response = http_get(url)
#
#     ensure_success(response)
#
#     data = response.text
#     content_type = response.headers.get("content-type")
#
#     if "json" in content_type or url.endswith(".json"):
#         return json.loads(data)
#
#     if "yaml" in content_type or url.endswith(".yaml") or url.endswith(".yml"):
#         return yaml.safe_load(data)


class HTTPSource(DataReader):
    def test(self, source: str) -> bool:
        source_lower = source.lower()
        return source_lower.startswith("http://") or source_lower.startswith("https://")

    def read(self, source: str) -> Any:
        assert self.test(source)

        response = http_get(source)

        ensure_success(response)
        data = response.text
        content_type = response.headers.get("content-type")
        #################
        # TODO: parse!
        #################
        return data
