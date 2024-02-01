"""
This module provides an implementation of cards.

neoteroi.cards

MIT License
Copyright (c) 2022 to present, Roberto Prevato
"""

from markdown import Extension

from neoteroi.mkdocs.markdown.images import Image
from neoteroi.mkdocs.markdown.processors import (
    EmbeddedBlockProcessor,
    SourceBlockProcessor,
)
from neoteroi.mkdocs.markdown.utils import create_instance, create_instances

from .domain import CardItem, Cards
from .html import CardsHTMLBuilder, CardsViewOptions


class BaseCardsProcessor:
    @property
    def name(self) -> str:
        return "cards"

    def norm_obj(self, obj):
        for item in obj:
            if "image" in item:
                item["image"] = Image.from_obj(item["image"])

    def build_html(self, parent, obj, props) -> None:
        """Builds the HTML for the given input object."""
        if not isinstance(obj, list):
            raise TypeError("Expected a list of items describing cards.")

        if self.root_config:
            new_props = dict(**self.root_config)
            new_props.update(props)
            props = new_props

        self.norm_obj(obj)
        builder = CardsHTMLBuilder(create_instance(CardsViewOptions, props))
        builder.build_html(parent, Cards(create_instances(CardItem, obj)))


class CardsEmbeddedProcessor(BaseCardsProcessor, EmbeddedBlockProcessor):
    """
    Block processor that can render cards using data embedded in the Markdown.
    """


class CardsSourceProcessor(BaseCardsProcessor, SourceBlockProcessor):
    """
    Block processor that can render cards using data from a source outside of the
    Markdown (e.g. file, URL, database).
    """


class CardsExtension(Extension):
    """Extension that includes cards."""

    def __init__(self, *args, **kwargs):
        self.config = {
            "priority": [12, "The priority to be configured for the extension."],
            "blank_target": [False, 'Whether to generate links with target="_blank"'],
        }
        super().__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        md.registerExtension(self)
        priority = self.getConfig("priority")

        configs = self.getConfigs()
        del configs["priority"]

        md.parser.blockprocessors.register(
            CardsEmbeddedProcessor(md.parser).with_root_config(configs),
            "cards",
            priority + 0.1,
        )

        md.parser.blockprocessors.register(
            CardsSourceProcessor(md.parser).with_root_config(configs),
            "cards-from-source",
            priority,
        )
