import re
from typing import Any, Dict, Iterable, List, Optional, Tuple, Type, TypeVar

from essentials.meta import deprecated

_TABLE_LINE_PATTERN = re.compile(r"\s?\|([^\|]+)")
_TABLE_SEPARATOR_LINE_PATTERN = re.compile(r"^[-:\s\|]*$")


class Matrix:
    """
    A matrix of rows and columns, with mutable values.
    """

    def __init__(
        self, columns_count: int, rows_count: int, initial_value: Any = None
    ) -> None:
        self._columns_count = columns_count
        self._rows_count = rows_count
        self._rows = tuple(
            [[initial_value for _ in range(columns_count)] for _ in range(rows_count)]
        )

    @property
    def rows(self) -> Tuple[List[Any], ...]:
        return self._rows

    def __str__(self) -> str:
        return f"<Matrix {str(self.rows)}>"

    def __repr__(self) -> str:
        return f"Matrix({self._columns_count}, {self._rows_count})"

    def __iter__(self):
        yield from self.rows

    def __len__(self):
        return len(self.rows)

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            if len(key) > 2:
                raise ValueError("Slice length out of boundary.")
            col, row = key
            self.rows[row][col] = value
            return

        raise ValueError("Expected a tuple of values (x, y).")

    def __getitem__(self, key):
        if isinstance(key, tuple):
            if len(key) > 2:
                raise ValueError("Slice length out of boundary.")
            col, row = key
            return self.rows[row][col]

        return self.rows[key]


class Table:
    """
    Represents a read-only table with information obtained from Markdown.
    """

    def __init__(
        self, headers: Iterable[str], records: Iterable[Iterable[str]]
    ) -> None:
        self._headers = tuple(headers)
        self._records = tuple(tuple(record) for record in records)
        self._headers_indexes = {header: i for i, header in enumerate(self._headers)}

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({self.headers}, "
            f"len: {len(self)} id: {id(self)})"
        )

    @property
    def headers(self) -> Tuple[str, ...]:
        return self._headers

    @property
    def records(self) -> Tuple[Tuple[str, ...], ...]:
        return self._records

    @property
    def rows(self) -> Iterable[Tuple[str, ...]]:
        yield self._headers
        yield from self.records

    def __iter__(self):
        yield from self.records

    def __len__(self):
        return len(self.records)

    def __getitem__(self, key):
        if isinstance(key, (int, slice)):
            return self.records[key]

        if isinstance(key, tuple):
            if len(key) > 2:
                raise ValueError("Slice length out of boundary.")
            col, row = key
            return self.records[row][col]

        if key not in self.headers:
            raise KeyError(key)
        index = self._headers_indexes[key]
        # TODO: handle missing values if a row has less values (this should not happen)
        return tuple(record[index] for record in self.records)


T = TypeVar("T", bound=Table)


def read_table(markdown: str, cls: Type[T]) -> Optional[T]:
    headers: List[str] = []
    records: List[List[str]] = []

    for line in markdown.splitlines():
        if _TABLE_SEPARATOR_LINE_PATTERN.match(line):
            continue

        matches = list(_TABLE_LINE_PATTERN.finditer(line))

        if matches:
            row = [match.group(1).strip() for match in matches]
            if not headers:
                headers = row
            else:
                records.append(row)

    return cls(headers, records) if headers else None


def read_table_records(markdown: str) -> Iterable[Dict[str, str]]:
    """
    Reads the records from a Markdown table and yields them, assuming that the table
    has headers and the separator line after the headers.

    Example:
    ```
        | A   | B   | C   | D   |
        | --- | --- | --- | --- |
        | 1   | 2   | 3   | 4   |
        | 5   | 6   | 7   | 8   |
    ```

    yields the following ->
    ```
        [
            {"A": "1", "B": "2", "C": "3", "D": "4"},
            {"A": "5", "B": "6", "C": "7", "D": "8"}
        ]
    ```
    """
    headers: Dict[int, str] = {}

    # TODO: raise a ValueError if none of the lines contains a headers separator line

    for line in markdown.splitlines():
        if _TABLE_SEPARATOR_LINE_PATTERN.match(line):
            continue

        matches = list(_TABLE_LINE_PATTERN.finditer(line))

        if matches:
            if not headers:
                headers = {
                    index: match.group(1).strip() for index, match in enumerate(matches)
                }
            else:
                values = {
                    headers[index]: match.group(1).strip()
                    for index, match in enumerate(matches)
                }
                yield values
