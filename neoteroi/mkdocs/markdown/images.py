import xml.etree.ElementTree as etree
from dataclasses import dataclass
from typing import Optional

from .utils import create_instance


@dataclass
class Image:
    url: str
    height: Optional[int] = None
    width: Optional[int] = None
    alt: Optional[str] = None

    @classmethod
    def from_obj(cls, obj):
        if isinstance(obj, str):
            return cls(obj)
        elif isinstance(obj, dict):
            return create_instance(cls, obj)

        raise TypeError("The given object is not of a supported type.")

    def get_props(self):
        props = {"src": self.url}

        if self.height is not None:
            props["height"] = str(self.height)

        if self.width is not None:
            props["width"] = str(self.width)

        if self.alt:
            props["alt"] = str(self.alt)

        return props


def build_image_html(parent, image: Image):
    etree.SubElement(parent, "img", image.get_props())


def build_icon_html(parent, icon):
    if not icon:
        return

    if "/" in icon:
        etree.SubElement(
            parent, "img", {"class": "icon", "src": icon, "alt": "step icon"}
        )
    elif "fa-" in icon:
        # Fontawesome
        etree.SubElement(parent, "i", {"class": f"{icon} icon"})
    else:
        # other icon - this integrates with other processors, like the one from
        # Material for MkDocs!
        span = etree.SubElement(parent, "span", {"class": "icon"})
        span.text = icon
