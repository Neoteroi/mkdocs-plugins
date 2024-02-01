"""
This module defines a base class for types that can read text from a source.
"""

from abc import ABC, abstractmethod
from typing import Any


class DataReader(ABC):
    @abstractmethod
    def test(self, source: str) -> bool:
        """
        Returns a value indicating whether this DataReader can read from a source
        described by the given value.
        """

    @abstractmethod
    def read(self, source: str) -> Any:
        """Returns data read from a source."""
