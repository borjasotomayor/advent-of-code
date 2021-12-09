"""
Day 9
https://adventofcode.com/2021/day/9

1st star: 00:07:13
2nd star: 00:19:24

This is one of those problems where the Grid class I wrote a while back
(and have been improving over the years) came in veeeery handy. No need
to futz around with the boundaries of the grid, etc. as it was all
handled by my Grid class.

Other than that, a pretty straightforward application of flood filling.
The code below is pretty similar to what I wrote to solve the problem,
with some minor refactoring and cleaning up.
"""

import util
import math
import sys
import re

from util import log


def find_low_points(grid):
    """
    Finds the low points in a height map
    """
    low_points = []
    for x in range(grid.max_x):
        for y in range(grid.max_y):
            v = grid.get(x,y)

            dirs = [(x-1, y), (x+1, y), (x, y+1), (x, y-1)]
            adjs = [grid.getdefault(dx, dy) for dx, dy in dirs]

            if  all(v < a for a in adjs if a is not None):
                low_points.append((x,y))

    return low_points


def task1(grid):
    """
    Task 1: find the low points, and add up their heights+1
    """
    low_points = find_low_points(grid)

    risk = 0
    for x, y in low_points:
        height = grid.get(x,y)
        risk += height + 1

    return risk
    

def basin_size(grid, x, y):
    """
    Find the size of a basin at coordinates (x, y) using flood filling
    """

    def basin_size_r(grid, x, y, visited):
        if (x, y) in visited:
            return 0
        
        visited.add((x,y))

        v = grid.get(x,y)

        dirs = [(x-1, y), (x+1, y), (x, y+1), (x, y-1)]

        size = 1
        for dx, dy in dirs:
            a_v = grid.getdefault(dx,dy)
            if a_v is not None and a_v > v and a_v < 9:
                size += basin_size_r(grid, dx, dy, visited)

        return size

    return basin_size_r(grid, x, y, visited=set())


def task2(grid):
    """
    Task 2: Find the size of the basins, and return the
    product of the top three sizes.
    """
    low_points = find_low_points(grid)

    sizes = [basin_size(grid, x, y) for x, y in low_points]
    sizes.sort(reverse=True)

    return math.prod(sizes[:3])
        

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.Grid.from_file("input/sample/09.in", cast=int)
    input = util.Grid.from_file("input/09.in", cast=int)

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
