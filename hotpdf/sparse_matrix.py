class SparseMatrix:
    """
    2D representation of a PDF in plain text format.
    Sparse matrix removes the need to keep in memory the blank spaces
    that are present in a PDF. Thus reducing memory usage drastically.
    """

    def __init__(self, rows: int = 0, columns: int = 0):
        self.values: dict = {}
        self.rows = rows
        self.columns = columns

    def __getitem__(self, key):
        row_idx, column_idx = key
        self.__check_indices(row_idx, column_idx)
        return self.values.get((row_idx, column_idx), "")

    def __update_indices(self, row_idx, column_idx):
        if row_idx > self.rows:
            self.rows = row_idx + 1
        if column_idx > self.columns:
            self.columns = column_idx + 1

    def __check_indices(self, row_idx: int, column_idx: int):
        if row_idx < 0 or column_idx < 0:
            raise IndexError("Specified index is out of range")

    def __setitem__(self, key, value):
        row_idx, column_idx = key
        self.__check_indices(row_idx, column_idx)
        self.__update_indices(row_idx, column_idx)
        if value:
            self.values[(row_idx, column_idx)] = value

    def __iter__(self):
        for key, value in self.values.items():
            yield key, value

    def insert(self, value: str, row_idx: int, column_idx: int):
        self.__update_indices(row_idx, column_idx)
        self.__check_indices(row_idx, column_idx)
        if value:
            self.values[(row_idx, column_idx)] = value

    def get(self, row_idx: int, column_idx: int):
        self.__check_indices(row_idx, column_idx)
        return self.values.get((row_idx, column_idx), "")
