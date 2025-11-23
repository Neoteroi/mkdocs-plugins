from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class Contributor:
    name: str
    email: str
    count: int = -1
    image: str | None = None
    key: str | None = None


class ContributionsReader(ABC):
    @abstractmethod
    def get_contributors(self, file_path: Path) -> list[Contributor]:
        """Obtains the list of contributors for a file with the given path."""

    @abstractmethod
    def get_last_modified_date(self, file_path: Path) -> datetime:
        """Reads the last commit date of a file."""
