"""
Day 4
https://adventofcode.com/2025/day/4

Once again, having a ready-made Grid class
made solving this kind of problem pretty
striaghtforward.
"""

import util
import math
import sys
import re

from util import log
from grid import Grid


def is_accessible(grid: Grid, r: int, c: int) -> bool:
    """
    Checks if a position on the grid contains a roll 
    of paper and, if so, checks whether it is accessible.  
    """
    v = grid.get(r, c)

    if v == "@":
        num_adj = 0
        for dr, dc in Grid.DIRECTIONS:
            if grid.getdefault(r+dr, c+dc) == "@":
                num_adj += 1
        if num_adj < 4:
            return True

    return False


def count_accessible(g: Grid) -> int:
    """
    Counts the number of accessible rolls of paper
    on the grid
    """
    accessible = 0
    for r in range(g.rows):
        for c in range(g.cols):
            if is_accessible(g, r, c):
                accessible += 1
                    
    return accessible


def count_removed(g: Grid) -> int:
    """
    Count the number of rolls of paper that can be removed
    """
    total_removed = 0

    # In each iteration, we go through the entire grid,
    # and remove accessible rolls of paper as we encounter
    # them. If we go through the grid and don't remove
    # anything, we're done.
    while True:
        removed = 0

        for r in range(g.rows):
            for c in range(g.cols):
                if is_accessible(g, r, c):
                    removed += 1
                    g.set(r, c, ".")

        total_removed += removed

        if removed == 0:
            break

    return total_removed


if __name__ == "__main__":
    util.set_debug(False)

    sample = Grid.from_file("input/sample/04.in")
    input = Grid.from_file("input/04.in")

    print("TASK 1")
    util.call_and_print(count_accessible, sample)
    util.call_and_print(count_accessible, input)

    print("\nTASK 2")
    util.call_and_print(count_removed, sample)
    util.call_and_print(count_removed, input)
