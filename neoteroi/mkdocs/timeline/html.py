import logging
import xml.etree.ElementTree as etree
from dataclasses import dataclass

from neoteroi.mkdocs.markdown.align import Alignment
from neoteroi.mkdocs.markdown.images import build_icon_html

from .domain import Timeline, TimelineItem

logger = logging.getLogger("MARKDOWN")


@dataclass
class TimelineViewOptions:
    id: str = ""
    class_name: str = ""
    alternate: bool = False
    align: Alignment = Alignment.LEFT
    headings: bool = False


class TimelineHTMLBuilder:
    def __init__(self, options: TimelineViewOptions) -> None:
        self.options = options

    def get_class(self) -> str:
        return (
            "nt-timeline vertical "
            + self.options.align.value
            + (" alternate" if self.options.alternate else "")
            + (f" {self.options.class_name}" if self.options.class_name else "")
        )

    def get_dot_class(self, item: TimelineItem) -> str:
        return "nt-timeline-dot " + (item.key or "") + (" bigger" if item.icon else "")

    def build_html(self, parent, timeline: Timeline):
        root_props = {"class": self.get_class()}
        if self.options.id:
            root_props["id"] = self.options.id

        root_element = etree.SubElement(parent, "div", root_props)
        etree.SubElement(root_element, "div", {"class": "nt-timeline-before"})

        items_element = etree.SubElement(
            root_element, "div", {"class": "nt-timeline-items"}
        )

        for item in timeline.items:
            self.build_item_html(items_element, item)

        etree.SubElement(root_element, "div", {"class": "nt-timeline-after"})

    def build_icon_html(self, parent, item: TimelineItem):
        build_icon_html(parent, item.icon)

    def build_item_html(self, parent, item: TimelineItem):
        item_element = etree.SubElement(
            parent,
            "div",
            {"class": "nt-timeline-item" + (f" {item.key}" if item.key else "")},
        )

        title_element = etree.SubElement(
            item_element,
            "h3" if self.options.headings else "p",
            {"class": "nt-timeline-title"},
        )
        title_element.text = item.title

        if item.sub_title:
            sub_title_element = etree.SubElement(
                item_element, "span", {"class": "nt-timeline-sub-title"}
            )
            sub_title_element.text = item.sub_title

        if item.content:
            content_element = etree.SubElement(
                item_element, "p", {"class": "nt-timeline-content"}
            )
            content_element.text = item.content

        dot_element = etree.SubElement(
            item_element, "div", {"class": self.get_dot_class(item)}
        )

        self.build_icon_html(dot_element, item)
