"""
Day 6
https://adventofcode.com/2024/day/6

The first part of the problem was fairly straightforward
to solve with my Grid class. 

For the second part, I tried a brute force approach:
for each open position in the grid, add an obstacle and
run a patrol to see if the guard get stuck. This worked,
but took about a minute to run on my computer. I then
realized you only needed to try the open positions along
the guards original patrol, which reduced the running
time considerably (but I still wonder if there is a less
brute force-ish approach)
"""

import util
from grid import Grid

from util import log

class InfiniteLoopException(Exception):
    """Exception thrown when the guard falls into an infinite loop"""
    pass

def patrol(grid: Grid, sr: int, sc: int) -> set[tuple[int, int]]:
    """Run a patrol of the grid

    Returns the number of steps, or raises
    InfiniteLoopException if the guard gets
    stuck in a loop
    """
    r, c = sr, sc
    dr, dc = Grid.UP
    visited = set()
    visited_dir = set()

    while grid.valid(r, c):
        # If the guard visits the same position
        # again, moving in the same direction,
        # then they've fallen into a loop
        vec = (r,c,dr,dc)
        if vec in visited_dir:
            raise InfiniteLoopException

        # Update visited sets
        visited.add((r,c))
        visited_dir.add((r,c,dr,dc))

        # Next position
        nr, nc = r + dr, c + dc

        # Update position/direction if there's an obstacle
        if grid.getdefault(nr, nc) == "#":
            dr, dc = grid.CLOCKWISE[(dr, dc)]
            # Careful: if we encounter an obstacle, we turn
            # but we don't take a step (there could be an
            # obstacle in front of us after turning)
            nr, nc = r, c

        r, c = nr, nc

    return visited


def count_steps(grid: Grid) -> int:
    """
    Part 1: Count the number of steps the guard takes
    in a single patrol.
    """
    rv = grid.find_value("^")
    assert rv is not None

    sr, sc = rv

    visited = patrol(grid, sr, sc)

    return len(visited)


def count_stuck(grid: Grid) -> int:
    """
    Part 2: Count how many obstacles we could add
    that would cause the guard to get stuck in an
    infinite loop
    """
    rv = grid.find_value("^")
    assert rv is not None

    sr, sc = rv

    # Brute force-ish approach: Find the positions
    # visited by the guard, and then try adding
    # an obstacle in each one of them (except
    # the starting position)

    visited = patrol(grid, sr, sc)
    visited.remove((sr, sc))

    total = 0
    for r, c in visited:
        grid.set(r, c, "#")
        try:
            patrol(grid, sr, sc)
        except InfiniteLoopException:
            total += 1
        grid.set(r, c, ".")

    return total


if __name__ == "__main__":
    util.set_debug(False)

    sample = Grid.from_file("input/sample/06.in")
    input = Grid.from_file("input/06.in")

    print("TASK 1")
    util.call_and_print(count_steps, sample)
    util.call_and_print(count_steps, input)

    print("\nTASK 2")
    util.call_and_print(count_stuck, sample)
    util.call_and_print(count_stuck, input)
