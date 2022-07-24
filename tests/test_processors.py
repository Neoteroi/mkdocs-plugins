import re

import pytest

from neoteroi.markdown.processors import find_closing_fragment_index


@pytest.mark.parametrize(
    "pattern,blocks,expected_result",
    [
        [
            re.compile("adipiscing elit"),
            [
                "Lorem ipsum",
                " dolor sit amet, \n",
                "consectetur adipiscing elit,",
                "\nsed do eiusmod tempor",
            ],
            2,
        ],
        [
            re.compile("eiusmod"),
            [
                "Lorem ipsum",
                " dolor sit amet, \n",
                "consectetur adipiscing elit,",
                "\nsed do eiusmod tempor",
            ],
            3,
        ],
        [
            re.compile("Sonic"),
            [
                "Lorem ipsum",
                " dolor sit amet, \n",
                "consectetur adipiscing elit,",
                "\nsed do eiusmod tempor",
            ],
            -1,
        ],
    ],
)
def test_find_closing_fragment_index(pattern, blocks, expected_result):
    index = find_closing_fragment_index(pattern, blocks)
    assert index == expected_result
