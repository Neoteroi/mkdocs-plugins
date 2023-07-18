import logging
import xml.etree.ElementTree as etree
from dataclasses import dataclass

from neoteroi.mkdocs.markdown.images import build_icon_html, build_image_html

from .domain import CardItem, Cards

logger = logging.getLogger("MARKDOWN")


@dataclass
class CardsViewOptions:
    id: str = ""
    class_name: str = ""
    cols: int = 3
    image_bg: bool = False
    blank_target: bool = False

    def __post_init__(self):
        if isinstance(self.cols, str):
            self.cols = int(self.cols)


class CardsHTMLBuilder:
    def __init__(self, options: CardsViewOptions) -> None:
        self.options = options

    @property
    def use_image_tags(self) -> bool:
        return not self.options.image_bg

    def get_item_props(self, item: CardItem):
        if item.key:
            item_props = {"class": f"nt-card {item.key}"}
        else:
            item_props = {"class": "nt-card"}

        return item_props

    def _get_root_class(self):
        base_class = f"nt-cards nt-grid cols-{self.options.cols}"

        if self.options.class_name:
            return base_class + " " + self.options.class_name
        return base_class

    def _get_link_properties(self, item: CardItem):
        assert item.url is not None
        props = {"href": item.url}

        if self.options.blank_target:
            props.update(target="_blank", rel="noopener")
        return props

    def build_html(self, parent, cards: Cards):
        root_element = etree.SubElement(
            parent, "div", {"class": self._get_root_class()}
        )

        for item in cards.items:
            self.build_item_html(root_element, item)

    def build_item_html(self, parent, item: CardItem):
        item_element = etree.SubElement(parent, "div", self.get_item_props(item))

        if item.url:
            first_child = etree.SubElement(
                item_element, "a", self._get_link_properties(item)
            )
        else:
            first_child = etree.SubElement(
                item_element, "div", {"class": "nt-card-wrap"}
            )

        wrapper_element = etree.SubElement(first_child, "div", {})

        if item.image:
            self.build_image_html(wrapper_element, item)
        elif item.icon:
            build_icon_html(
                etree.SubElement(wrapper_element, "div", {"class": "nt-card-icon"}),
                item.icon,
            )

        text_wrapper = etree.SubElement(
            wrapper_element, "div", {"class": "nt-card-content"}
        )

        title_element = etree.SubElement(text_wrapper, "p", {"class": "nt-card-title"})
        title_element.text = item.title

        if item.content:
            content_element = etree.SubElement(
                text_wrapper, "p", {"class": "nt-card-text"}
            )
            content_element.text = item.content

    def build_image_html(self, wrapper_element, item: CardItem):
        if not item.image:
            return

        if self.use_image_tags:
            build_image_html(
                etree.SubElement(
                    wrapper_element, "div", {"class": "nt-card-image tags"}
                ),
                item.image,
            )
        else:
            etree.SubElement(
                wrapper_element,
                "div",
                {
                    "class": "nt-card-image",
                    "style": f"background-image: url('{item.image.url}')",
                },
            )
