"""
This module provides an extension to support Markdown tables with colspan and rowspan.

neoteroi.Timeline

MIT License

Copyright (c) 2022 to present, Roberto Prevato
"""
from markdown import Extension

from neoteroi.markdown.processors import BaseBlockProcessor, SourceInlineProcessor

from .domain import Timeline, TimelineItem
from .html import TimelineHTMLBuilder, aligment_from_props


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
                [TimelineItem(**item) for item in obj],
                align=aligment_from_props(props),
                alternate=props.get("alternate", False),
            ),
        )


class TimelineProcessor(BaseTimelineProcessor, BaseBlockProcessor):
    """"""


class TimelineInlineProcessor(BaseTimelineProcessor, SourceInlineProcessor):
    """"""


class TimelineExtension(Extension):
    """Extension that includes timelines."""

    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.parser.blockprocessors.register(
            TimelineProcessor(md.parser), "Timeline", 106
        )

        md.inlinePatterns.register(
            TimelineInlineProcessor(md),
            "InlineTimelineProcessor",
            15,
        )


def make_extension(*args, **kwargs):
    return TimelineExtension(*args, **kwargs)
