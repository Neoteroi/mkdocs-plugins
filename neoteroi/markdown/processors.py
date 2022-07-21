"""
This module defines common classes used in the package to implement BlockProcessor
types. It defines a common class to handle a notation like:

[example(content)]

and

::example:: prop_1="value_1" prop_2="value_2" ...
content
::/example::
"""

import logging
import re
import textwrap
import xml.etree.ElementTree as etree
from abc import ABC, abstractmethod
from typing import Iterable, List, Optional

from markdown.blockprocessors import BlockProcessor
from markdown.inlinepatterns import InlineProcessor

from neoteroi.markdown import parse_props
from neoteroi.markdown.data.text import (
    DEFAULT_PARSERS,
    CSVParser,
    JSONParser,
    TextParser,
    YAMLParser,
    try_parse_text,
)

logger = logging.getLogger("MARKDOWN")


def _find_closing_fragment_index(pattern: re.Pattern, blocks: List[str]) -> int:
    for index, block in enumerate(blocks):
        if pattern.search(block):
            return index
    return -1


def pop_to_index(items, index):
    """
    Pops elements from a source list, and yields them up to the given index,
    included.

    Example:
    pop_to_index([1, 2, 3, 4], 2) -> yields 1, 2, 3,
    removing them from the source list.
    """
    i = 0

    while i <= index:
        block = items.pop(0)
        yield block + "\n"
        i += 1


class NeoteroiInlineProcessor(InlineProcessor):
    """
    Common inline processor that reads information from a file or URL source and handles
    it to create an HTML element.
    """

    def get_data_from_source(self, value: str):
        ...

    def handleMatch(self, m, data):
        import xml.etree.ElementTree as etree

        value = m.group(1)

        el = etree.Element("div")
        el.text = m.group(1) + " FUUUU!"
        return el, m.start(0), m.end(0)


class SourceOnlyProcessor(BlockProcessor, ABC):
    """
    A processor that handles a fragment like:

    [example(...)]
    """

    _pattern: Optional[re.Pattern] = None

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the tag that will be handled by this processor."""

    @property
    def pattern(self) -> re.Pattern:
        if self._pattern is None:
            self._pattern = re.compile(rf"\[{self.name}\(([^\)]+)\)\]")
        return self._pattern

    def find_closing_fragment_index(self, blocks) -> int:
        return _find_closing_fragment_index(self.pattern, blocks)

    def test(self, parent, block) -> bool:
        if self.pattern.search(block):
            return True
        else:
            return False

    def run(self, parent, blocks):
        closing_block_index = self.find_closing_fragment_index(blocks)

        if closing_block_index == -1:
            # unclosed tag, ignore
            logger.warning(
                f"Unclosed ::{self.name}:: block - expected a ::/{self.name}::."
            )
            return False

        relevant_blocks = list(pop_to_index(blocks, closing_block_index))
        print(relevant_blocks)
        import xml.etree.ElementTree as etree

        etree.SubElement(parent, "div", {"class": "ug-timeline"})


class BaseBlockProcessor(BlockProcessor, ABC):
    """
    Base class for standard block processors that handle a fragment like:

    ::example:: format prop_1="value_1" prop_2="value_2" ...
    [CSV | JSON | YAML]
    ::/example::

    This class provides base functions to handle the Markdown integration and parsing of
    the input, concrete classes define how to build the HTML once the input has been
    parsed.
    """

    _start_pattern: Optional[re.Pattern] = None
    _end_pattern: Optional[re.Pattern] = None

    parsers: Iterable[TextParser] = DEFAULT_PARSERS

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the tag that will be handled by this processor."""

    @abstractmethod
    def build_html(self, parent, obj, props) -> None:
        """Builds the HTML for the given input object."""

    @property
    def start_pattern(self) -> re.Pattern:
        if self._start_pattern is None:
            self._start_pattern = re.compile(
                rf"""(?P<indent>\s*)::{self.name}::([^\s]*)""", re.DOTALL
            )
        return self._start_pattern

    @property
    def end_pattern(self) -> re.Pattern:
        if self._end_pattern is None:
            self._end_pattern = re.compile(rf"\s*::/{self.name}::\s*\n?")
        return self._end_pattern

    def test(self, parent, block) -> bool:
        if self.start_pattern.search(block):
            return True
        else:
            return False

    def get_parsers(self, props):
        """
        Tries to get the best parser by tag property.
        """
        if props.get("yaml") is True:
            return [YAMLParser()]

        if props.get("json") is True:
            return [JSONParser()]

        if props.get("csv") is True:
            return [CSVParser()]

        return self.parsers

    def find_closing_fragment_index(self, blocks) -> int:
        return _find_closing_fragment_index(self.end_pattern, blocks)

    def parse(self, text, props):
        return try_parse_text(text, self.get_parsers(props))

    def get_content(self, relevant_blocks):
        raw_text = textwrap.dedent("".join(relevant_blocks))
        return self.end_pattern.sub("", self.start_pattern.sub("", raw_text))

    def run(self, parent, blocks):
        closing_block_index = self.find_closing_fragment_index(blocks)

        if closing_block_index == -1:
            # unclosed tag, ignore
            logger.warning(
                f"Unclosed ::{self.name}:: block - expected a ::end-{self.name}::."
            )
            return False

        # TODO: gestire blocchi senza \n
        props = parse_props(self.start_pattern.sub("", blocks[0]), bool_attrs=True)

        blocks.pop(0)
        raw_text = self.get_content(pop_to_index(blocks, closing_block_index - 1))

        try:
            obj = self.parse(raw_text, props)
        except ValueError:
            logger.exception("Could not parse the value of a %s block.", self.name)
            self._render_courtesy_error(parent)
        else:
            self.build_html(parent, obj, props)

    def _render_courtesy_error(self, parent):
        div = etree.SubElement(parent, "div", {"class": "ug-error"})
        p = etree.SubElement(div, "p", {"class": "ug-error"})
        p.text = (
            f"Could not parse the value of this {self.name} block. "
            "Please correct the input."
        )
