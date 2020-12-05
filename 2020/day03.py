"""
Day 3
https://adventofcode.com/2020/day/3

1st star: 00:08:08
2nd star: 00:11:42

After getting the stars, I refactored the code considerably, including
implementing a Grid class (in util.py) that abstracts away how to 
work with an "infinite" grid. Once you do that, the code for counting
the number of trees is pretty clean and straightforward.

The 2nd star is also pretty straightforward if you take care to
write a "count_trees" function that takes the x-skip and y-skip
as parameters.
"""

import util
import math

from util import log


def count_trees(grid, x_skip, y_skip):
    log(grid.max_x, grid.max_y)
    
    x, y = 0, 0
    n_trees = 0
    while y < grid.max_y:
        log("CHECKING", x, y)
        if grid.get(x, y) == "#":
            log("Tree at ({}, {})".format(x, y))
            n_trees += 1

        x += x_skip
        y += y_skip

    return n_trees


def task1(grid):
    return count_trees(grid, x_skip=3, y_skip=1)


def task2(grid):
    total_trees = []

    for x_skip, y_skip in [(1,1),(3,1),(5,1),(7,1),(1,2)]:
        trees = count_trees(grid, x_skip, y_skip)
        total_trees.append(trees) 

    return math.prod(total_trees)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.Grid.from_file("input/sample/03.in")
    sample.infinite_x = True
    
    grid = util.Grid.from_file("input/03.in")
    grid.infinite_x = True

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, grid)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, grid)

