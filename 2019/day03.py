"""
Day 3
https://adventofcode.com/2019/day/3

1st star: 00:26:01
2nd star: 00:34:59

This was a fun problem once you realize that the "grid" is a bit of a
red herring, and that trying to create an actual grid can make the
solution much more complicated than it needs to be (similarly, no
need to do anything as fancy as computing individual segments and
checking whether they intersect on a plane). Instead, simply
keep track of the coordinates that a wire goes through (using a set).
Finding the points where the wire intersect then becomes as easy
as getting the intersection of two sets.
"""

import util

def get_wire_coordinates(dirs):
    """
    Computes all the grid coordinates that the wire goes through

    Args:
        dirs (list of strings): The sequence of directions
        followed by the wire (e.g., "R8", "U5")

    Returns:
        set of (int, int): set of coordinates the wire goes through
    """
    coords = set()

    # x, y represent our current coordinates
    # The wire always starts at (0, 0)
    x, y = (0, 0)

    for dir in dirs:
        # The first character of the string is the direction
        d = dir[0]

        # The remainder of the string is the amount
        a = int(dir[1:])

        # Update the current coordinates according to the
        # given direction, and adding a new coordinate pair
        # to the coords set as we go along
        if d == "R":
            for _ in range(a):
                y += 1
                coords.add((x,y))
        if d == "L":
            for _ in range(a):
                y -= 1
                coords.add((x,y))
        if d == "U":
            for _ in range(a):
                x += 1
                coords.add((x,y))
        if d == "D":
            for _ in range(a):
                x -= 1
                coords.add((x,y))

    return coords

def trace(dirs, tx, ty):
    """
    Starting at the origin, trace a wire until we reach
    the target coordinated

    Args:
        dirs (list of strings): The sequence of directions
        followed by the wire (e.g., "R8", "U5")
        tx, ty (int): Target coordinates

    Returns:
        int: Number of steps
    """

    # x, y represent our current coordinates
    # The wire always starts at (0, 0)
    x, y = (0, 0)
    
    steps = 0
    for dir in dirs:
        # The first character of the string is the direction        
        d = dir[0]

        # The remainder of the string is the amount
        a = int(dir[1:])

        # Update the current coordinates according to the
        # given direction, incrementing the number of steps.
        # Stop if we reach the target coordinates.
        if d == "R":
            for _ in range(a):
                y += 1
                steps += 1
                if x == tx and y == ty:
                    return steps
        if d == "L":
            for _ in range(a):
                y -= 1
                steps += 1
                if x == tx and y == ty:
                    return steps
        if d == "U":
            for _ in range(a):
                x += 1
                steps += 1
                if x == tx and y == ty:
                    return steps
        if d == "D":
            for _ in range(a):
                x -= 1
                steps += 1
                if x == tx and y == ty:
                    return steps


def wires_intersect(dirs1, dirs2):
    """
    Find the coordinates where two wires intersect.

    Args:
        dirs1, dirs2 (list of strings): The sequence of directions
        followed by the wire (e.g., "R8", "U5")

    Returns:
        set of (int, int): set of coordinates the wires intersect
    """

    # Get the coordinates for each wire
    coords1 = get_wire_coordinates(dirs1)
    coords2 = get_wire_coordinates(dirs2)

    # The intersection of both sets tells us where
    # the wires intersect
    common = coords2.intersection(coords1)
    
    return common


def manhattan(x, y):
    """
    Compute the Manhattan Distance from x, y to 0, 0
    """
    return abs(0-x) + abs(0-y)


def task1(wire1, wire2):
    """
    Find where two writes intersect, and find the intersection
    point that is closest to the origin (by Manhattan distance)

    The wires are given in the format described in the problem
    (a single comma-separated string)
    """

    dirs1 = wire1.split(",")
    dirs2 = wire2.split(",")

    common = wires_intersect(dirs1, dirs2)
    
    smallest = None
    for x, y in common:
        d = manhattan(x, y)
        if smallest is None or d < smallest:
            smallest = d

    return smallest


def task2(wire1, wire2):
    """
    Find where two writes intersect. For each intersection,
    find the number of steps it takes to get from the origin
    to the intersection in each wire, and compute the sum.
    Return the smallest such sum.

    The wires are given in the format described in the problem
    (a single comma-separated string)    
    """

    dirs1 = wire1.split(",")
    dirs2 = wire2.split(",")

    common = wires_intersect(dirs1, dirs2)

    smallest_steps = None
    for x, y in common:
        steps1 = trace(dirs1, x, y)
        steps2 = trace(dirs2, x, y)
        total_steps = steps1 + steps2
        if smallest_steps is None or total_steps < smallest_steps:
            smallest_steps = total_steps

    return smallest_steps


if __name__ == "__main__":
    wire1, wire2 = util.read_strs("input/03.in")

    sample1_wire1 = "R75,D30,R83,U83,L12,D49,R71,U7,L72"
    sample1_wire2 = "U62,R66,U55,R34,D71,R55,D58,R83"

    sample2_wire1 = "R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"
    sample2_wire2 = "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"

    print("TASK 1")
    util.call_and_print(task1, sample1_wire1, sample1_wire2)
    util.call_and_print(task1, sample2_wire1, sample2_wire2)
    util.call_and_print(task1, wire1, wire2)

    print("\nTASK 2")
    util.call_and_print(task2, sample1_wire1, sample1_wire2)
    util.call_and_print(task2, sample2_wire1, sample2_wire2)
    util.call_and_print(task2, wire1, wire2)
