"""
Utility functions and classes for Advent of Code
"""

import shapely.geometry
import shapely.affinity
import math
import parse # type: ignore
from collections.abc import Callable, Generator
from typing import Self, overload

#
# DEBUGGING/LOGGING
#

DEBUG=False

def set_debug(debug: bool) -> None:
    """
    Enables/disables debug messages
    """
    global DEBUG
    DEBUG = debug


def log(*args: object) -> None:
    """
    Prints a debugging message (if debugging messages are enabled)
    """
    if DEBUG: 
        print('\x1b[7;30;47m', end="")
        print(*args, end="")
        print('\x1b[0m')


def call_and_print(fn: Callable[..., object], *args: object) -> None:
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

@overload
def read_strs(filename: str, sep: str | None = ..., sep2: None = ..., strip: bool = ...) -> list[str]: ...

@overload
def read_strs(filename: str, sep: str | None, sep2: str, strip: bool = ...) -> list[list[str]]: ...

def read_strs(filename: str, sep: str | None = None, sep2: str | None = None, strip: bool = True) -> list[str] | list[list[str]]:
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
        return [s.split(sep=sep2) for s in strs]

    return strs


@overload
def read_ints(filename: str, sep: str | None = ..., sep2: None = ..., strip: bool = ...) -> list[int]: ...

@overload
def read_ints(filename: str, sep: str | None, sep2: str, strip: bool = ...) -> list[list[int]]: ...

def read_ints(filename: str, sep: str | None = None, sep2: str | None = None, strip: bool = True) -> list[int] | list[list[int]]:
    """
    Read integers from a file, separated by whitespace or by the
    specified separator.
    """
    strs = read_strs(filename, sep, strip=strip)
    if sep2 is not None:
        return [[int(x) for x in s.split(sep=sep2)] for s in strs]
    return [int(x) for x in strs]


def iter_parse(strings: list[str], fmt: str) -> Generator:
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
    def __init__(self, x: float, y: float):
        self._p = shapely.geometry.Point(x, y)

    @classmethod
    def bearing(cls, degrees: float) -> "Direction":
        north = cls(0, 1)
        rotated = shapely.affinity.rotate(north._p, -degrees, origin=(0, 0))
        return cls(rotated.x, rotated.y)

    @classmethod
    def UP(cls) -> "Direction":
        return cls(0,1)

    @classmethod
    def DOWN(cls) -> "Direction":
        return cls(0,-1)

    @classmethod
    def RIGHT(cls) -> "Direction":
        return cls(1,0)

    @classmethod
    def LEFT(cls) -> "Direction":
        return cls(-1,0)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Direction):
            return False
        return self._p == other._p

    def __hash__(self) -> int:
        return hash((self._p.x, self._p.y))

    def __copy__(self) -> "Direction":
        return Direction(self._p.x, self._p.y)

    NORTH = UP
    SOUTH = DOWN
    EAST = RIGHT
    WEST = LEFT

    def rotate_counterclockwise(self, degrees: float) -> None:
        # Rotate anti-clockwise by degrees
        self._p = shapely.affinity.rotate(self._p, degrees, origin=(0,0))

    def rotate_clockwise(self, degrees: float) -> None:
        # Rotate clockwise by degrees
        self._p = shapely.affinity.rotate(self._p, -degrees, origin=(0,0))

    def move_grid_coordinates(self, x_or_coords: int | tuple[int, int], y: int | None=None) -> tuple[int, int]:
        assert (isinstance(x_or_coords, int) and isinstance(y, int)) or \
            (isinstance(x_or_coords, tuple) and len(x_or_coords) == 2 and
             isinstance(x_or_coords[0], int) and isinstance(x_or_coords[1], int) and
             y is None)

        if isinstance(x_or_coords, int):
            assert isinstance(y, int)
            x = x_or_coords
            y = y
        elif isinstance(x_or_coords, tuple):
            x, y = x_or_coords

        assert self._p.x in (-1,0,1) and self._p.y in (-1,0,1)
        x2 = x + int(self._p.x)
        y2 = y + int(self._p.y)
        return (x2, y2)

    def __repr__(self) -> str:
        return "<{}, {}>".format(self._p.x, self._p.y)       


def rotate_counterclockwise(point: tuple[float, float], degrees: float, origin: tuple[float, float]=(0,0)) -> tuple[float, float]:
    """
    Rotate a point counterclockwise around an origin.
    """

    rp = shapely.affinity.rotate(shapely.geometry.Point(*point), degrees, origin)

    # A lot of AoC problems use 0, 90, 180, 270, etc. degrees and integer coordinates.
    # In these cases, we want to return integers.
    if isinstance(point[0], int) and isinstance(point[1], int) and degrees % 90 == 0:
        return (round(rp.x), round(rp.y))

    return (rp.x, rp.y)


def rotate_clockwise(point: tuple[float, float], degrees: float, origin: tuple[float, float]=(0,0)) -> tuple[float, float]:
    """
    Rotate a point counterclockwise around an origin.
    """
    return rotate_counterclockwise(point, -degrees, origin)


def angle_points(origin: shapely.Point, p1: shapely.Point, p2: shapely.Point) -> float:
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
