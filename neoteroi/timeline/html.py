import logging
import xml.etree.ElementTree as etree

from .domain import Timeline, TimelineAlignment, TimelineItem

logger = logging.getLogger("MARKDOWN")


def aligment_from_props(props):
    if props.get("center") is True:
        return TimelineAlignment.CENTER

    if props.get("left") is True:
        return TimelineAlignment.LEFT

    if props.get("right") is True:
        return TimelineAlignment.RIGHT

    return try_parse_position(props.get("align", "left"))


def try_parse_position(align: str):
    try:
        return TimelineAlignment(align)
    except KeyError:
        logger.exception(
            "Invalid timeline align property: %s; ignoring this attribute", align
        )
        return TimelineAlignment.LEFT


class TimelineHTMLBuilder:
    def get_class(self, timeline: Timeline) -> str:
        return (
            "ug-timeline vertical "
            + timeline.align.value
            + (" alternate" if timeline.alternate else "")
        )

    def get_dot_class(self, item: TimelineItem) -> str:
        return "ug-timeline-dot " + (item.key or "") + (" bigger" if item.icon else "")

    def build_html(self, parent, timeline: Timeline):
        root_element = etree.SubElement(
            parent, "div", {"class": self.get_class(timeline)}
        )
        etree.SubElement(root_element, "div", {"class": "ug-timeline-before"})

        items_element = etree.SubElement(
            root_element, "div", {"class": "ug-timeline-items"}
        )

        for item in timeline.items:
            self.build_item_html(items_element, item)

        etree.SubElement(root_element, "div", {"class": "ug-timeline-after"})

    def build_item_html(self, parent, item: TimelineItem):
        item_element = etree.SubElement(
            parent,
            "div",
            {"class": "ug-timeline-item" + (f" {item.key}" if item.key else "")},
        )

        title_element = etree.SubElement(
            item_element, "h3", {"class": "ug-timeline-title"}
        )
        title_element.text = item.title

        if item.sub_title:
            sub_title_element = etree.SubElement(
                item_element, "span", {"class": "ug-timeline-sub-title"}
            )
            sub_title_element.text = item.sub_title

        content_element = etree.SubElement(
            item_element, "p", {"class": "ug-timeline-content"}
        )
        content_element.text = item.content

        icon_element = etree.SubElement(
            item_element, "div", {"class": self.get_dot_class(item)}
        )

        if item.icon:
            etree.SubElement(icon_element, "i", {"class": f"{item.icon} icon"})
