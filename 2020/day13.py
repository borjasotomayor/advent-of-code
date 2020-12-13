"""
Day 13
https://adventofcode.com/2020/day/13

1st star: 00:09:16
2nd star: 00:46:54

Welp, this gave me flashbacks to Discrete Math in grad school.
The first star was simple enough but, for the second star,
I wasted a bunch of time trying to iterate over the possible
timestamps, before realizing this could be solved with the
Chinese Remainder Theorem. My original solution had a
janky CRT implementation, but I then learned that SymPy 
provides one, so I cleaned up my code to use that
instead.
"""

import util
import math
import sys
import re

from util import log
from sympy.ntheory.modular import crt


def task1(input):
    earliest = int(input[0])
    bus_ids = [int(x) for x in input[1].split(",") if x != "x"]

    # Find the bus times starting at the earliest time
    times = []
    for bus_id in bus_ids:
        next_time = (((earliest//bus_id)+1) * bus_id)
        times.append((next_time, bus_id))

    # Find the first bus
    next_time, bus_id = min(times)

    wait = next_time - earliest

    return wait * bus_id


def task2(input):
    ids = [(int(x), i) for i, x in enumerate(input[1].split(",")) if x != "x"]

    # Straightforward application of the Chinese Remainder Theorem
    primes = [x[0] for x in ids]
    remainders = [x[0] - x[1] for x in ids]

    N, _ = crt(primes, remainders)
    
    return N


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/13.in", sep="\n")
    input = util.read_strs("input/13.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
