"""
Day 22
https://adventofcode.com/2021/day/22

1st star: 00:08:15
2nd star: 03:03:31

This problem was... painful. Part 1 was pretty straightforward but, for Part 2
I went down a lot of very unproductive rabbit holes. First, I checked whether
there was some sort of geometry library that would do all these operations
easily, then I started reading up on algorithms on "axis-aligned bounding boxes",
then I decided maybe I should just bite the bullet and implement union/difference
operations on cubes that split a cube into smaller cubes when another cube
is added/subtracted. That last one led me to a hellscape of off-by-one errors,
and I ultimately decided to scrap all the code entirely and start from scratch.

I came up with a solution that (I think) is rooted in the inclusion/exclusion
principle (although, not gonna lie, I also followed the "let's throw stuff at the
wall and see what sticks" principle on this one). Fortunately, the "intersection" 
operation I had already implemented was pretty solid, and things ultimately 
worked out.
"""

import util
import math
import sys
import re

from util import log


class Cube:
    """
    Class for representing cubes (or, rather, cuboids)
    """

    def __init__(self, min_point, max_point):
        self.min_point = min_point
        self.max_point = max_point

        # We keep track of cubes that have been subtracted from this cube
        self.subtracted = []

    @property
    def volume(self):
        """
        Computes the volume of the cube
        """
        x1,y1,z1 = self.min_point
        x2,y2,z2 = self.max_point

        # We need to subtract the volume of the subtracted cubes.
        # The subtract() method explains how we're avoiding double-
        # counting.
        subtracted_volumes = sum(c.volume for c in self.subtracted)

        return (x2-x1+1)*(y2-y1+1)*(z2-z1+1) - subtracted_volumes

    def subtract(self, other):
        """
        Subtract one cuboid from another.

        We dont actually subtract it (in the sense of creating new
        cubes that cover all the volume of the original cube minus
        the subtracted cube but, rather, we keep track of the
        subtracted cubes)
        """

        # We start by computing the intersection between the cubes.
        intr = self.intersection(other)

        # If the cubes don't intersect, there's nothing to subctract
        if intr is not None:
            # We recursively subctract the intersection cube
            # from all the cubes we've already subtracted. This avoids
            # double-counting subtractions.
            for s in self.subtracted:
                s.subtract(intr)

            # Finally, we add the intersection cube to the list of 
            # subtracted cubes.
            self.subtracted.append(intr)

    def intersection(self, other):
        """
        Computes the intersection between two cubes, returning
        a new Cube object covering the intersection.

        Based on https://stackoverflow.com/questions/5556170/finding-shared-volume-of-two-overlapping-cuboids
        """

        x1,y1,z1 = self.min_point
        x2,y2,z2 = self.max_point

        ox1,oy1,oz1 = other.min_point
        ox2,oy2,oz2 = other.max_point

        ix1 = max(x1,ox1)
        ix2 = min(x2,ox2)
        iy1 = max(y1,oy1)
        iy2 = min(y2,oy2)
        iz1 = max(z1,oz1)
        iz2 = min(z2,oz2)

        if ix2 - ix1 < 0 or iy2 - iy1 < 0 or iz2 - iz1 < 0:
            return None
        else:
            return Cube((ix1,iy1,iz1), (ix2,iy2,iz2))

    def inside(self, other):
        """
        Returns True if self is wholy inside other. False otherwise
        """
        x1,y1,z1 = self.min_point
        x2,y2,z2 = self.max_point

        ox1,oy1,oz1 = other.min_point
        ox2,oy2,oz2 = other.max_point

        min_inside = ox1 <= x1 <= ox2 and \
                     oy1 <= y1 <= oy2 and \
                     oz1 <= z1 <= oz2

        max_inside = ox1 <= x2 <= ox2 and \
                     oy1 <= y2 <= oy2 and \
                     oz1 <= z2 <= oz2

        return min_inside and max_inside

    def __str__(self):
        """
        Dunder method for debugging
        """
        x1,y1,z1 = self.min_point
        x2,y2,z2 = self.max_point

        return f"{self.toggle} x={x1}..{x2},y={y1}..{y2},z={z1}..{z2}"


def reboot(cubes, bounding_cube=None):
    """
    Reboot the reactor by processing the cubes (ignoring those outside
    the bounding cube, if any)
    """

    on_cubes = []
    for toggle, cube in cubes:
        if bounding_cube is None or cube.inside(bounding_cube):
            # We subtract the cube from all the on cubes we've encountered
            # so far. We need to do this regardless of whether this is
            # and on of off cube: if it's an on cube, subtracting the
            # cube ensures we produce a union of both cubes (and don't
            # double-count the intersection). If it's an off cube, this
            # has the effect of turning the interscting on cubes "off"
            for on_cube in on_cubes:
                on_cube.subtract(cube)

            # We add this cube only if it's an on cube
            if toggle == "on":
                on_cubes.append(cube)

    return sum(c.volume for c in on_cubes)


def read_input(input):
    """
    Reads the input
    """
    input_iterator = util.iter_parse(input, "{} x={:d}..{:d},y={:d}..{:d},z={:d}..{:d}")

    cubes = []
    for toggle, x1, x2, y1, y2, z1, z2 in input_iterator:
        cubes.append((toggle, Cube((x1,y1,z1), (x2,y2,z2))))
        
    return cubes


def task1(input):
    """
    Task 1: Reboot the reactor with a bounding cube
    """
    cubes = read_input(input)

    return reboot(cubes, bounding_cube=Cube((-50,-50,-50),(50,50,50)))


def task2(input):
    """
    Task 2: Reboot the reactor (and process all cubes)
    """
    cubes = read_input(input)

    return reboot(cubes)
    

if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/22-1.in", sep="\n")
    sample2 = util.read_strs("input/sample/22-2.in", sep="\n")
    sample3 = util.read_strs("input/sample/22-3.in", sep="\n")
    input = util.read_strs("input/22.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample1)
    util.call_and_print(task1, sample2)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample1)
    util.call_and_print(task2, sample3)
    util.call_and_print(task2, input)
