"""
This module provides an extension to support Markdown tables with colspan and rowspan.

neoteroi.spantable

MIT License
Copyright (c) 2022 to present, Roberto Prevato
"""

import logging
import re
import xml.etree.ElementTree as etree
from typing import Dict, Optional

from markdown import Extension
from markdown.blockprocessors import BlockProcessor

from neoteroi.mkdocs.markdown import parse_props
from neoteroi.mkdocs.markdown.tables import read_table
from neoteroi.mkdocs.markdown.tables.spantable import Cell, SpanTable

logger = logging.getLogger("MARKDOWN")


class SpanTableProcessor(BlockProcessor):
    START_RE = re.compile(r"""(?P<indent>\s*)::spantable::[\w\s]*""", re.DOTALL)

    END_RE = re.compile(r"\s*:{2}end-spantable:{2}\s*\n?")

    def test(self, parent, block):
        if self.START_RE.search(block):
            return True
        else:
            return False

    def find_closing_fragment_index(self, blocks) -> int:
        for index, block in enumerate(blocks):
            if self.END_RE.search(block):
                return index
        return -1

    def pop_to_index(self, items, index):
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

    def read_first_table(self, blocks) -> Optional[SpanTable]:
        """
        Reads the first table in the given blocks, returning it.
        If a block does not contain a table, it is ignored.
        """
        for block in blocks:
            table = read_table(block, SpanTable)

            if table is not None:
                return table

    def run(self, parent, blocks):
        """
        Converts Markdown code to an HTML table, injecting it to the given parent.
        """
        closing_block_index = self.find_closing_fragment_index(blocks)

        if closing_block_index == -1:
            # unclosed tag, ignore
            logger.warning(
                "Unclosed ::spantable:: block - expected a ::end-spantable::."
            )
            return False

        props = parse_props(blocks[0])

        table_blocks = list(self.pop_to_index(blocks, closing_block_index))
        span_table = self.read_first_table(table_blocks)
        assert span_table is not None, "A table is expected if test() -> True"

        div = etree.SubElement(parent, "div", {"class": "span-table-wrapper"})
        table = etree.SubElement(div, "table", self._get_table_props(props))

        self._handle_caption(table, props)
        self._set_table(span_table, table)

    def _handle_caption(self, table_element: etree.Element, props: Dict[str, str]):
        caption = props.get("caption")
        if caption:
            caption_el = etree.SubElement(table_element, "caption", {})
            caption_el.text = caption

    def _get_table_props(self, props):
        data = {"class": "span-table"}

        html_class = props.get("class")
        if html_class:
            data["class"] = f"span-table {html_class}"

        return data

    def _set_table(self, span_table: SpanTable, table_element: etree.Element):
        for row in span_table.matrix.rows:
            tr = etree.SubElement(table_element, "tr")

            for cell in row:
                assert isinstance(cell, Cell)
                if cell.skip:
                    continue
                props = {}

                if cell.html_class:
                    props["class"] = cell.html_class

                if cell.col_span > 1:
                    props["colspan"] = str(cell.col_span)

                if cell.row_span > 1:
                    props["rowspan"] = str(cell.row_span)

                td = etree.SubElement(tr, "td", props)
                td.text = cell.text


class SpanTableExtension(Extension):
    """Extension that includes SpanTables (tables supporting rowspan and colspan)."""

    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.parser.blockprocessors.register(
            SpanTableProcessor(md.parser), "spantable", 106
        )


def make_extension(*args, **kwargs):
    return SpanTableExtension(*args, **kwargs)
