import os
from typing import Any

import httpx

from .source import DataReader

HTTPX_DISABLE_SSL_VERIFY = bool(os.environ.get("HTTPX_DISABLE_SSL_VERIFY"))

default_http_client = httpx.Client(verify=not HTTPX_DISABLE_SSL_VERIFY, timeout=20)


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


class HTTPDataReader(DataReader):
    http_client: httpx.Client = default_http_client

    def test(self, source: str) -> bool:
        source_lower = source.lower()
        return source_lower.startswith("http://") or source_lower.startswith("https://")

    def get(self, url: str) -> httpx.Response:
        try:
            return self.http_client.get(url)
        except httpx.HTTPError as http_error:  # pragma: no cover
            raise FailedRequestError(str(http_error)) from http_error

    def read(self, source: str) -> Any:
        assert self.test(source)
        response = self.get(source)

        ensure_success(response)
        return response.text
