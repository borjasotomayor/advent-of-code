"""
Day 12
https://adventofcode.com/2022/day/12

1st star: 00:25:11
2nd star: 00:31:53

This was one of those problems were I had a pretty good sense of
how to solve the problem from the start, and then lost a bunch
of time with silly bugs (including one stemming from not reading
the problem carefully enough, smdh)

It also would've taken me much longer, except this year I finally
sat down and wrote down some common algorithms for Advent of
Code. So, instead of having to spend a bunch of time reviewing
(and re-coding) Breadth-First Search, I was just able to copy-paste
my implementation in algorithms.py, and use that as a starting point.
"""

import util
import math
import sys
import re

from util import log

def climb(grid, start_x, start_y):
    """
    Starting at (start_x, start_y) find the shortest path to
    the location of the grid containing an "E". We only
    return the distance, not the actual path.

    This function uses breadth-first search, adapted from
    the grid_bfs function in my algorithms.py module
    """

    # Queue
    q = []
    q.append((start_x,start_y))

    # Set of visited locations
    visited = {(start_x,start_y)}

    # Distance and previous-location dictionaries
    dist = {}
    dist[(start_x,start_y)] = 0
    target = None

    # Ye olde BFS loop
    while len(q) > 0:
        cur = q.pop(0)

        cx, cy = cur

        cur_elev = grid.get(cx, cy)

        # Adjust if we're at the start
        if cur_elev == "S":
            cur_elev = "a"

        # Check if we've reached the target
        if cur_elev == "E":
            target = cur
            break

        # Check the neighbors
        for dx, dy in util.Grid.CARDINAL_DIRS:
            neigh = cx+dx, cy+dy
            nx, ny = neigh
            if grid.valid(nx, ny) and neigh not in visited:
                neigh_elev = grid.get(nx, ny)

                # Adjust if we're at the target
                if neigh_elev == "E":
                    neigh_elev = "z"

                if ord('a') <= ord(neigh_elev) <= ord(cur_elev) + 1:
                    visited.add(neigh)
                    dist[neigh] = dist[cur] + 1
                    q.append(neigh)
    

    if target is None:
        # If there was no path to the target, return None
        return None
    else:
        # Otherwise, return the number of steps
        return dist[target]


def task1(grid):
    """
    Find the shortest path starting at a single location
    """

    # Find the starting position
    start = None
    for x in range(0, grid.max_x):
        for y in range(0, grid.max_y):
            if grid.get(x, y) == "S":
                start = (x, y)
                break
        if start is not None: break
        
    # Find the number of steps
    sx, sy = start
    steps = climb(grid, sx, sy)

    return steps


def task2(grid):
    """
    Find the shortest path starting from multiple possible locations
    """

    # Find all the possible starting points
    starts = set()
    for x in range(0, grid.max_x):
        for y in range(0, grid.max_y):
            if grid.get(x, y) in ("S", "a"):
                starts.add((x,y))

    # Find all the paths
    path_lengths = set()
    for x, y in starts:
        steps = climb(grid, x, y)
        if steps is not None:
            path_lengths.add(steps)

    # Return the shortest path
    return min(path_lengths)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.Grid.from_file("input/sample/12.in")
    input = util.Grid.from_file("input/12.in")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
