"""
Day 22
https://adventofcode.com/2022/day/22

1st star: 01:15:46	
2nd star: 02:45:48

Welp, that was painful.

In Part 1, I moved fairly quickly thanks to my existing Grid 
and Direction classes, which meant I already had code for 
moving a long a grid in a given direction *and* for rotating 
that direction.

For Part 2, I basically gave up any pretension of coming up
with a general solution that can fold any cube, and instead
focused on the layout of the input, painstakingly figuring out
how each edge would wrap to another edge. So, the solution below
won't work with the sample input, but it *should* work with
other inputs where the cube sides are laid out the same way.

Like a lot of people, I ended up crafting an actual cube so
I could get all the wrapping correct. You can see a picture
here: https://redd.it/zsg87q
"""

import util
from copy import copy


# We use the util.Direction class to represent
# the direction we're moving in
DIR_RIGHT = util.Direction.RIGHT()
DIR_LEFT = util.Direction.LEFT()

# The up/down directions are reversed because 
# Direction uses cartesian coordinates, where "up" 
# increments y by 1.
DIR_UP = util.Direction.DOWN()
DIR_DOWN = util.Direction.UP()


def read_input(filename):
    """
    Reads the input and returns a grid with the full
    contents of the input (including blank spaces),
    as well as a list of (step, rotate) pairs.
    """
    with open(filename) as f:
        txt = f.read()
    
    grid_string, path_string = txt.split(sep="\n\n")  
    grid_lines = grid_string.split("\n")

    # We need to make sure we pad all the lines
    # so they have the same length
    # (not strictly necessary, but makes working
    # with the grid easier)
    max_len = max(len(s) for s in grid_lines)
    for i, s in enumerate(grid_lines):
        grid_lines[i] = s.ljust(max_len, " ")

    grid = util.Grid._from_lines(grid_lines)

    # Parse the path
    path = []
    cur_num = []
    for c in path_string:
        if c.isnumeric():
            cur_num.append(c)
        else:
            path.append((int("".join(cur_num)), c))
            cur_num = []

    # Make sure to add the trailing number!
    path.append((int("".join(cur_num)), None))    

    return grid, path


def find_start_position(grid):
    """
    Find the starting position on the grid
    """
    for x in range(grid.max_x):
        if grid.get(x, 0) != " ":
            return (x, 0)


def compute_wrap_locations_2d(grid):
    """
    Find the locations we will wrap around to in the 2-dimensional grid.

    Returns a dictionary that maps a Direction object (right, left, up, or down)
    and either an x value (if we're moving up or down) or a y value (if we're
    moving left or right) to the coordinates and direction we would wrap around to.
    """
    wrap = {}
    wrap[DIR_RIGHT] = {}
    wrap[DIR_LEFT] = {}
    wrap[DIR_UP] = {}
    wrap[DIR_DOWN] = {}

    for y in range(grid.max_y):
        # Moving right
        for x in range(grid.max_x):
            if grid.get(x, y) != " ":
                wrap[DIR_RIGHT][y] = (x, y, DIR_RIGHT)
                break
        # Moving left
        for x in range(grid.max_x-1, -1, -1):
            if grid.get(x, y) != " ":
                wrap[DIR_LEFT][y] = (x, y, DIR_LEFT)
                break

    for x in range(grid.max_x):
        # Moving down
        for y in range(grid.max_y):
            if grid.get(x, y) != " ":
                wrap[DIR_DOWN][x] = (x, y, DIR_DOWN)
                break
        # Moving up
        for y in range(grid.max_y-1,-1,-1):
            if grid.get(x, y) != " ":
                wrap[DIR_UP][x] = (x, y, DIR_UP)
                break

    return wrap


