from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional


@dataclass
class Contributor:
    name: str
    email: str
    count: int = -1
    image: Optional[str] = None
    key: Optional[str] = None


class ContributionsReader(ABC):
    @abstractmethod
    def get_contributors(self, file_path: Path) -> List[Contributor]:
        """Obtains the list of contributors for a file with the given path."""

    @abstractmethod
    def get_last_modified_date(self, file_path: Path) -> datetime:
        """Reads the last commit date of a file."""
