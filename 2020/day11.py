"""
Day 11
https://adventofcode.com/2020/day/11

1st star: 00:08:32
2nd star: 00:25:05

Dang, almost made it into the global leaderboard for the 1st star
(I placed 101st!) It helped that I had a pretty decent Grid class
that saved me a lot of time.

The second star uses brute force, with some very minor optimizations,
but I'm pretty sure there's a more DP-ish solution for this.
"""

import util
import math
import sys
import re

from util import log

DIRECTIONS = [(-1, -1), (0, -1), (+1,-1),
              (-1,  0),          (+1, 0),
              (-1, +1), (0, +1), (+1,+1)]

def find_occupied(grid, x, y, direction, immediate_only):
    """
    Checks if you can see an occupied seat from position x, y
    looking in the given direction (specifying an x, y offset)
    If immediate_only is true, we only look at seats immediately
    adjacent to x, y
    """
    dx, dy = direction
    xx = x + dx
    yy = y + dy

    while 0 <= xx < grid.max_x and 0 <= yy < grid.max_y:
        v = grid.get(xx, yy)

        if v == "L":
            return 0
        elif v == "#":
            return 1
        elif v == "." and immediate_only:
            return 0

        xx = xx + dx
        yy = yy + dy

    return 0


def get_new_value(grid, x, y, immediate_only, threshold):
    """
    Update the seat according to the rules given in the problem.
    If immediate_only is True, we only look at seats immediately
    adjacent to x, y (otherwise, we use line of sight). threshold
    specifies the minimum number of occupied seat to flip an
    occupied seat to an empty seat.
    """
    cur_value = grid.get(x, y)

    if cur_value == ".":
        return "."

    occupied = 0
    for dir in DIRECTIONS:
        occupied += find_occupied(grid, x, y, dir, immediate_only)
        if cur_value == "L" and occupied >= 1:
            return "L"
        elif cur_value == "#" and occupied >= threshold:
            return "L"

    if cur_value == "L" and occupied == 0:
        return "#"
    else:
        return cur_value


def update_grid(grid, immediate_only, threshold):
    """
    Update the entire grid. See 'get_new_value' for meaning
    of immediate_only and threshold.
    """
    new_grid = util.Grid.empty(grid.max_x, grid.max_y)
    changes = 0
    for x in range(grid.max_x):
        for y in range(grid.max_y):
            old_value = grid.get(x, y)
            new_value = get_new_value(grid, x, y, immediate_only, threshold)
            new_grid.set(x, y, new_value)

            if old_value != new_value:
                changes += 1

    return new_grid, changes


def find_stable_state(grid, immediate_only, threshold):
    """
    Find the number of occupied seats in the stable state.
    """
    while True:
        grid, changes = update_grid(grid, immediate_only, threshold)

        if changes == 0:
            occupied = 0
            for x in range(grid.max_x):
                for y in range(grid.max_y):
                    if grid.get(x, y) == "#":
                        occupied += 1
            return occupied
        

if __name__ == "__main__":
    util.set_debug(False)

    sample = util.Grid.from_file("input/sample/11.in")
    grid = util.Grid.from_file("input/11.in")

    print("TASK 1")
    util.call_and_print(find_stable_state, sample, True, 4)
    util.call_and_print(find_stable_state, grid, True, 4)

    print("\nTASK 2")
    util.call_and_print(find_stable_state, sample, False, 5)
    util.call_and_print(find_stable_state, grid, False, 5)
