"""
Utility functions and classes for Advent of Code
"""

import copy

#
# DEBUGGING/LOGGING
#

DEBUG=False

def set_debug(debug):
    """
    Enables/disables debug messages
    """
    global DEBUG
    DEBUG = debug


def log(*args):
    """
    Prints a debugging message (if debugging messages are enabled)
    """
    if DEBUG: 
        print('\x1b[7;30;47m', end="")
        print(*args, end="")
        print('\x1b[0m')


def call_and_print(fn, *args):
    """
    Call a function with some parameters, and print the
    function call and the return value.
    """
    str_args = ", ".join(repr(arg) for arg in args)

    if len(str_args) > 20:
        str_args = str_args[:20] + "..."

    print("{}({}) = {}".format(fn.__name__, str_args, fn(*args)))


#
# FILE I/O
#

def read_strs(filename, sep=None):
    """
    Read strings from a file, separated by whitespace or by the
    specified separator.
    """
    with open(filename) as f:
        txt = f.read().strip()
        strs = txt.split(sep=sep)    

    return strs


def read_ints(filename, sep=None):
    """
    Read integers from a file, separated by whitespace or by the
    specified separator.
    """
    strs = read_strs(filename, sep)
    return [int(x) for x in strs]


#
# UTILITY FUNCTIONS / CLASSES
#

class Grid:
    """
    Used to manipulate grids with one character per position,
    using (x,y) coordinates (where the top-left position is 0,0)
    """

    def __init__(self, grid, infinite_x=False, infinite_y=False):
        self.infinite_x = infinite_x
        self.infinite_y = infinite_y
        self._grid = copy.deepcopy(grid)


    def __str__(self):
        rows = ["".join(row) for row in self._grid]
        return "\n".join(rows)


    @property
    def max_x(self):
        return len(self._grid[0])


    @property
    def max_y(self):
        return len(self._grid)


    def __validate_coords(self, x, y):
        orig_x = x
        orig_y = y

        if self.infinite_x:
            x = x % self.max_x
        
        if self.infinite_y:
            y = y % self.max_y

        if not 0 <= x < self.max_x or not 0 <= y < self.max_y:
            raise IndexError(f"Invalid position ({x}, {y}). Original: ({orig_x}, {orig_y})")

        return x, y        

    def get(self, x, y):
        x, y = self.__validate_coords(x, y)

        return self._grid[y][x]


    def set(self, x, y, value):
        x, y = self.__validate_coords(x, y)

        self._grid[y][x] = value


    @classmethod
    def from_file(cls, filename):
        lines = read_strs(filename, sep="\n")

        # We convert each line to a list, in case we
        # need to modify the contents of the grid
        grid = [list(line) for line in lines]

        return cls(grid)


    @classmethod
    def empty(cls, max_x, max_y, char=" "):
        grid = [[char] * max_x for _ in range(max_y)]

        return cls(grid)        
