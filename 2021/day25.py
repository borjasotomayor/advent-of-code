"""
Day 25
https://adventofcode.com/2021/day/25

1st star: 00:21:21
2nd star: 00:21:26

Well, it's over! As usual, the last problem was a bit of a gimme,
but still challenging enough to make it fun.
"""

import util

def half_step(grid, herd):
    """
    Update the grid for just one herd
    """
    new_grid = util.Grid.empty(grid.max_x, grid.max_y, ".")

    moves = 0    
    for x in range(grid.max_x):
        for y in range(grid.max_y):
            if herd == ">" and grid.get(x, y) == ">":
                next_x = 0 if x + 1 == grid.max_x else x + 1
                if grid.get(next_x, y) == ".":
                    moves += 1
                    new_grid.set(x, y, ".")
                    new_grid.set(next_x, y, ">")
                else:
                    new_grid.set(x,y,">")
            elif herd == "v" and grid.get(x, y) == "v":
                next_y = 0 if y + 1 == grid.max_y else y + 1
                if grid.get(x, next_y) == ".":
                    moves += 1
                    new_grid.set(x, y, ".")
                    new_grid.set(x, next_y, "v")                    
                else:
                    new_grid.set(x,y,"v")
            elif herd == ">" and grid.get(x,y) == "v":
                new_grid.set(x,y,"v")
            elif herd == "v" and grid.get(x,y) == ">":
                new_grid.set(x,y,">")

    return new_grid, moves


def step(grid):
    """
    Do a full step of the simulation (update the grid with
    both herds)
    """
    grid, moves1 = half_step(grid, ">")
    grid, moves2 = half_step(grid, "v")

    return grid, moves1 + moves2


def solve(grid):
    """
    Find the step number when no moves take place.
    """
    num_steps = 1
    
    while True:
        grid, moves = step(grid)
        
        if moves == 0:
            return num_steps
        num_steps += 1


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.Grid.from_file("input/sample/25.in")
    input = util.Grid.from_file("input/25.in")

    print("TASK 1")
    util.call_and_print(solve, sample)
    util.call_and_print(solve, input)

