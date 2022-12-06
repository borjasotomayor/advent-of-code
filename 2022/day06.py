"""
Day 6
https://adventofcode.com/2022/day/6

1st star: 00:02:36
2nd star: 00:03:19

Did I mention how much I love Python sets? This had
such a quick and satisfying solution. The code
below is essentially the same I wrote originally
(all I did was refactor it into a function that takes
the marker size as a parameter)
"""

import util
import math
import sys
import re

from util import log


def find_marker(message, marker_size):
    """
    Find the index of the last character of the marker
    (a run of marker_size non-repeated characters).

    We do this by generating every substring of size
    marker_size, converting it to a set, and checking
    whether the set has size marker_size (if it does,
    then there were no repeated characters)
    """
    for i in range(0, len(message) - marker_size):
        cmd = message[i:i+marker_size]
        if len(set(cmd)) == marker_size:
            return i + marker_size


if __name__ == "__main__":
    util.set_debug(False)

    input = util.read_strs("input/06.in", sep="\n")[0]

    print("TASK 1")
    util.call_and_print(find_marker, "mjqjpqmgbljsphdztnvjfqwrcgsmlb", 4)
    util.call_and_print(find_marker, "bvwbjplbgvbhsrlpgdmjqwftvncz", 4)
    util.call_and_print(find_marker, "nppdvjthqldpwncqszvftbrmjlhg", 4)
    util.call_and_print(find_marker, "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 4)
    util.call_and_print(find_marker, "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 4)
    util.call_and_print(find_marker, input, 4)

    print("\nTASK 2")
    util.call_and_print(find_marker, "mjqjpqmgbljsphdztnvjfqwrcgsmlb", 14)
    util.call_and_print(find_marker, "bvwbjplbgvbhsrlpgdmjqwftvncz", 14)
    util.call_and_print(find_marker, "nppdvjthqldpwncqszvftbrmjlhg", 14)
    util.call_and_print(find_marker, "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg", 14)
    util.call_and_print(find_marker, "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw", 14)
    util.call_and_print(find_marker, input, 14)
