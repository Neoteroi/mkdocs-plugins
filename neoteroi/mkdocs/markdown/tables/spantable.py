import re
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple

from .. import extract_props
from . import Matrix, Table

SPAN_RE = re.compile(r"@span=?([\d]+)?:?([\d]+)?")


@dataclass
class Cell:
    text: str
    skip: bool = False
    col_span: int = 1
    row_span: int = 1
    props: Optional[Dict[str, str]] = None

    @property
    def html_class(self) -> Optional[str]:
        return self.props.get("class") if self.props else None


def _iter_coords(
    x: int, y: int, colspan: int, rowspan: int
) -> Iterable[Tuple[int, int]]:
    for x_increment in range(colspan):
        for y_increment in range(rowspan):
            yield (x + x_increment, y + y_increment)


def _get_auto_cols_span(values: Tuple[str, ...], start_index: int = 0) -> int:
    span = 1

    for i in range(start_index, len(values)):
        if not values[i].strip():
            span += 1
        else:
            break
    return span


def _get_auto_rows_span(
    rows: List[Tuple[str, ...]], start_index: int, cols_slice: slice
) -> int:
    span = 1

    for i in range(start_index, len(rows)):
        values_to_check = rows[i][cols_slice]
        if all(not value.strip() for value in values_to_check):
            span += 1
        else:
            break
    return span


def get_matrix(table: Table) -> Matrix:
    matrix = Matrix(len(table.records[0]), len(table.records) + 1)
    rows = list(table.records)
    rows.insert(0, table.headers)

    for row_index, row in enumerate(rows):
        for column_index, value in enumerate(row):
            existing_cell = matrix[column_index, row_index]

            if existing_cell is not None:
                # set by previous span
                continue

            match = SPAN_RE.search(value)
            if match:
                raw_cols_span = match.group(1)
                raw_rows_span = match.group(2)

                if raw_cols_span is None and raw_rows_span is None:
                    # Automatic mode: increase the span until empty cells are found
                    # columns span takes precedence over rows span
                    cols_span = _get_auto_cols_span(row, column_index + 1)
                    rows_span = _get_auto_rows_span(
                        rows,
                        row_index + 1,
                        slice(column_index, column_index + cols_span),
                    )
                else:
                    cols_span = max(int(raw_cols_span or 1), 1)
                    rows_span = max(int(raw_rows_span or 1), 1)

                if cols_span > 0 or rows_span > 0:
                    for coords in _iter_coords(
                        column_index, row_index, cols_span, rows_span
                    ):
                        current = coords == (column_index, row_index)
                        cell_text, props = (
                            extract_props(SPAN_RE.sub("", value).strip(), "@")
                            if current
                            else ["", {}]
                        )
                        matrix[coords] = Cell(
                            cell_text,
                            skip=not current,
                            col_span=cols_span,
                            row_span=rows_span,
                            props=props,
                        )
            else:
                cell_text, props = extract_props(value, "@")
                matrix[column_index, row_index] = Cell(cell_text, props=props)
    return matrix


class SpanTable(Table):
    """
    Class holding information about a table represented in Markdown, supporting
    colspan and rowspan.
    """

    def __init__(
        self, headers: Iterable[str], records: Iterable[Iterable[str]]
    ) -> None:
        super().__init__(headers, records)
        self._matrix = get_matrix(self)

    @property
    def matrix(self) -> Matrix:
        return self._matrix
