import markdown
import pytest

from neoteroi.mkdocs.markdown.data.web import (
    FailedRequestError,
    HTTPDataReader,
    ensure_success,
)
from neoteroi.mkdocs.timeline import TimelineExtension
from tests.test_timeline import EXAMPLE_1

from .serverfixtures import *  # noqa
from .serverfixtures import BASE_URL


def test_fetch_yaml():
    reader = HTTPDataReader()
    text = reader.read(f"{BASE_URL}/timeline-1.json")
    assert '"title": "Zero"' in text


def test_failed_request():
    reader = HTTPDataReader()
    with pytest.raises(FailedRequestError) as failed_request:
        response = reader.read(f"{BASE_URL}/missing-file.json")
        ensure_success(response)

    error = failed_request.value
    # there is no inner exception in this case
    assert error.inner_exception is None


def test_timeline_from_url():
    example = f"""
    [timeline({BASE_URL}/timeline-1.json)]
    """
    html = markdown.markdown(example, extensions=[TimelineExtension(priority=100)])
    assert html.strip() == EXAMPLE_1.strip()
