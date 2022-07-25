import logging
import xml.etree.ElementTree as etree

from neoteroi.markdown.images import build_image_html

from .domain import CardItem, Cards

logger = logging.getLogger("MARKDOWN")


class CardsHTMLBuilder:
    def build_html(self, parent, cards: Cards):
        root_element = etree.SubElement(parent, "div", {"class": "nt-cards"})

        for item in cards.items:
            self.build_item_html(root_element, item)

    def build_item_html(self, parent, item: CardItem):
        root_element = etree.SubElement(parent, "div", {"class": "nt-card"})

        if item.url:
            first_child = etree.SubElement(root_element, "a", {"href": item.url})
        else:
            raise NotImplementedError()

        wrapper_element = etree.SubElement(first_child, "div", {})

        if item.image:
            build_image_html(
                etree.SubElement(wrapper_element, "div", {"class": "nt-card-image"}),
                item.image,
            )

        title_element = etree.SubElement(
            wrapper_element, "p", {"class": "nt-card-title"}
        )
        title_element.text = item.title

        if item.content:
            content_element = etree.SubElement(
                wrapper_element, "p", {"class": "nt-card-content"}
            )
            content_element.text = item.content
