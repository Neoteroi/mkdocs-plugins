import textwrap
from pathlib import Path
from unittest.mock import Mock

import pytest
from mkdocs.structure.files import File
from mkdocs.structure.pages import Page

from neoteroi.mkdocs.contribs import ContribsPlugin
from neoteroi.mkdocs.contribs.domain import ContributionsReader, Contributor
from neoteroi.mkdocs.contribs.git import GitContributionsReader
from neoteroi.mkdocs.contribs.txt import TXTContributionsReader
from tests import get_resource_file_path


@pytest.mark.parametrize(
    "value,expected_result",
    [
        [
            "     2\tRoberto Prevato <roberto.prevato@example.com>\n",
            [Contributor("Roberto Prevato", "roberto.prevato@example.com", 2)],
        ],
        [
            "     2\tRoberto Prevato (RP) <roberto.prevato@example.com>\n",
            [Contributor("Roberto Prevato (RP)", "roberto.prevato@example.com", 2)],
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


def _get_contribs_config():
    return {
        "contributors_label": "Contributors",
        "last_modified_label": "Last modified on",
        "show_last_modified_time": True,
        "show_contributors_title": False,
        "time_format": "%Y-%m-%d %H:%M:%S",
    }


def test_contribs_plugin_success():
    """
    Tests a successful scenario.
    """
    handler = ContribsPlugin()
    handler.config = _get_contribs_config()

    example = textwrap.dedent(
        """
        # Hello World!

        Lorem ipsum dolor sit amet.

        """.strip(
            "\n"
        )
    )

    result = handler.on_page_markdown(
        example,
        page=Page(
            "Example",
            File(
                path="res/contribs-01.html",
                src_dir="tests/res",
                dest_dir="tests",
                use_directory_urls=True,
            ),
            {},
        ),
    )

    assert result is not None
    assert (
        result
        == """# Hello World!

Lorem ipsum dolor sit amet.



<div class="nt-contribs"><p class="nt-mod-time">Last modified on: 2022-10-04 21"""
        + """:01:05</p><div class="nt-contributors"><div class="nt-contributor """
        + """nt-group-0" title="Charlie Brown &lt;charlie.brown@example.org&gt;"""
        + """ (1)"><span class="nt-initials">CB</span></div><div class="nt-cont"""
        + """ributor nt-group-1" title="Sally Brown (SB) &lt;sally.brown@exampl"""
        + """e.org&gt; (1)"><span class="nt-initials">SB</span></div></div></di"""
        + """v>"""
    )


def test_contribs_plugin_new_file_ignore():
    """
    Tests the scenario of a new file that is created while developing and is not
    committed, yet.
    """
    handler = ContribsPlugin()
    handler.config = _get_contribs_config()

    example = textwrap.dedent(
        """
        # Hello World!

        Lorem ipsum dolor sit amet.

        """.strip(
            "\n"
        )
    )

    with open("docs/res/contribs-new.html", mode="wt", encoding="utf8") as new_file:
        new_file.write(example)

    result = handler.on_page_markdown(
        example,
        page=Page(
            "Example",
            File(
                path="res/contribs-new.html",
                src_dir="tests/res",
                dest_dir="tests",
                use_directory_urls=True,
            ),
            {},
        ),
    )

    assert result is not None
    assert result == example


def test_txt_reader_contributors():
    reader = TXTContributionsReader()
    contributors = reader.get_contributors(Path(get_resource_file_path("example.md")))

    assert contributors == [
        Contributor("Charlie Brown", "charlie.brown@peanuts.com", 3),
        Contributor("Sally Brown", "sally.brown@peanuts.com", 1),
    ]


def test_txt_reader_last_modified_time():
    reader = TXTContributionsReader()
    lmt = reader.get_last_modified_date(Path(get_resource_file_path("example.md")))

    assert lmt is not None


def test_contributor_alt_names():
    """
    When the same person commits using the same email address but different names,
    Git returns two different contributors. In such scenario, it is desirable to merge
    two items into one.
    """
    plugin = ContribsPlugin()

    contributors = [
        Contributor("Charlie Brown", "charlie.brown@neoteroi.xyz", count=1),
        Contributor("Charlie Marrone", "charlie.brown@neoteroi.xyz", count=2),
    ]

    reader_mock = Mock(ContributionsReader)
    reader_mock.get_contributors.return_value = contributors

    file_mock = Mock(File)
    file_mock.src_path = Path("foo.txt")
    plugin._contribs_reader = reader_mock
    result = plugin._get_contributors(file_mock)

    assert result == contributors

    # setting
    plugin.config = {
        "contributors": [
            {"email": "charlie.brown@neoteroi.xyz", "name": "Charlie Brown"}
        ]
    }

    result = plugin._get_contributors(file_mock)

    assert result == [
        Contributor("Charlie Brown", "charlie.brown@neoteroi.xyz", count=3),
    ]
