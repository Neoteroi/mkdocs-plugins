from dataclasses import dataclass


@dataclass
class TimelineItem:
    title: str
    content: str | None = None
    sub_title: str | None = None
    icon: str | None = None
    key: str | None = None


@dataclass
class Timeline:
    items: list[TimelineItem]
