"""
Utility functions and classes for Advent of Code
"""

import shapely.geometry
import shapely.affinity
import math
import copy
import parse # type: ignore

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

def read_strs(filename, sep=None, sep2=None, strip=True):
    """
    Read strings from a file, separated by whitespace or by the
    specified separator.
    """
    with open(filename) as f:
        txt = f.read()
        if strip:
            txt = txt.strip()
        strs = txt.split(sep=sep)  

    if sep2 is not None:
        strs = [s.split(sep=sep2) for s in strs]

    return strs


def read_ints(filename, sep=None, sep2=None):
    """
    Read integers from a file, separated by whitespace or by the
    specified separator.
    """
    strs = read_strs(filename, sep, sep2)
    
    if sep2 is not None:
        return [[int(x) for x in s] for s in strs]
    else:
        return [int(x) for x in strs]


def iter_parse(strings, fmt):
    """
    Generator function that iterates over a sequence of strings,
    and returns the values parsed according to a format string
    """
    p = parse.compile(fmt)

    for s in strings:
        yield p.parse(s)


#
# UTILITY FUNCTIONS / CLASSES
#

class Direction:
    def __init__(self, x, y):
        self._p = shapely.geometry.Point(x, y)

    @classmethod
    def bearing(cls, degrees):
        north = cls(0,1)
        return shapely.affinity.rotate(north, -degrees)

    @classmethod
    def UP(cls):
        return cls(0,1)

    @classmethod
    def DOWN(cls):
        return cls(0,-1)

    @classmethod
    def RIGHT(cls):
        return cls(1,0)

    @classmethod
    def LEFT(cls):
        return cls(-1,0)

    def __eq__(self, other):
        return self._p == other._p

    def __hash__(self):
        return hash((self._p.x, self._p.y))

    def __copy__(self):
        return Direction(self._p.x, self._p.y)

    NORTH = UP
    SOUTH = DOWN
    EAST = RIGHT
    WEST = LEFT

    def rotate_counterclockwise(self, degrees):
        # Rotate anti-clockwise by degrees
        self._p = shapely.affinity.rotate(self._p, degrees, origin=(0,0))

    def rotate_clockwise(self, degrees):
        # Rotate clockwise by degrees
        self._p = shapely.affinity.rotate(self._p, -degrees, origin=(0,0))

    def move_grid_coordinates(self, x_or_coords, y=None):
        assert (isinstance(x_or_coords, int) and isinstance(y, int)) or \
            (isinstance(x_or_coords, tuple) and len(x_or_coords) == 2 and
             isinstance(x_or_coords[0], int) and isinstance(x_or_coords[1], int) and
             y is None)

        if isinstance(x_or_coords, int):
            x = x_or_coords
            y = y
        elif isinstance(x_or_coords, tuple):
            x, y = x_or_coords

        assert self._p.x in (-1,0,1) and self._p.y in (-1,0,1)
        x2 = x + int(self._p.x)
        y2 = y + int(self._p.y)
        return (x2, y2)

    def __repr__(self):
        return "<{}, {}>".format(self._p.x, self._p.y)       


def rotate_counterclockwise(point, degrees, origin=(0,0)):
    """
    Rotate a point counterclockwise around an origin.
    """

    rp = shapely.affinity.rotate(shapely.geometry.Point(*point), degrees, origin)

    # A lot of AoC problems use 0, 90, 180, 270, etc. degrees and integer coordinates.
    # In these cases, we want to return integers.
    if isinstance(point[0], int) and isinstance(point[1], int) and degrees % 90 == 0:
        return (round(rp.x), round(rp.y))

    return (rp.x, rp.y)


def rotate_clockwise(point, degrees, origin=(0,0)):
    """
    Rotate a point counterclockwise around an origin.
    """
    return rotate_counterclockwise(point, -degrees, origin)


def angle_points(origin, p1, p2):
    """
    Return the angle between two points, relative to an origin
    """
    dx1 = p1.x - origin.x
    dy1 = p1.y - origin.y

    dx2 = p2.x - origin.x
    dy2 = p2.y - origin.y

    a1 = math.atan2(dy1, dx1)
    a2 = math.atan2(dy2, dx2)

    d = math.degrees(a2 - a1)

    if d < 0:
        return 360 + d
    else:
        return d
