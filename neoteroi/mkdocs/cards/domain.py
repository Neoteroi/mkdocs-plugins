from dataclasses import dataclass
from typing import List, Optional

from neoteroi.mkdocs.markdown.images import Image


@dataclass
class CardItem:
    title: str
    url: Optional[str] = None
    content: Optional[str] = None
    icon: Optional[str] = None
    key: Optional[str] = None
    image: Optional[Image] = None

    def __post_init__(self):
        if self.image and not self.image.alt:
            self.image.alt = self.title


@dataclass
class Cards:
    items: List[CardItem]
