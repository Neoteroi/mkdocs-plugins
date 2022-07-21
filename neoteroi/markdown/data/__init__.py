"""
This module contains common classes that can be reused to obtain content and
configuration for extensions.
"""
from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


class SourceError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class ContentSource(Generic[T], ABC):
    @abstractmethod
    def read(self, source: str) -> T:
        """Returns content read from a source."""


class ConfigurationReader:
    ...


def read_from_source(source: str, sources: List[ContentSource]):
    # Example:
    # ./file.csv
    # ./file.json
    # ./file.yaml
    # ./URL -> CSV
    for source in sources:
        ...
