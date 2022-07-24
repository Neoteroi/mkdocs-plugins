from dataclasses import dataclass
from typing import List, Optional

from neoteroi.markdown.align import Alignment


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
    align: Alignment = Alignment.LEFT
    alternate: bool = False
