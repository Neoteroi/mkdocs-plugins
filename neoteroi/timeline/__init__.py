"""
This module provides an extension to support Markdown tables with colspan and rowspan.

neoteroi.Timeline

MIT License

Copyright (c) 2022 to present Roberto Prevato
"""
import logging

from markdown import Extension, Markdown

from neoteroi.markdown.processors import (
    BaseBlockProcessor,
    NeoteroiInlineProcessor,
    SourceOnlyProcessor,
)

from .domain import Timeline, TimelineItem, TimelineAlignment
from .html import TimelineHTMLBuilder

logger = logging.getLogger("MARKDOWN")


class TimelineProcessor(BaseBlockProcessor):
    @property
    def name(self) -> str:
        return "timeline"

    def aligment_from_props(self, props):
        if props.get("center") is True:
            return TimelineAlignment.CENTER

        if props.get("left") is True:
            return TimelineAlignment.LEFT

        if props.get("right") is True:
            return TimelineAlignment.RIGHT

        return self.try_parse_position(props.get("align", "left"))

    def try_parse_position(self, align: str):
        try:
            return TimelineAlignment(align)
        except KeyError:
            logger.exception(
                "Invalid timeline align property: %s; ignoring this attribute", align
            )
            return TimelineAlignment.LEFT

    def build_html(self, parent, obj, props) -> None:
        """Builds the HTML for the given input object."""
        if not isinstance(obj, list):
            raise TypeError("Expected a list of items describing timeline parts.")

        builder = TimelineHTMLBuilder()
        builder.build_html(
            parent,
            Timeline(
                [TimelineItem(**item) for item in obj],
                align=self.aligment_from_props(props),
                alternate=props.get("alternate", False),
            ),
        )


class TimelineInlineProcessor(NeoteroiInlineProcessor):
    def __init__(self, md: Markdown) -> None:
        super().__init__(r"\[timeline(.*?)\]", md)


class TimelineFromSourceProcessor(SourceOnlyProcessor):
    @property
    def name(self) -> str:
        return "timeline"


class TimelineExtension(Extension):
    """Extension that includes timelines."""

    def extendMarkdown(self, md):
        md.registerExtension(self)

        md.parser.blockprocessors.register(
            TimelineProcessor(md.parser), "Timeline", 106
        )
        # md.parser.blockprocessors.register(
        #    TimelineFromSourceProcessor(md.parser), "TimelineFromSource", 107
        # )
        md.inlinePatterns.register(
            TimelineInlineProcessor(md),
            "InlineTimelineProcessor",
            15,
        )


def make_extension(*args, **kwargs):
    return TimelineExtension(*args, **kwargs)
