"""
This module provides an implementation of cards.

neoteroi.cards

MIT License
Copyright (c) 2022 to present, Roberto Prevato
"""
from markdown import Extension

from neoteroi.markdown.images import Image
from neoteroi.markdown.processors import EmbeddedBlockProcessor, SourceBlockProcessor
from neoteroi.markdown.utils import create_instance, create_instances

from .domain import CardItem, Cards
from .html import CardsHTMLBuilder


class BaseCardsProcessor:
    @property
    def name(self) -> str:
        return "cards"

    def norm_obj(self, obj):
        for item in obj:
            if "image" in item:
                item["image"] = create_instance(Image, item["image"])

    def build_html(self, parent, obj, props) -> None:
        """Builds the HTML for the given input object."""
        if not isinstance(obj, list):
            raise TypeError("Expected a list of items describing timeline parts.")

        self.norm_obj(obj)
        builder = CardsHTMLBuilder()
        builder.build_html(parent, Cards(create_instances(CardItem, obj)))


class CardsEmbeddedProcessor(BaseCardsProcessor, EmbeddedBlockProcessor):
    """
    Block processor that can render a timeline using data embedded in the Markdown.
    """


class CardsSourceProcessor(BaseCardsProcessor, SourceBlockProcessor):
    """
    Block processor that can render a timeline using data from a source outside of the
    Markdown (e.g. file, URL, database).
    """


class CardsExtension(Extension):
    """Extension that includes cards."""

    config = {
        "priority": [12, "The priority to be configured for the extension."],
    }

    def extendMarkdown(self, md):
        md.registerExtension(self)
        priority = self.getConfig("priority")

        md.parser.blockprocessors.register(
            CardsEmbeddedProcessor(md.parser), "cards", priority + 0.1
        )

        md.parser.blockprocessors.register(
            CardsSourceProcessor(md.parser), "cards-from-source", priority
        )


def make_extension(*args, **kwargs):
    return CardsExtension(*args, **kwargs)
