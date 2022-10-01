import pytest

from neoteroi.contribs.domain import Contributor
from neoteroi.contribs.git import GitContributionsReader


@pytest.mark.parametrize(
    "value,expected_result",
    [
        [
            "     2\tRoberto Prevato <roberto.prevato@example.com>\n",
            [Contributor("Roberto Prevato", "roberto.prevato@example.com", 2)],
        ],
        [
            (
                "     14\tRoberto Prevato <roberto.prevato@example.com>\n"
                "     3\tCharlie Brown <charlieb@example.com>\n"
            ),
            [
                Contributor("Roberto Prevato", "roberto.prevato@example.com", 14),
                Contributor("Charlie Brown", "charlieb@example.com", 3),
            ],
        ],
    ],
)
def test_parse_contributors(value, expected_result):
    reader = GitContributionsReader()
    contributors = list(reader.parse_committers(value))
    assert contributors == expected_result
