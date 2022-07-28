import logging
import xml.etree.ElementTree as etree

from neoteroi.markdown.images import build_image_html

from .domain import CardItem, Cards

logger = logging.getLogger("MARKDOWN")


class CardsHTMLBuilder:
    def __init__(self, props) -> None:
        self.props = props

    @property
    def use_image_tags(self) -> bool:
        return self.props.get("image-tags", False)

    def get_item_props(self, item: CardItem):
        if item.key:
            item_props = {"class": f"nt-card {item.key}"}
        else:
            item_props = {"class": "nt-card"}

        flex = self.props.get("flex")

        if flex:
            if flex.endswith("%"):
                flex = flex.rstrip("%")
            item_props["style"] = f"flex: {flex}%;"

        return item_props

    def build_html(self, parent, cards: Cards):
        root_element = etree.SubElement(parent, "div", {"class": "nt-cards"})

        for item in cards.items:
            self.build_item_html(root_element, item)

    def build_item_html(self, parent, item: CardItem):
        item_element = etree.SubElement(parent, "div", self.get_item_props(item))

        if item.url:
            first_child = etree.SubElement(item_element, "a", {"href": item.url})
        else:
            first_child = etree.SubElement(
                item_element, "div", {"class": "nt-card-wrap"}
            )

        wrapper_element = etree.SubElement(first_child, "div", {})

        self.build_image_html(wrapper_element, item)

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
