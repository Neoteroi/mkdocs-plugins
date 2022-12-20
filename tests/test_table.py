import pytest

from neoteroi.mkdocs.markdown.tables import Matrix, Table


def test_table_slice():
    table = Table(
        ["A", "_", "B" "_"],
        [
            ["A1", "A2", "B1", "B2"],
            ["A3", "A4", "B3", "B4"],
        ],
    )

    assert table[0, 0] == "A1"
    assert table[1, 0] == "A2"
    assert table[0, 1] == "A3"
    assert table[1, 1] == "A4"
    assert table[2, 0] == "B1"
    assert table[2, 1] == "B3"

    with pytest.raises(ValueError):
        table[2, 1, 0]


def test_table_functions():
    table = Table(
        ["A", "_", "B" "_"],
        [
            ["A1", "A2", "B1", "B2"],
            ["A3", "A4", "B3", "B4"],
        ],
    )
    assert repr(table) == (
        f"{table.__class__.__name__}({table.headers}, "
        f"len: {len(table)} id: {id(table)})"
    )

    assert list(table) == [
        ("A1", "A2", "B1", "B2"),
        ("A3", "A4", "B3", "B4"),
    ]

    assert len(table) == 2


def test_matrix_assignment():
    matrix = Matrix(10, 10)

    assert matrix[2, 2] is None
    matrix[2, 2] = 1
    assert matrix[2, 2] == 1


def test_matrix_read_row():
    matrix = Matrix(8, 8)

    matrix[2, 2] = 1
    assert matrix[2] == [None, None, 1, None, None, None, None, None]

    matrix = Matrix(8, 8, initial_value=0)

    matrix[2, 2] = 1
    assert matrix[2] == [0, 0, 1, 0, 0, 0, 0, 0]


def test_matrix_invalid_assignments():
    matrix = Matrix(10, 10)

    with pytest.raises(ValueError):
        matrix[2, 2, 3]

    with pytest.raises(ValueError):
        matrix[2, 2, 3] = ...

    with pytest.raises(ValueError):
        matrix[2] = ...


def test_matrix_functions():
    matrix = Matrix(2, 2)

    matrix[1, 1] = 1
    assert list(matrix) == [[None, None], [None, 1]]

    assert repr(matrix) == f"Matrix({matrix._columns_count}, {matrix._rows_count})"
    assert str(matrix) == f"<Matrix {str(matrix.rows)}>"
