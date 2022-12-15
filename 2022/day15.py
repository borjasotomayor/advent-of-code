"""
Day 15
https://adventofcode.com/2022/day/15

1st star: 00:16:44
2nd star: 00:50:53

This was a pretty neat problem once you had the insight
that, for a given y, each scanner covers a range of
positions in x, and you just need to keep track of
those ranges, and not process every x position individually.
If you merge those ranges, it's easy to detect whether
they form a single continuous range, or whether there's
a gap (the distress beacon)

That said, my solution still takes ~20 seconds to run
on the actual input, so I suspect there's a much
more efficient solution to this.
"""

import util
import operator

from util import log


class Sensor:
    """
    Simple class for keeping track of sensor information
    """

    def __init__(self, sx, sy, bx, by):
        """
        Constructor.

        Parameters:
        - sx, sy: Sensor coordinates
        - bx, by: Beacon coordinates
        """
        self.x = sx
        self.y = sy

        self.range = abs(sx-bx) + abs(sy-by)

    def __repr__(self):
        return f"Sensor({self.x}, {self.y})"


def parse_input(input):
    """
    Parses the input and returns a list of Sensor objects
    and a set of beacon coordinates
    """
    sensors = []
    beacons = set()
    for sx, sy, bx, by in util.iter_parse(input, "Sensor at x={:d}, y={:d}: closest beacon is at x={:d}, y={:d}"):
        s = Sensor(sx, sy, bx, by)
        sensors.append(s)
        beacons.add((bx, by))

    return sensors, beacons


def merge(ranges):
    """
    Takes a list of intervals and merges as many of them as possible.
    For example:

    - (0, 5), (3, 7) becomes (0, 7)
    - (0, 5), (10, 12), (7, 9) becomes (0, 5), (7, 12)

    Based on https://learncodingfast.com/merge-intervals/
    (tweaked for readability, and to also merge contiguous 
    ranges, not just overlapping ranges)
    """
    if len(ranges) == 0 or len(ranges) == 1:
        return ranges

    ranges.sort(key=operator.itemgetter(0))
    result = [ranges[0]]
    for lb, ub in ranges[1:]:
        prev_lb, prev_ub = result[-1]

        if prev_ub >= lb-1:
            result[-1] = (prev_lb, max(prev_ub, ub))
        else:
            result.append((lb, ub))

    return result


def find_sensor_ranges(sensors, y, bound=None):
    """
    For a given y, find the ranges (in x) that
    are covered by any sensor. If a bound
    is provided, we won't consider ranges
    outside of [0, bound]
    """

    ranges = []
    for s in sensors:
        # If the difference between y and the
        # sensor's y is greater than the sensor's
        # range, then this sensor won't have any
        # coverage in this y coordinate.
        if abs(s.y - y) > s.range:
            continue

        # Find the lower and upper bound (in x)
        # that this sensor covers
        xdiff = s.range - abs(s.y-y)
        lb = s.x - xdiff
        ub = s.x + xdiff

        # If a bound has been provided, then
        # adjust the lower/upper bounds
        if bound is not None:
            lb = max(0, lb)
            ub = min(bound, ub)

        ranges.append((lb, ub))

    # Merge the ranges
    merged_ranges = merge(ranges)

    return merged_ranges


def find_nobeacon_positions(sensors, beacons, y):
    """
    Part 1: Given a y, find how many positions in that row
    can't contain a beacon.
    """

    # We find the sensor ranges
    sensor_ranges = find_sensor_ranges(sensors, y)
    
    # Part 1 is premised on there not being any positions
    # within range of the sensors that could contain
    # the distress beacon, so we should get just one
    # sensor range
    assert len(sensor_ranges) == 1
    lb, ub = sensor_ranges[0]

    n = ub - lb + 1

    # Subtract any known beacons
    for _, by in beacons:
        if by == y:
            n -= 1

    return n


def find_tuning_frequency(sensors, bound):
    """
    Part 2: Find the distress beacon and return its tuning frequency
    """

    for y in range(0, bound):
        sensor_ranges = find_sensor_ranges(sensors, y, bound=bound)

        if len(sensor_ranges) == 1:
            # If we only get a single continuous sensor range,
            # then the distress beacon isn't here
            continue
        
        # Otherwise, it's in the gap between the two sensors ranges.
        tx = sensor_ranges[0][1]+1

        return tx*4000000 + y


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/15.in", sep="\n")
    input = util.read_strs("input/15.in", sep="\n")

    sample_sensors, sample_beacons = parse_input(sample)
    sensors, beacons = parse_input(input)

    print("TASK 1")
    util.call_and_print(find_nobeacon_positions, sample_sensors, sample_beacons, 10)
    util.call_and_print(find_nobeacon_positions, sensors, beacons, 2000000)

    print("\nTASK 2")
    util.call_and_print(find_tuning_frequency, sample_sensors, 20)
    util.call_and_print(find_tuning_frequency, sensors, 4000000)
