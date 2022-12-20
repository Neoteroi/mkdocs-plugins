import pytest

from neoteroi.mkdocs.markdown.align import (
    Alignment,
    aligment_from_props,
    try_parse_align,
)


@pytest.mark.parametrize(
    "value,expected_result",
    [
        [{"left": True}, Alignment.LEFT],
        [{"align": "left"}, Alignment.LEFT],
        [{"center": True}, Alignment.CENTER],
        [{"align": "center"}, Alignment.CENTER],
        [{"right": True}, Alignment.RIGHT],
        [{"align": "right"}, Alignment.RIGHT],
    ],
)
def test_alignment_from_props(value, expected_result):
    assert aligment_from_props(value) == expected_result


def test_try_parse_align_returns_default():
    assert try_parse_align("foo") == Alignment.LEFT
