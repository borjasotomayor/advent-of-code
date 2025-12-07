"""
Day 7
https://adventofcode.com/2025/day/7

A very satisfying recursive problem (particularly when adding a single line
to add memoization made everything fall into place for Part 2)
"""

import util
import functools

from util import log
from grid import Grid



def explore(grid: Grid[str], r: int, c: int, visited: set[tuple[int, int]]) -> int:
    """
    Explore the diagram in a DFS-ish way, starting at a given coordinate.
    """

    # Base case: We encounter a coordinate that we've already explored,
    # or we fall off the grid.
    if (r, c) in visited or not grid.valid(r, c):
        return 0
          
    visited.add((r, c))

    if grid.get(r, c) == "^":
        # If we encounter a splitter, we branch left and right
        left = explore(grid, r, c-1, visited)
        right = explore(grid, r, c+1, visited)
        return 1 + left + right
    else:
        # Otherwise, we keep going down
        return explore(grid, r+1, c, visited)
        

@functools.lru_cache
def quantum_explore(grid: Grid[str], r:int, c: int) -> int:   
    """
    Count the number of paths through the diagram. For 
    large inputs, will not finish in a reasonable amount
    of time without memoization.    
    """
    if r == grid.rows:
        # If we fall below the diagram, that is one path
        return 1
          
    if grid.get(r, c) == "^":
        # If we encounter a splitter, count up the paths
        # to the left and right.
        left = quantum_explore(grid, r, c-1)
        right = quantum_explore(grid, r, c+1)
        return left + right
    else:
        # Otherwise, keep going down.
        return quantum_explore(grid, r+1, c)


def count_splits(grid: Grid[str]) -> int:
    """
    Task 1: Count the number of splits
    """
    
    # Find the starting point
    for r, c, v in grid:
        if v == "S":
            break

    return explore(grid, r, c, set())


def count_paths(grid: Grid[str]) -> int:
    """
    Task 2: Count the number of paths
    """

    # Find the starting point
    for r, c, v in grid:
        if v == "S":
            break

    return quantum_explore(grid, r, c)


if __name__ == "__main__":
    util.set_debug(False)

    sample = Grid.from_file("input/sample/07.in")
    input = Grid.from_file("input/07.in")

    print("TASK 1")
    util.call_and_print(count_splits, sample)
    util.call_and_print(count_splits, input)

    print("\nTASK 2")
    util.call_and_print(count_paths, sample)
    util.call_and_print(count_paths, input)
