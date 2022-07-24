"""
This module provides an extension to support Markdown tables with colspan and rowspan.

neoteroi.timeline

MIT License
Copyright (c) 2022 to present, Roberto Prevato
"""
from markdown import Extension

from neoteroi.markdown.align import aligment_from_props
from neoteroi.markdown.processors import EmbeddedBlockProcessor, SourceBlockProcessor
from neoteroi.markdown.utils import create_instances

from .domain import Timeline, TimelineItem
from .html import TimelineHTMLBuilder


class BaseTimelineProcessor:
    @property
    def name(self) -> str:
        return "timeline"

    def build_html(self, parent, obj, props) -> None:
        """Builds the HTML for the given input object."""
        if not isinstance(obj, list):
            raise TypeError("Expected a list of items describing timeline parts.")

        builder = TimelineHTMLBuilder()
        builder.build_html(
            parent,
            Timeline(
                create_instances(TimelineItem, obj),
                align=aligment_from_props(props),
                alternate=props.get("alternate", False),
            ),
        )


class TimelineEmbeddedProcessor(BaseTimelineProcessor, EmbeddedBlockProcessor):
    """
    Block processor that can render a timeline using data embedded in the Markdown.
    """


class TimelineSourceProcessor(BaseTimelineProcessor, SourceBlockProcessor):
    """
    Block processor that can render a timeline using data from a source outside of the
    Markdown (e.g. file, URL, database).
    """


class TimelineExtension(Extension):
    """Extension that includes timelines."""

    config = {
        "priority": [12, "The priority to be configured for the extension."],
    }

    def extendMarkdown(self, md):
        md.registerExtension(self)
        priority = self.getConfig("priority")

        md.parser.blockprocessors.register(
            TimelineEmbeddedProcessor(md.parser), "timeline", priority + 0.1
        )

        md.parser.blockprocessors.register(
            TimelineSourceProcessor(md.parser), "timeline-from-source", priority
        )


def make_extension(*args, **kwargs):
    return TimelineExtension(*args, **kwargs)
