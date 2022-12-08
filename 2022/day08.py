"""
Day 8
https://adventofcode.com/2022/day/8

1st star: 00:08:12
2nd star: 00:21:23

Once again, my Grid class comes to the rescue. That said,
my first solution involved a lot of rote loops to iterate
up, down, left, and right, which led to a bunch of silly
mistakes. In hindsight, I should've just used the
CARDINAL_DIRS list from the start (as in the cleaned
up solution below)
"""

import util
import math
import sys
import re

from util import log

def is_visible(grid, x, y):
    """
    Checks if an edge is visible from (x, y) in any
    direction (up, down, left, right)
    """
    height = grid.get(x, y)

    # Check in all cardinal directions
    for dx, dy in util.Grid.CARDINAL_DIRS:
        # If we encounter a tree that is not shorter
        # we'll set this to False
        all_shorter = True

        # Keep moving in the current direction (dx, dy)
        # until we reach an invalid grid value (because
        # we went past the edge)
        ix, iy = x + dx, y + dy
        while grid.valid(ix, iy):
            height2 = grid.get(ix, iy)
            if height2 >= height:
                all_shorter = False
                break
            ix, iy = ix + dx, iy + dy
        
        if all_shorter:
            return True

    return False


def viewing_distance(grid, x, y):
    """
    Find the product of the viewing distances from (x,y)
    in all directions (up, down, left, right)
    """
    height = grid.get(x, y)

    distances = []
    for dx, dy in util.Grid.CARDINAL_DIRS:
        distance = 0

        # Keep moving in the current direction (dx, dy)
        # until we reach an invalid grid value (because
        # we went past the edge)
        ix, iy = x + dx, y + dy
        while grid.valid(ix, iy):
            distance += 1
            height2 = grid.get(ix, iy)
            if height2 >= height:
                break
            ix, iy = ix + dx, iy + dy
        
        distances.append(distance)

    return math.prod(distances)


def count_visible(grid):
    """
    Count how many visible trees there are
    """
    visible = 0
    for x in range(0, grid.max_x):
        for y in range(0, grid.max_y):
            if is_visible(grid, x, y):
                visible += 1

    return visible
    

def find_max_viewing_distance(grid):
    """
    Find the tree with the highest viewing distance
    (and return the distance)
    """
    best = 0
    for x in range(0, grid.max_x):
        for y in range(0, grid.max_y):
            vd = viewing_distance(grid, x, y)
            if vd > best:
                best = vd

    return best


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.Grid.from_file("input/sample/08.in", cast=int)
    input = util.Grid.from_file("input/08.in", cast=int)

    print("TASK 1")
    util.call_and_print(count_visible, sample)
    util.call_and_print(count_visible, input)

    print("\nTASK 2")
    util.call_and_print(find_max_viewing_distance, sample)
    util.call_and_print(find_max_viewing_distance, input)
