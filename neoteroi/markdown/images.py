import xml.etree.ElementTree as etree
from dataclasses import dataclass
from typing import Optional

# TODO: remove this!!


@dataclass
class Image:
    url: str
    height: Optional[int] = None
    width: Optional[int] = None
    alt: Optional[str] = None

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
