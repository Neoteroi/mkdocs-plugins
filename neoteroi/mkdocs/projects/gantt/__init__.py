"""
This module provides a control to render Gantt diagrams.

neoteroi.gantt

MIT License
Copyright (c) 2022 to present, Roberto Prevato
"""

from neoteroi.mkdocs.markdown.processors import (
    EmbeddedBlockProcessor,
    SourceBlockProcessor,
)
from neoteroi.mkdocs.markdown.utils import create_instance

from ..domain import Plan
from .html import GanttHTMLBuilder, GanttViewOptions


class BaseGanttProcessor:
    @property
    def name(self) -> str:
        return "gantt"

    def build_html(self, parent, obj, props) -> None:
        """Builds the HTML for the given input object."""
        if not isinstance(obj, (dict, list)):
            raise TypeError("Expected a list of items describing Gantt.")

        builder = GanttHTMLBuilder(
            Plan.from_obj(obj), create_instance(GanttViewOptions, props)
        )
        builder.build_html(parent)


class GanttEmbeddedProcessor(BaseGanttProcessor, EmbeddedBlockProcessor):
    """
    Block processor that can render a Gantt diagram using data embedded in the Markdown.
    """


class GanttSourceProcessor(BaseGanttProcessor, SourceBlockProcessor):
    """
    Block processor that can render a Gantt diagram using data from a source outside of
    the Markdown (e.g. file, URL, database).
    """


def register_extension(md, priority):
    md.parser.blockprocessors.register(
        GanttEmbeddedProcessor(md.parser), "gantt", priority + 0.1
    )

    md.parser.blockprocessors.register(
        GanttSourceProcessor(md.parser), "gantt-from-source", priority
    )
