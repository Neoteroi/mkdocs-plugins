from neoteroi.markdown.tables import Matrix, Table


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


def test_matrix():
    matrix = Matrix(10, 10)

    assert matrix[2, 2] is None
    matrix[2, 2] = 1
    assert matrix[2, 2] == 1
