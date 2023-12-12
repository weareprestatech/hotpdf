class SparseMatrix:
    """
    2D representation of a PDF in plain text format.
    Sparse matrix removes the need to keep in memory the blank spaces
    that are present in a PDF. Thus reducing memory usage drastically.
    """

    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.values: dict = {}

    def __iter__(self):
        for row_idx in range(self.rows):
            for column_idx in range(self.columns):
                yield self.get(row_idx, column_idx)

    def __getitem__(self, key):
        return self.get(key[0], key[1])

    def __check_indices(self, row_idx: int, column_idx: int):
        if (
            row_idx < 0
            or row_idx > self.rows
            or column_idx < 0
            or column_idx > self.columns
        ):
            raise IndexError("Specified index is out of range")

    def insert(self, value: str, row_idx: int, column_idx: int):
        self.__check_indices(row_idx, column_idx)
        if value:
            self.values[(row_idx, column_idx)] = value

    def get(self, row_idx: int, column_idx: int):
        self.__check_indices(row_idx, column_idx)
        return self.values.get((row_idx, column_idx), "")
