"""
This module defines common processor classes used in the package. It defines classes to
handle common notations like:

[example(pros?)(content-source)]

and

::example:: (props?) ...
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

from neoteroi.mkdocs.markdown import parse_props
from neoteroi.mkdocs.markdown.data.files import FileReader
from neoteroi.mkdocs.markdown.data.source import DataReader
from neoteroi.mkdocs.markdown.data.text import (
    CSVParser,
    JSONParser,
    TextParser,
    YAMLParser,
)
from neoteroi.mkdocs.markdown.data.web import HTTPDataReader

logger = logging.getLogger("MARKDOWN")


def find_closing_fragment_index(pattern: re.Pattern, blocks: List[str]) -> int:
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


class BaseProcessor(ABC):
    root_config: dict = {}
    parsers: Iterable[TextParser] = (YAMLParser(), JSONParser(), CSVParser())

    @property
    @abstractmethod
    def name(self) -> str:
        """Returns the name of the tag that will be handled by this processor."""

    @abstractmethod
    def build_html(self, parent, obj, props) -> None:
        """Builds the HTML for the given input object."""

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

    def render_courtesy_error(self, parent, message: str):
        div = etree.SubElement(parent, "div", {"class": "nt-error"})
        p = etree.SubElement(div, "p")
        p.text = message

    def parse(self, text, props):
        for parser in self.get_parsers(props):
            try:
                return parser.parse(text)
            except (TypeError, ValueError) as parser_exc:
                logger.debug(
                    "The parser %s failed to parse the text.",
                    type(parser).__qualname__,
                    exc_info=parser_exc,
                )

        raise ValueError("The input text could not be parsed.")

    def render(self, parent, data, props):
        if isinstance(data, str):
            try:
                obj = self.parse(data, props)
            except ValueError:
                logger.exception("Could not parse the value of a %s block.", self.name)
                self.render_courtesy_error(
                    parent,
                    f"Could not parse the value of this {self.name} block. "
                    "Please correct the input.",
                )
                return
        else:
            obj = data

        try:
            self.build_html(parent, obj, props)
        except (ValueError, TypeError):
            logger.exception("Could not render a %s block.", self.name)
            self.render_courtesy_error(
                parent,
                f"Could not render a {self.name} block. Please correct the input.",
            )

    def get_match(self, pattern, blocks) -> Optional[re.Match]:
        first_block = blocks.pop(0)
        new_lines = []
        match = None

        for line in first_block.splitlines():
            match = pattern.match(line)
            if match:
                break
            else:
                new_lines.append(line)
        if new_lines:
            blocks.insert(0, "\n".join(new_lines))

        return match

    def with_root_config(self, props):
        self.__dict__["root_config"] = props
        return self


class SourceBlockProcessor(BlockProcessor, BaseProcessor):
    """
    Base class for inline processors that read information from a file or URL source
    and handle it to create an HTML element, like:

    [timeline(./example.yaml)]

    [timeline(https://.../example.json)]
    """

    _pattern: Optional[re.Pattern] = None

    @property
    def pattern(self) -> re.Pattern:
        if self._pattern is None:
            self._pattern = re.compile(
                rf"(?P<indent>\s*)\[{self.name}\s?([^\(]*)\((.*?)\)\]", re.DOTALL
            )
        return self._pattern

    def test(self, parent, block) -> bool:
        if self.pattern.search(block):
            return True
        else:
            return False

    data_readers: Iterable[DataReader] = (FileReader(), HTTPDataReader())

    def get_data_reader(self, source: str) -> DataReader:
        if not source:
            raise ValueError("Missing source parameter.")

        for reader in self.data_readers:
            if reader.test(source):
                return reader

        logger.warning("[%s] could not resolve the source: %s", self.name, source)
        raise ValueError(
            f'[{self.name}] invalid source. The source "{source}" could not be '
            "resolved. If the source is a file, please verify the path."
        )

    def read_from_source(self, source: str):
        reader = self.get_data_reader(source)
        return reader.read(source)

    def run(self, parent, blocks):
        match = self.get_match(self.pattern, blocks)
        assert match is not None

        groups = match.groups()
        raw_props = groups[1]
        source = groups[2]

        if raw_props:
            props = parse_props(raw_props, bool_attrs=True)
        else:
            props = {}

        props["__source"] = source

        try:
            data = self.read_from_source(source)
        except ValueError as value_error:
            self.render_courtesy_error(parent, str(value_error))
        else:
            self.render(parent, data, props)


class EmbeddedBlockProcessor(BlockProcessor, BaseProcessor):
    """
    Base class for standard block processors that handle a fragment like:

    ::example:: format prop_1="value_1" prop_2="value_2" ...
    [CSV | JSON | YAML]
    ::/example::

    This class provides base functions to handle the Markdown integration and parsing of
    the input, concrete classes define how to build the HTML once the input has been
    parsed.

    The source of data in this case is always coming as a string.
    """

    _start_pattern: Optional[re.Pattern] = None
    _end_pattern: Optional[re.Pattern] = None

    @property
    def start_pattern(self) -> re.Pattern:
        if self._start_pattern is None:
            self._start_pattern = re.compile(
                rf"""(?P<indent>\s*)::{self.name}::([^\n]*)?""", re.DOTALL
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

    def find_closing_fragment_index(self, blocks) -> int:
        return find_closing_fragment_index(self.end_pattern, blocks)

    def get_content(self, relevant_blocks):
        raw_text = textwrap.dedent("".join(relevant_blocks))
        return self.end_pattern.sub("", self.start_pattern.sub("", raw_text))

    def run(self, parent, blocks):
        closing_block_index = self.find_closing_fragment_index(blocks)

        if closing_block_index == -1:
            # unclosed tag, ignore
            logger.warning(
                f"Unclosed ::{self.name}:: block - expected a ::/{self.name}:: block."
            )
            return False
        match = self.start_pattern.match(blocks[0])

        assert match is not None, "A match here is expected"

        props = parse_props(
            match.group(0).lstrip().replace(f"::{self.name}::", ""), bool_attrs=True
        )

        if closing_block_index == 0:
            # there is no carriage return, which is not ideal for
            # what we want to achieve
            single_block = blocks[0].lstrip()
            raw_text = textwrap.dedent(
                self.end_pattern.sub("", self.start_pattern.sub("", single_block))
            ).lstrip()
            blocks.pop(0)
        else:
            blocks.pop(0)
            raw_text = self.get_content(pop_to_index(blocks, closing_block_index - 1))

        self.render(parent, raw_text, props)
