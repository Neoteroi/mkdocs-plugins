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
            create_instance(cls, obj)

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
