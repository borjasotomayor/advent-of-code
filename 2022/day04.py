"""
Day 4
https://adventofcode.com/2022/day/4

1st star: 00:05:26
2nd star: 00:08:51

I briefly flirted with the idea of solving this with sets, but
bet on Part II being solvable just by checking the limits of
the ranges, and the bet paid of. The solution below is fairly
similar to the one I wrote originally, except I had to nearly
identical functions that I refactored into a single function.
"""

import util
import math
import sys
import re

from util import log

# Format string for parsing each line
PAIRS_FMT = "{:d}-{:d},{:d}-{:d}"

def find_overlaps(section_assignments):
    """
    Given a list of pairs of ranges, finds the number of pairs
    that overlap completely and the number of pairs that overlap
    (not necessarily completely)
    """
    fully_overlap = 0
    dont_overlap = 0

    for lb1, ub1, lb2, ub2 in util.iter_parse(section_assignments, PAIRS_FMT):
        if (lb2 <= lb1 <= ub1 <= ub2) or (lb1 <= lb2 <= ub2 <= ub1):
            # Either [lb1-ub1] is fully contained inside [lb2-ub2], or viceversa
            fully_overlap += 1
        elif (ub1 < lb2) or (lb1 > ub2):
            # [lb1-ub1] is either strictly before or after [lb2-ub2]
            dont_overlap += 1

    some_overlap = len(section_assignments) - dont_overlap
    
    return fully_overlap, some_overlap


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/04.in", sep="\n")
    input = util.read_strs("input/04.in", sep="\n")

    print("TASK 1 and 2")
    util.call_and_print(find_overlaps, sample)
    util.call_and_print(find_overlaps, input)
