"""
Day 8
https://adventofcode.com/2024/day/8

This problem was... kinda confusing? I ultimately got it,
but it involved a bit of trial and error to ensure I was
interpreting the problem statement correctly. Not gonna
lie, this wasn't the most exciting problem to solve.
"""

import util
import itertools
from grid import Grid

from util import log


def count_antinodes(grid: Grid, resonant: bool) -> int:
    """
    Part 1 and 2: Count the number of antinodes. If resonant
    is True, account for resonant harmonics (Part 2)
    """

    # Determine the locations of the antennas
    antennas: dict[str, set[tuple[int, int]]] = {}
    for r, c, v in grid:
        if v != ".":
            antennas.setdefault(v, set()).add((r,c))
    
    # Compute the pairs of antennas of the same frequency
    pairs = set()
    for ant, locs in antennas.items():
        for pair in itertools.combinations(locs, 2):
            pairs.add(pair)

    # Figure out the location of the antinodes.
    # Given a pair of antennas, we compute the 
    # (row, col) difference between the two
    # coordinates, and add that difference in
    # both directions.
    antinodes = set()
    for ((r1, c1), (r2, c2)) in pairs:
        # Compute antinode(s) in one direction
        dr, dc = r2 - r1, c2 - c1
        ar, ac = r2 + dr, c2 + dc
        while grid.valid(ar, ac):
            antinodes.add((ar, ac))
            ar, ac = ar + dr, ac + dc
            # In part 1, we only add the first
            # antinode
            if not resonant:
                break

        # And in the other direction
        dr, dc = r1 - r2, c1 - c2
        ar, ac = r1 + dr, c1 + dc
        while grid.valid(ar, ac):
            antinodes.add((ar, ac))
            ar, ac = ar + dr, ac + dc
            if not resonant:
                break

    num_antinodes = len(antinodes)

    # In Part 2, we also need to add the
    # locations of antennas such that:
    #
    # - There are at least two antennas of that same
    #   frequency on the map.
    # - The location of the antenna hasn't already
    #   been identified as an antinode.
    if resonant:
        antiantennas = 0
        for locs in antennas.values():
            if len(locs) < 2:
                continue

            for a in locs:
                if a not in antinodes:
                    num_antinodes += 1

    return num_antinodes


if __name__ == "__main__":
    util.set_debug(False)

    sample = Grid.from_file("input/sample/08.in")
    input = Grid.from_file("input/08.in")

    print("TASK 1")
    util.call_and_print(count_antinodes, sample, False)
    util.call_and_print(count_antinodes, input, False)

    print("\nTASK 2")
    util.call_and_print(count_antinodes, sample, True)
    util.call_and_print(count_antinodes, input, True)
