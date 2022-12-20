import pytest

from neoteroi.mkdocs.markdown import extract_props, parse_props
from neoteroi.mkdocs.markdown.tables import Table, read_table


def test_markdown_table():
    table = Table("A B C".split(), [["1", "2", "3"], ["4", "5", "6"]])

    assert table["A"] == ("1", "4")
    assert table["B"] == ("2", "5")
    assert table["C"] == ("3", "6")

    assert table[0] == tuple("1 2 3".split())
    assert table[1] == tuple("4 5 6".split())


def test_markdown_table_key_error():
    table = Table("A B C".split(), [["1", "2", "3"], ["4", "5", "6"]])

    with pytest.raises(KeyError):
        table["D"]


def test_markdown_table_index_error():
    table = Table("A B C".split(), [["1", "2", "3"], ["4", "5", "6"]])

    with pytest.raises(IndexError):
        table[4]


@pytest.mark.parametrize(
    "markdown,expected_result",
    [
        (
            """
            | A   | B   | C   | D   |
            | --- | --- | --- | --- |
            | 1   | 2   | 3   | 4   |
            | 5   | 6   | 7   | 8   |
            """,
            [
                {"A": "1", "B": "2", "C": "3", "D": "4"},
                {"A": "5", "B": "6", "C": "7", "D": "8"},
            ],
        ),
        (
            """
| Source                         | Example                                              |
| ------------------------------ | ---------------------------------------------------- |
| YAML file                      | `./docs/swagger.yaml`                                |
| JSON file                      | `./docs/swagger.json`                                |
| URL returning YAML on HTTP GET | `https://example-domain.net/swagger/v1/swagger.yaml` |
| URL returning JSON on HTTP GET | `https://example-domain.net/swagger/v1/swagger.json` |
            """,
            [
                {"Source": "YAML file", "Example": "`./docs/swagger.yaml`"},
                {"Source": "JSON file", "Example": "`./docs/swagger.json`"},
                {
                    "Source": "URL returning YAML on HTTP GET",
                    "Example": "`https://example-domain.net/swagger/v1/swagger.yaml`",
                },
                {
                    "Source": "URL returning JSON on HTTP GET",
                    "Example": "`https://example-domain.net/swagger/v1/swagger.json`",
                },
            ],
        ),
    ],
)
def test_read_table(markdown, expected_result):
    table = read_table(markdown)
    assert table is not None
    items = list(table.items())
    assert items == expected_result


@pytest.mark.parametrize(
    "value,expected_result",
    [
        ("", {}),
        ("Lorem ipsum dolor sit amet", {}),
        ("example foo='power'", {"foo": "power"}),
        ("example @foo='power'", {"@foo": "power"}),
        ("example\nfoo='power'", {"foo": "power"}),
        ('example foo="power"', {"foo": "power"}),
        (
            'example foo="power" style="color:red;"',
            {"foo": "power", "style": "color:red;"},
        ),
        (
            'example\n\nfoo="power"\nstyle="color:red;"',
            {"foo": "power", "style": "color:red;"},
        ),
    ],
)
def test_parse_props(value, expected_result):
    props = parse_props(value)
    assert props == expected_result


@pytest.mark.parametrize(
    "value,expected_result",
    [
        ("", {}),
        ("Lorem ipsum dolor sit amet", {}),
        ("example class='x' @foo='power'", {"foo": "power"}),
        ("example @foo='power'", {"foo": "power"}),
        ("example\n@foo='power'", {"foo": "power"}),
    ],
)
def test_parse_props_with_prefix(value, expected_result):
    props = parse_props(value, "@")
    assert props == expected_result


@pytest.mark.parametrize(
    "value,expected_result",
    [
        ("", ("", {})),
        ("Lorem ipsum dolor sit amet", ("Lorem ipsum dolor sit amet", {})),
        (
            "example class='x' @foo='power'",
            ("example", {"class": "x", "@foo": "power"}),
        ),
        ("lorem ipsum\n@foo='power'", ("lorem ipsum", {"@foo": "power"})),
    ],
)
def test_extract_props(value, expected_result):
    result = extract_props(value)
    assert result == expected_result
