"""
Day 10
https://adventofcode.com/2024/day/10

A fairly run-of-the-mill DFS problem (made slightly
easier by my Grid class). The plot twist was that
Part 2 did not require any memoization to run in
a reasonable amount of time.
"""

import util

from util import log
from grid import Grid


def find_trailheads(grid: Grid[int]) -> list[tuple[int, int]]:
    """
    Find the trailheads in the grid
    """
    rv = []
    for r, c, v in grid:
        if v == 0:
            rv.append((r,c))
    return rv

def explore_trail(grid: Grid[int], r: int, c: int) -> int:
    """
    Explore the trail in a DFS fashion.
    """

    def explore_trail_r(grid: Grid[int], r: int, c: int, visited: set[tuple[int, int]]) -> int:
        if (r, c) in visited:
            return 0
        
        visited.add((r,c))
        v = grid.get(r, c)

        # Base case: we reached the end of a trail
        if v == 9:
            return 1
        
        total = 0
        for dr, dc in Grid.CARDINAL_DIRS:
            nr, nc = r + dr, c + dc
            av = grid.getdefault(nr, nc)
            # Recursively explore adjacent position if
            # its value is one more than current value
            # (getdefault returns None if the position is
            # outside the grid, so the condition below
            # will also be False in that case)
            if av == v + 1:
                total += explore_trail_r(grid, nr, nc, visited)

        return total

    return explore_trail_r(grid, r, c, set())


def count_trails(grid: Grid[int], r: int, c: int) -> int:
    """
    Recursively count the number of unique trails starting
    at a given trailhead.
    """
    v = grid.get(r, c)

    # Base case: the end of the trail
    if v == 9:
        return 1

    # Recursively count all possible trails
    # starting at this point
    total = 0
    for dr, dc in Grid.CARDINAL_DIRS:
        nr, nc = r + dr, c + dc
        av = grid.getdefault(nr, nc)
        if av == v + 1:
            total += count_trails(grid, nr, nc)
    
    return total


def score_trails(grid: Grid[int]) -> int:
    """
    Part 1: Compute the scores of the trails
    """
    trailheads = find_trailheads(grid)

    total = 0
    for r, c in trailheads:
        total += explore_trail(grid, r, c)

    return total


def rate_trails(grid: Grid[int]) -> int:
    """
    Part 2: Compute the ratings of the trails

    For larger datasets, we would probably need to add
    memoization with @functools.cache
    """
    trailheads = find_trailheads(grid)

    total = 0
    for r, c in trailheads:
        total += count_trails(grid, r, c)

    return total


if __name__ == "__main__":
    util.set_debug(False)

    sample = Grid.from_file("input/sample/10.in", cast=int)
    input = Grid.from_file("input/10.in", cast=int)

    print("TASK 1")
    util.call_and_print(score_trails, sample)
    util.call_and_print(score_trails, input)

    print("\nTASK 2")
    util.call_and_print(rate_trails, sample)
    util.call_and_print(rate_trails, input)
