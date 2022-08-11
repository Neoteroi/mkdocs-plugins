from pathlib import Path
from typing import Any

from .source import DataReader


def read_file(file_path: Path, encoding: str = "utf-8") -> str:
    with open(file_path, "rt", encoding=encoding) as source_file:
        return source_file.read()


class FileReader(DataReader):
    encoding = "utf-8"

    def test(self, source: str) -> bool:
        source_path = Path(source)
        return source_path.exists() and source_path.is_file()

    def read(self, source: str) -> Any:
        assert self.test(source)
        return read_file(Path(source), encoding=self.encoding)
