"""
Grid classes for Advent of Code
"""
from typing import TypeVar, Generic, Callable

import math
import copy

T = TypeVar("T")


class Grid(Generic[T]):
    """
    Used to manipulate
    """
    
    # Useful for problems that require checking adjacent positions
    DIRECTIONS = [(-1, -1), (0, -1), (+1,-1),
                  (-1,  0),          (+1, 0),
                  (-1, +1), (0, +1), (+1,+1)]

    CARDINAL_DIRS = [          (0, -1),
                     (-1,  0),          (+1, 0),
                               (0, +1)         ]

    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)

    CLOCKWISE = {UP: RIGHT,
                 RIGHT: DOWN,
                 DOWN: LEFT,
                 LEFT: UP}

    COUNTER_CLOCKWISE = {UP: LEFT,
                         LEFT: DOWN,
                         DOWN: RIGHT,
                         RIGHT: UP}

    _grid: list[list[T]]

    def __init__(self, grid: list[list[T]]):
        self._grid = copy.deepcopy(grid)

    def __str__(self):
        rows = ["".join(str(x) for x in row) for row in self._grid]
        return "\n".join(rows)

    def str_with_markers(self, locs: list[tuple[int, int]], char: str) -> str:
        rows = []
        for r, row in enumerate(self._grid):
            line = []
            for c, value in enumerate(row):
                if (r, c) in locs:
                    line.append(char)
                else:
                    line.append(str(value))
            rows.append("".join(line))
        return "\n".join(rows)


    def copy(self):
        return Grid(self._grid)

    def __iter__(self):
        """
        Iterate over the grid yielding (row, col, value) for each cell.

        Example:
            for r, c, v in grid:
                ...
        """
        for r, row in enumerate(self._grid):
            for c, v in enumerate(row):
                yield (r, c, v)

    def items(self):
        """Alias for `__iter__`, returns an iterator of (row, col, value)."""
        return self.__iter__()

    @property
    def rows(self):
        return len(self._grid)

    @property
    def cols(self):
        return len(self._grid[0])

    def __validate_coords(self, row: int, col: int) -> None:
        if not 0 <= row < self.rows or not 0 <= col < self.cols:
            raise IndexError(f"Invalid position ({row}, {col})")

    def get(self, row: int, col: int) -> T:
        self.__validate_coords(row, col)

        return self._grid[row][col]

    def getdefault(self, row: int, col: int, default: T | None = None) -> T | None:
        try:
            return self.get(row, col)
        except IndexError:
            return default

    def valid(self, row: int, col: int) -> bool:
        try:
            self.__validate_coords(row, col)
            return True
        except IndexError:
            return False

    def set(self, row: int, col: int, value: T) -> None:
        self.__validate_coords(row, col)

        self._grid[row][col] = value

    def hash(self) -> int:
        tpl_grid = tuple(tuple(row) for row in self._grid)
        return hash(tpl_grid)

    @classmethod
    def _from_lines(cls, lines: list[str], cast: type | None = str) -> "Grid":
        # We convert each line to a list, in case we
        # need to modify the contents of the grid
        str_grid = [list(line) for line in lines]

        if cast is None:
            cast = str

        grid = [[cast(v) for v in row] for row in str_grid]

        return cls(grid)

    @classmethod
    def from_file(cls, filename: str, cast: type | None = None) -> "Grid":
        with open(filename) as f:
            txt = f.read().strip()
            lines = txt.split("\n")

        return cls._from_lines(lines, cast)

    @classmethod
    def from_string(cls, grid_str: str, cast: type | None = None) -> "Grid":
        lines = grid_str.strip().split(sep="\n")

        return cls._from_lines(lines, cast)

    @classmethod
    def init(cls, rows: int, cols: int, value: T) -> "Grid":
        grid = [[value] * cols for _ in range(rows)]

        return cls(grid)        
