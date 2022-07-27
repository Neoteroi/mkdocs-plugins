import logging
import xml.etree.ElementTree as etree

from neoteroi.markdown.align import aligment_from_props

from .domain import Timeline, TimelineItem

logger = logging.getLogger("MARKDOWN")


class TimelineHTMLBuilder:
    def __init__(self, props) -> None:
        self.align = aligment_from_props(props)
        self.alternate = props.get("alternate", False)

    def get_class(self) -> str:
        return (
            "nt-timeline vertical "
            + self.align.value
            + (" alternate" if self.alternate else "")
        )

    def get_dot_class(self, item: TimelineItem) -> str:
        return "nt-timeline-dot " + (item.key or "") + (" bigger" if item.icon else "")

    def build_html(self, parent, timeline: Timeline):
        root_element = etree.SubElement(parent, "div", {"class": self.get_class()})
        etree.SubElement(root_element, "div", {"class": "nt-timeline-before"})

        items_element = etree.SubElement(
            root_element, "div", {"class": "nt-timeline-items"}
        )

        for item in timeline.items:
            self.build_item_html(items_element, item)

        etree.SubElement(root_element, "div", {"class": "nt-timeline-after"})

    def build_icon_html(self, parent, item: TimelineItem):
        if not item.icon:
            return

        if item.icon.startswith("http"):
            etree.SubElement(
                parent, "img", {"class": "icon", "src": item.icon, "alt": "step icon"}
            )
        elif "fa-" in item.icon:
            # Fontawesome
            etree.SubElement(parent, "i", {"class": f"{item.icon} icon"})
        else:
            # other icon - this integrates with other processors, like the one from
            # Material for MkDocs!
            span = etree.SubElement(parent, "span", {"class": "icon"})
            span.text = item.icon

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

        dot_element = etree.SubElement(
            item_element, "div", {"class": self.get_dot_class(item)}
        )

        if item.icon:
            self.build_icon_html(dot_element, item)
