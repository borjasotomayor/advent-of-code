"""
This module defines a Grid class that comes in handy in
Advent of Code problems that involve working with grids,
particularly when we need to navigate around the grid
(keeping grid bounds in mind).
"""

from typing import Generic, Self
from collections.abc import Generator
from typing_extensions import TypeVar

import copy

# Type variable so we can make the Grid class generic
# While most grids contain strings, there are occasional
# exceptions and, for type-checking purposes, it pays off
# to make the Grid a generic class.
T = TypeVar("T", default=str)


class Grid(Generic[T]):
    """
    Grid class for manipulating grids of values,
    indexed by row and column
    """
    
    # Useful for problems that require checking adjacent positions
    DIRECTIONS = [(-1, -1), (0, -1), (+1,-1),
                  (-1,  0),          (+1, 0),
                  (-1, +1), (0, +1), (+1,+1)]

    CARDINAL_DIRS = [          (0, -1),
                     (-1,  0),          (+1, 0),
                               (0, +1)         ]

    # Cardinal directions of movement
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)
    LEFT = (0, -1)

    # Dictionary to easily rotate a direction
    # clockwise (90 degrees right)
    CLOCKWISE = {UP: RIGHT,
                 RIGHT: DOWN,
                 DOWN: LEFT,
                 LEFT: UP}

    # Dictionary to easily rotate a direction
    # counter-clockwise (90 degrees left)
    COUNTER_CLOCKWISE = {UP: LEFT,
                         LEFT: DOWN,
                         DOWN: RIGHT,
                         RIGHT: UP}

    _grid: list[list[T]]

    #
    # CONSTRUCTORS
    #

    def __init__(self, grid: list[list[T]]):
        """Constructor

        Create a grid from a list of lists. Typically not
        called directly.

        Args:
            grid (list[list[T]]): List of lists of values
        """
        self._grid = copy.deepcopy(grid)

    @classmethod
    def _from_lines(cls, lines: list[str], cast: type | None = None) -> Self:
        """Helper method to create a Grid from a list of strings

        Args:
            lines (list[str]): List of strings representing the grid,
               with one character per cell.
            cast (type | None, optional): Optionally, cast each character
               to a given type.

        Returns: Grid
        """
        # We convert each line to a list, in case we
        # need to modify the contents of the grid
        str_grid = [list(line) for line in lines]

        if cast is None:
            cast = str

        grid = [[cast(v) for v in row] for row in str_grid]

        return cls(grid)

    @classmethod
    def from_file(cls, filename: str, cast: type | None = None) -> Self:
        """Create a Grid from a text file

        The file should contain one line per row, and one
        character per cell. By default, creates a Grid
        of strings, but the characters can be cast to a different
        type.

        Args:
            filename (str): Filename
            cast (type | None, optional): Type to cast characters to. 

        Returns: Grid
        """
        with open(filename) as f:
            txt = f.read().strip()
            lines = txt.split("\n")

        return cls._from_lines(lines, cast)

    @classmethod
    def from_string(cls, grid_str: str, cast: type | None = None) -> Self:
        """Create a grid from a string

        The file should contain one line per row, and one
        character per cell. By default, creates a Grid
        of strings, but the characters can be cast to a different
        type.

        Args:
            grid_str (str): String containing the grid
            cast (type | None, optional):  Type to cast characters to. 

        Returns: Grid
        """
        lines = grid_str.strip().split(sep="\n")

        return cls._from_lines(lines, cast)

    @classmethod
    def init(cls, rows: int, cols: int, value: T) -> Self:
        """Create a grid filled with a specific value

        Creates a grid of the given dimensions, and sets all the values
        to the given value

        Args:
            rows (int): Number of rows
            cols (int): Number of columns
            value (T): Value to set in all cells

        Returns: Grid
        """
        grid = [[value] * cols for _ in range(rows)]

        return cls(grid)        

    def __str__(self) -> str:
        """Returns a print-able string representation"""
        rows = ["".join(str(x) for x in row) for row in self._grid]
        return "\n".join(rows)

    def str_with_markers(self, locs: list[tuple[int, int]], char: str) -> str:
        """Create a string representation (with extra markers)

        Creates a string representation, but adding markers at
        specified locations.

        Args:
            locs (list[tuple[int, int]]): Locations to add markers at
            char (str): Character to use as a marker

        Returns:
            str: String representation with markers
        """
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

    def copy(self) -> Self:
        """Create a deep copy of the grid

        Returns: Grid
        """
        return type(self)(self._grid)
    
    #
    # PROPERTIES
    #

    @property
    def rows(self) -> int:
        """Returns the number of rows in the grid"""
        return len(self._grid)

    @property
    def cols(self) -> int:
        """Returns the number of columns in the grid"""
        return len(self._grid[0])    
    
    #
    # ACCESS METHODS
    #

    def __iter__(self) -> Generator[tuple[int, int, T], None, None]:
        """
        Iterate over the grid yielding (row, col, value) for each cell.

        Example:
            for r, c, v in grid:
                ...
        """
        for r, row in enumerate(self._grid):
            for c, v in enumerate(row):
                yield (r, c, v)

    def items(self)-> Generator[tuple[int, int, T], None, None]:
        """Alias for `__iter__`, returns an iterator of (row, col, value)."""
        return self.__iter__()

    def __validate_coords(self, row: int, col: int) -> None:
        """Helper method to validate (row, col) coordinates

        Args:
            row (int): Row
            col (int): Column

        Raises:
            IndexError: If the row or column are not valid
        """
        if not 0 <= row < self.rows or not 0 <= col < self.cols:
            raise IndexError(f"Invalid position ({row}, {col})")

    def get(self, row: int, col: int) -> T:
        """Get the value at (row, col), assuming valid coordinates

        Raises an exception if the coordinates are not valid

        Args:
            row (int): Row
            col (int): Column

        Returns:
            T: Value at (row, col)

        Raises:
            IndexError: If the row or column are not valid
        """
        self.__validate_coords(row, col)

        return self._grid[row][col]

    def getdefault(self, row: int, col: int, default: T | None = None) -> T | None:
        """Get value at (row, col), or a default value if the coordinates are not valid

        This method is useful when inspecting values around a coordinate, as
        it avoids having to do bounds checking. Instead, we can just check
        whether this method returns the default value.

        Args:
            row (int): Row
            col (int): Column
            default (T | None, optional): Default to return if (row, col)
                are not valid coordinates.

        Returns: The value at (row, col) if the coordinates are valid,
            the default value otherwise.
        """
        try:
            return self.get(row, col)
        except IndexError:
            return default

    def valid(self, row: int, col: int) -> bool:
        """Checks if (row, col) are valid coordinates

        Args:
            row (int): Row
            col (int): Column

        Returns: True if the coordinates are valid, False otherwise.
        """
        try:
            self.__validate_coords(row, col)
            return True
        except IndexError:
            return False

    #
    # UPDATE METHODS
    #

    def set(self, row: int, col: int, value: T) -> None:
        """Set the value at (row, col)

        Args:
            row (int): Row
            col (int): Column
            value (T): Value

        Raises:
            IndexError: If the row or column are not valid            
        """
        self.__validate_coords(row, col)

        self._grid[row][col] = value


    #
    # UTILITY METHODS
    #

    def hash(self) -> int:
        """Return a hash value that can be used in sets, dictionaries, etc.

        Currently just generates a hash based on a
        tuple of tuples representation of the grid.

        Returns:
            int: Hash value
        """
        tpl_grid = tuple(tuple(row) for row in self._grid)
        return hash(tpl_grid)
    
    def find_value(self, value: T) -> tuple[int, int] | None:
        """Find the first occurrence of a value in the grid

        Args:
            v (T): value to search for

        Returns:
            tuple[int, int]: Coordinates of the value, or
            None if the value can't be found.
        """
        for r, c, v in self.items():
            if v == value:
                return (r, c)
        
        return None
