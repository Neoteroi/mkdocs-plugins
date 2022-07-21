from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class TimelineAlignment(Enum):
    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"


@dataclass
class TimelineItem:
    title: str
    content: str
    sub_title: Optional[str] = None
    icon: Optional[str] = None
    key: Optional[str] = None


@dataclass
class Timeline:
    items: List[TimelineItem]
    align: TimelineAlignment = TimelineAlignment.LEFT
    alternate: bool = False