def compute_wrap_locations_3d(grid):
    """
    Find the locations we will wrap around to in the cube.

    This *only* works with the actual input (not with the sample input),
    and assumes that the cube edges are laid out like this:

            AAAABBBB
            AAAABBBB
            AAAABBBB
            AAAABBBB
            CCCC
            CCCC
            CCCC
            CCCC
        DDDDEEEE
        DDDDEEEE
        DDDDEEEE
        DDDDEEEE
        FFFF
        FFFF
        FFFF
        FFFF
    
    Returns a dictionary that maps a Direction object (right, left, up, or down)
    and either an x value (if we're moving up or down) or a y value (if we're
    moving left or right) to the coordinates and direction we would wrap around to.
    """

    wrap = {}
    wrap[DIR_RIGHT] = {}
    wrap[DIR_LEFT] = {}
    wrap[DIR_UP] = {}
    wrap[DIR_DOWN] = {}

    for x in range(0, 50):
        # D -> C
        wrap[DIR_UP][x] = (50, x+50, DIR_RIGHT)
        # F -> B
        wrap[DIR_DOWN][x] = (x+100, 0, DIR_DOWN)

    for x in range(50, 100):
        # A -> F
        wrap[DIR_UP][x] = (0, x+100, DIR_RIGHT)
        # E -> F
        wrap[DIR_DOWN][x] = (49, x+100, DIR_LEFT)

    for x in range(100, 150):
        # B -> F
        wrap[DIR_UP][x] = (x-100, 199, DIR_UP)
        # B -> C    
        wrap[DIR_DOWN][x] = (99, x-50, DIR_LEFT)
    
    for y in range(0, 50):
        # A -> D
        wrap[DIR_LEFT][y] = (0, 149 - y, DIR_RIGHT)
        # B -> E
        wrap[DIR_RIGHT][y] = (99, 149 - y, DIR_LEFT)
    
    for y in range(50, 100):
        # C -> D
        wrap[DIR_LEFT][y] = (y-50, 100, DIR_DOWN)
        # C -> B
        wrap[DIR_RIGHT][y] = (y+50, 49, DIR_UP)

    for y in range(100, 150):
        # D -> A
        wrap[DIR_LEFT][y] = (50, 149-y, DIR_RIGHT)
        # E -> B
        wrap[DIR_RIGHT][y] = (149, 149-y, DIR_LEFT)

    for y in range(150, 200):
        # F -> A
        wrap[DIR_LEFT][y] = (y-100, 0, DIR_DOWN)
        # F -> E
        wrap[DIR_RIGHT][y] = (y-100, 149, DIR_UP)

    return wrap


def follow_path(grid, path, cube=False):
    """
    Given a grid and a path, follow the path.
    """

    if cube:
        wrap = compute_wrap_locations_3d(grid)
    else:
        wrap = compute_wrap_locations_2d(grid)
    
    cur_x, cur_y = find_start_position(grid)

    cur_dir = util.Direction.RIGHT()

    for steps, rotate in path:
        for _ in range(steps):
            # Move in the current direction
            next_x, next_y = cur_dir.move_grid_coordinates(cur_x, cur_y)
            
            # See what's in that position
            v = grid.getdefault(next_x, next_y)

            # If it's a blank space or if we've gone past the bounds
            # of the grid, we need to wrap around
            if v == " " or v is None:
                if cur_dir in (DIR_RIGHT, DIR_LEFT):
                    next_x, next_y, next_dir = wrap[cur_dir][next_y]
                elif cur_dir in (DIR_UP, DIR_DOWN):
                    next_x, next_y, next_dir = wrap[cur_dir][next_x]
                next_dir = copy(next_dir)
                v = grid.get(next_x, next_y)
            else:
                next_dir = cur_dir

            if v == ".":
                # If there's an empty space, we move to it
                cur_x, cur_y, cur_dir = next_x, next_y, next_dir
            elif v == "#":
                # If there's a wall, we stay put
                break

        if rotate == "L":
            cur_dir.rotate_clockwise(90)
        elif rotate == "R":
            cur_dir.rotate_counterclockwise(90)

    # Compute the return value
    col = cur_x+1
    row = cur_y+1
    
    if cur_dir == DIR_RIGHT:
        d = 0
    elif cur_dir == DIR_UP:
        d = 1
    elif cur_dir == DIR_LEFT:
        d = 2
    elif cur_dir == DIR_DOWN:
        d = 3

    return 1000*row + 4*col + d


if __name__ == "__main__":
    util.set_debug(False)

    sample_grid, sample_path = read_input("input/sample/22.in")
    grid, path = read_input("input/22.in")

    print("TASK 1")
    util.call_and_print(follow_path, sample_grid, sample_path)
    util.call_and_print(follow_path, grid, path)

    print("\nTASK 2")
    util.call_and_print(follow_path, grid, path, True)
