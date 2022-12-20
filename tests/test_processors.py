import re
import xml.etree.ElementTree as etree
from xml.etree.ElementTree import tostring as xml_to_str

import markdown
import pytest
from markdown.blockparser import BlockParser

from neoteroi.mkdocs.markdown.processors import (
    EmbeddedBlockProcessor,
    SourceBlockProcessor,
    find_closing_fragment_index,
)


class BaseMockProcessor:

    last_obj = None

    @property
    def name(self) -> str:
        return "mock"

    def build_html(self, parent, obj, props) -> None:
        if isinstance(obj, int):
            raise TypeError("Cannot accept int (crash test)")

        etree.SubElement(parent, "div", {"class": "nt-mock"})
        self.last_obj = obj


class MockSourceBlockProcessor(BaseMockProcessor, SourceBlockProcessor):
    pass


class MockEmbeddedProcessor(BaseMockProcessor, EmbeddedBlockProcessor):
    pass


class MockExtension(markdown.Extension):

    config = {
        "priority": [12, "The priority to be configured for the extension."],
    }

    def extendMarkdown(self, md):
        md.registerExtension(self)
        priority = self.getConfig("priority")

        md.parser.blockprocessors.register(
            MockEmbeddedProcessor(md.parser), "mock", priority + 0.1
        )

        md.parser.blockprocessors.register(
            MockSourceBlockProcessor(md.parser), "mock-from-source", priority
        )


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


def test_renders_courtesy_page_for_invalid_source():
    example = """
    [mock(./file-that-does-not-exist.json)]
    """

    html = markdown.markdown(example, extensions=[MockExtension(priority=100)])
    assert html == (
        '<div class="nt-error">\n<p>[mock] invalid source. The source '
        '"./file-that-does-not-exist.json" could not be resolved. '
        "If the source is a file, please verify the path.</p>\n</div>"
    )


def test_renders_courtesy_page_for_wrong_format():
    example = """
    ::mock:: json

    { not valid }

    ::/mock::
    """

    html = markdown.markdown(example, extensions=[MockExtension(priority=100)])
    assert html == (
        '<div class="nt-error">\n<p>Could not parse the value of this mock block. '
        "Please correct the input.</p>\n</div>"
    )


def test_does_nothing_with_unclosed_tag():
    example = """
    ::mock:: json

    { not valid }

    """

    html = markdown.markdown(example, extensions=[MockExtension(priority=100)])
    assert html == "<pre><code>::mock:: json\n\n{ not valid }\n</code></pre>"


def test_raises_for_missing_source():
    processor = MockSourceBlockProcessor(BlockParser(markdown.Markdown()))

    with pytest.raises(ValueError):
        processor.get_data_reader("")


def test_render_accepts_non_str():
    processor = MockSourceBlockProcessor(BlockParser(markdown.Markdown()))

    parent = etree.Element("div", {"class": "nt-mock"})
    data = []

    processor.render(parent, data, {})
    assert processor.last_obj is data


def test_render_handles_type_error():
    processor = MockSourceBlockProcessor(BlockParser(markdown.Markdown()))

    parent = etree.Element("div", {"class": "nt-mock"})
    processor.render(parent, -1, {})

    assert processor is not None
    html = xml_to_str(parent)
    assert html == (
        b'<div class="nt-mock"><div class="nt-error">'
        b"<p>Could not render a mock block. Please correct the input.</p></div></div>"
    )


def test_get_match():
    processor = MockSourceBlockProcessor(BlockParser(markdown.Markdown()))

    match = processor.get_match(processor.pattern, ["\n\n[mock(./foo.json)]", "\n"])
    assert match is not None
