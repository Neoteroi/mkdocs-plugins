import csv
import json
from abc import ABC, abstractmethod
from io import StringIO
from typing import Any, Iterable, Optional, Tuple

import yaml


class TextParser(ABC):
    """
    Base class for classes that can deserialize text into Python objects.
    """
    @abstractmethod
    def parse(self, text) -> Any:
        """Parses a text into a more complex object."""


class YAMLParser(TextParser):

    def parse(self, text) -> Any:
        return yaml.safe_load(text)


class JSONParser(TextParser):

    def parse(self, text) -> Any:
        return json.loads(text)


class CSVParser(TextParser):

    def get_reader(self, csv_file):
        return csv.DictReader(csv_file, delimiter=",")

    def parse(self, text) -> Any:
        with StringIO(text) as string_io:
            reader = self.get_reader(string_io)
            return [record for record in reader]


DEFAULT_PARSERS: Tuple[TextParser, ...] = (YAMLParser(), JSONParser(), CSVParser())


def try_parse_text(text: str, parsers: Optional[Iterable[TextParser]] = None) -> Any:
    if parsers is None:
        parsers = DEFAULT_PARSERS

    for parser in parsers:
        try:
            return parser.parse(text)
        except (TypeError, ValueError):
            pass

    raise ValueError("The input text could not be parsed.")
