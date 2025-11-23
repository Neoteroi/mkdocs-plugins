from dataclasses import dataclass

from neoteroi.mkdocs.markdown.images import Image


@dataclass
class CardItem:
    title: str
    url: str | None = None
    content: str | None = None
    icon: str | None = None
    key: str | None = None
    image: Image | None = None

    def __post_init__(self):
        if self.image and not self.image.alt:
            self.image.alt = self.title


@dataclass
class Cards:
    items: list[CardItem]
