import logging
import xml.etree.ElementTree as etree

from .domain import Timeline, TimelineItem

logger = logging.getLogger("MARKDOWN")


class TimelineHTMLBuilder:
    def get_class(self, timeline: Timeline) -> str:
        return (
            "nt-timeline vertical "
            + timeline.align.value
            + (" alternate" if timeline.alternate else "")
        )

    def get_dot_class(self, item: TimelineItem) -> str:
        return "nt-timeline-dot " + (item.key or "") + (" bigger" if item.icon else "")

    def build_html(self, parent, timeline: Timeline):
        root_element = etree.SubElement(
            parent, "div", {"class": self.get_class(timeline)}
        )
        etree.SubElement(root_element, "div", {"class": "nt-timeline-before"})

        items_element = etree.SubElement(
            root_element, "div", {"class": "nt-timeline-items"}
        )

        for item in timeline.items:
            self.build_item_html(items_element, item)

        etree.SubElement(root_element, "div", {"class": "nt-timeline-after"})

    def build_item_html(self, parent, item: TimelineItem):
        item_element = etree.SubElement(
            parent,
            "div",
            {"class": "nt-timeline-item" + (f" {item.key}" if item.key else "")},
        )

        title_element = etree.SubElement(
            item_element, "h3", {"class": "nt-timeline-title"}
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

        icon_element = etree.SubElement(
            item_element, "div", {"class": self.get_dot_class(item)}
        )

        if item.icon:
            etree.SubElement(icon_element, "i", {"class": f"{item.icon} icon"})
