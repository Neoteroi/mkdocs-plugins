from dataclasses import dataclass
from typing import List, Optional


@dataclass
class TimelineItem:
    title: str
    content: Optional[str] = None
    sub_title: Optional[str] = None
    icon: Optional[str] = None
    key: Optional[str] = None


@dataclass
class Timeline:
    items: List[TimelineItem]
