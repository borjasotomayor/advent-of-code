"""
Day 9
https://adventofcode.com/2025/day/9

This is one of those problems where it almost feels like
I cheated because I used the shapely library to perform
all the geometry operations (without implementing any
sort of "is a polygon contained in another polygon"
algorithm). On the other hand, it was a neat exercise
on knowing how to find the right library for the job.
"""

import util
import itertools
import shapely

from util import log

def rect_area(p1: tuple[int, int], p2: tuple[int, int]) -> int:
    """
    Compute the area of one rectangle
    """
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)


def find_largest_area_points(points: list[tuple[int, int]]) -> int:
    """
    Given a list of points, computes the area of the
    largest rectangles described by any two points
    """
    largest_points = None
    largest_area = 0
    for p1, p2 in itertools.combinations(points, 2):
        area = rect_area(p1, p2)
        if area > largest_area:
            largest_points = (p1, p2)
            largest_area = area

    log(f"Largest: {largest_points} (area: {largest_area})")

    return largest_area

    
def find_largest_area_polygon(points: list[tuple[int, int]]) -> int:
    """
    Given a polygon, find the rectangle described by two
    points on the polygon that has the largest area
    """

    poly = shapely.Polygon(points)

    largest_points = None
    largest_area = 0
    for p1, p2 in itertools.combinations(points, 2):
        # Create a rectangle described by the two points
        rect = shapely.box(
            xmin=min(p1[0], p2[0]), xmax=max(p1[0], p2[0]),
            ymin=min(p1[1], p2[1]), ymax=max(p1[1], p2[1]))
            
        area = rect_area(p1, p2)

        if area > largest_area and poly.contains(rect):
            largest_points = (p1, p2)
            largest_area = area

    log(f"Largest: {largest_points} (area: {largest_area})")

    return largest_area


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/09.in", sep="\n", sep2=",")
    input = util.read_ints("input/09.in", sep="\n", sep2=",")

    sample_points = [tuple(p) for p in sample]
    input_points = [tuple(p) for p in input]

    print("TASK 1")
    util.call_and_print(find_largest_area_points, sample_points)
    util.call_and_print(find_largest_area_points, input_points)

    print("\nTASK 2")
    util.call_and_print(find_largest_area_polygon, sample_points)
    util.call_and_print(find_largest_area_polygon, input_points)
