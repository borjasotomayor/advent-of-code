"""
Day 13
https://adventofcode.com/2023/day/13

1st star: 00:28:40
2nd star: 00:42:51

Time to break out the NumPy! This problem felt more laborious than
anything else, and I was surprised that the naive approach for
Part 2 (trying to flip every element in the grid) worked.
"""
import numpy as np
import numpy.typing as npt

import util


def find_reflection_col(grid: npt.NDArray[np.character], ignore_col: int) -> int:
    """
    Finds the right-hand column of a vertical line of reflection
    (this happens to be the number of columns to the left of the
    vertical line of reflection). If none exists, returns 0.

    We don't define a similar function for rows, because we can
    just rotate the array 90 degrees to turn the row problem
    into a column problem.
    """

    # The approach is to consider all columns as possible
    # reflection points, and to disprove columns one row
    # at a time until the set has size 0 (no reflection)
    # or 1 (reflection). This avoids having to check
    # the reflection on the entire array. For example,
    # if no reflection point is found in one row, it
    # doesn't matter what the other rows contain: the
    # array as a whole won't have a reflection point.
    candidate_cols = set(range(1, len(grid[0])))

    # For Part 2, we may need to ignore a previous reflection point
    candidate_cols.discard(ignore_col)

    # We check every row
    for row in grid:
        for col in frozenset(candidate_cols):
            # Compute the left and right side of the reflection point
            left = np.flip(row[:col])
            right = row[col:]

            # Compare both sides, up to the length of the smallest side
            max_reflection = min(len(left), len(right))
            if not np.array_equal(left[:max_reflection], right[:max_reflection]):
                # If they're not equal, this is not a valid
                # reflection point
                candidate_cols.discard(col)

        # If there are no candidate columns left, no point in
        # checking further
        if len(candidate_cols) == 0:
            break

    # If there is a reflection point, return it. Otherwise
    # return 0 (note how that is not a valid reflection point,
    # because were returning the right-hand column of the
    # reflection point)
    if len(candidate_cols) == 1:
        return candidate_cols.pop()
    else:
        return 0


def find_reflection(grid: npt.NDArray[np.character], ignore: tuple[int, int] = (0, 0)) -> tuple[int, int]:
    """
    Returns a tuple with the number of columns to the left of the vertical line
    of reflection and the number of rows above the horizontal line of reflection.
    If neither exists, returns (0, 0)

    Optionally, ignore prior lines of reflection via the "ignore" parameter.
    """
    refl = find_reflection_col(grid, ignore[0])
    if refl > 0:
        return refl, 0
    else:
        grid = np.rot90(grid)
        refl = find_reflection_col(grid, ignore[1])
        if refl is None:
            return 0, 0
        else:
            return 0, refl


def task1(input: list[list[str]]) -> int:
    """
    Task 1: Add up the reflection points in each grid
    """
    sum = 0
    for grid_lines in input:
        grid = np.array([list(line) for line in grid_lines])
        col_refl, row_refl = find_reflection(grid)
        sum += col_refl + 100*row_refl

    return sum


def flip(grid: npt.NDArray[np.character], r: int, c: int) -> None:
    """
    Flip a value in a grid
    """
    if grid[r][c] == ".":
        grid[r][c] = "#"
    elif grid[r][c] == "#":
        grid[r][c] = "."


def task2(input: list[list[str]]) -> int:
    """
    Task 2: Add up the reflection points in each grid, accounting for smudges
    """
    sum = 0
    for grid_lines in input:
        grid = np.array([list(line) for line in grid_lines])
        orig_refl = find_reflection(grid)

        # We try flipping every possible value in the grid
        # and checking whether it creates a new reflection point.
        # We bail if that point is found.
        done = False
        for r in range(len(grid)):
            if done: break
            for c in range(len(grid[0])):
                # Flip the value
                flip(grid, r, c)
                # Find the reflection points, taking care to ignore
                # the original one.
                refl = find_reflection(grid, ignore=orig_refl)
                if refl != (0, 0) and refl != orig_refl:
                    sum += refl[0] + 100 * refl[1]
                    done = True
                    break
                # Flip back the value
                flip(grid, r, c)

    return sum


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/13.in", sep="\n\n", sep2="\n")
    input = util.read_strs("input/13.in", sep="\n\n", sep2="\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
