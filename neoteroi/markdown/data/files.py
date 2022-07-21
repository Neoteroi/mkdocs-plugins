import json
from pathlib import Path

import yaml

from . import ContentSource


def read_file(file_path: Path) -> str:
    with open(file_path, "rt", encoding="utf-8") as source_file:
        return source_file.read()


def read_json_file(file_path: Path) -> str:
    return json.loads(read_file(file_path))


def read_yaml_file(file_path: Path) -> str:
    return yaml.safe_load(read_file(file_path))


class JSONContentReader(ContentSource):
    def read(self):
        """Returns content read from a source."""
