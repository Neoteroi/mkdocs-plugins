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


@dataclass
class Cards:
    items: List[CardItem]
