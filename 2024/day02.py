"""
Day 2
https://adventofcode.com/2024/day/2

This was a simple, but fun, problem to figure out. 
In part 2, I'm creating new lists for the sub-reports
(using slicing), which is kinda wasteful, but fine
in this problem given the length of the lists.
"""

import util
from itertools import pairwise

from util import log

def is_safe(report: list[int]) -> bool:
    """
    Checks if a report is safe
    """
    prev_diff = 0
    found_bad_level = False
    for a, b in pairwise(report):
        diff = b - a
        if not 1 <= abs(b-a) <= 3:
            return False
        
        # If we multiply the current difference and the previous difference,
        # and the result is negative, then the two numbers have different
        # signs. Vacuously true in the first iteration because we initialize
        # prev_diff to zero
        if diff * prev_diff < 0:
            return False
        
        prev_diff = diff
    return True
        

def count_safe_reports(reports: list[list[int]], dampener: bool) -> int:
    """
    Count the number of safe reports. If the dampener is active, we also
    check reports with an element removed (but only if the full report
    is unsafe, and we bail out if we determine a sub-report is safe)
    """
    total = 0
    for report in reports:
        if is_safe(report):
            total += 1
        elif dampener:
            # Check if removing an element from the report makes it safe
            found_safe = False
            for i, _ in enumerate(report):
                new_report = report[:i] + report[i+1:]
                if is_safe(new_report):
                    found_safe = True
                    break
            if found_safe:
                total += 1

    return total


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/02.in", sep="\n", sep2=" ")
    input = util.read_ints("input/02.in", sep="\n", sep2=" ")

    print("TASK 1")
    util.call_and_print(count_safe_reports, sample, False)
    util.call_and_print(count_safe_reports, input, False)

    print("\nTASK 2")
    util.call_and_print(count_safe_reports, sample, True)
    util.call_and_print(count_safe_reports, input, True)
