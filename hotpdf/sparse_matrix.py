from collections import defaultdict
from collections.abc import Iterator
from warnings import warn


class SparseMatrix:
    """2D representation of a PDF in plain text format.

    Sparse matrix removes the need to keep in memory the blank spaces
    that are present in a PDF. Thus reducing memory usage drastically.
    """

    def __init__(self, rows: int = 0, columns: int = 0):
        self.values: defaultdict[tuple[int, int], str] = defaultdict(str)
        self.rows = rows
        self.columns = columns

    def __getitem__(self, key: tuple[int, int]) -> str:
        row_idx, column_idx = key
        self.__check_indices(row_idx, column_idx)
        return self.values[(row_idx, column_idx)]

    def __update_indices(self, row_idx: int, column_idx: int) -> None:
        if row_idx > self.rows:
            self.rows = row_idx + 1
        if column_idx > self.columns:
            self.columns = column_idx + 1

    def __check_indices(self, row_idx: int, column_idx: int) -> None:
        if row_idx < 0 or column_idx < 0:
            raise IndexError("Specified index is out of range")

    def __setitem__(self, key: tuple[int, int], value: str) -> None:
        row_idx, column_idx = key
        try:
            self.__check_indices(row_idx, column_idx)
        except IndexError as ie:
            warn("Index Error. Skipping insertion into SparseMatrix", stacklevel=1)
            warn(str(ie), stacklevel=1)
            return
        self.__update_indices(row_idx, column_idx)
        if value:
            self.values[(row_idx, column_idx)] = value

    def __iter__(self) -> Iterator[tuple[tuple[int, int], str]]:
        yield from self.values.items()

    def insert(self, value: str, row_idx: int, column_idx: int) -> None:
        self.__update_indices(row_idx, column_idx)
        try:
            self.__check_indices(row_idx, column_idx)
        except IndexError:
            warn("Index Error. Skipping insertion into SparseMatrix", stacklevel=1)
            return
        if value:
            self.values[(row_idx, column_idx)] = value

    def get(self, row_idx: int, column_idx: int) -> str:
        self.__check_indices(row_idx, column_idx)
        return self.values[(row_idx, column_idx)]
