"""
Day 6
https://adventofcode.com/2021/day/6

1st star: 00:06:29
2nd star: 00:17:47

Because I love me a good discrete event simulation, my implementation for
the first task involved actually keeping track of the list of fishes
each day (which, in the back of my head, I just KNEW would come back 
to bite me in task 2) 

Sure enough, had to rewrite my entire solution for Task 2, because keeping
track of a list with 20-billion integers is maybe a bit too much. Also,
I'm glad I didn't go with my initial intuition of trying to exploit the fact
that the sequences repeat periodically. Nope, just had to count stuff with 
dictionaries.
"""

import util
import math
import sys
import re

from util import log


def count_fishes(initial_fishes, days):
    """
    Counts the number of fishes after a number of days
    """

    # Load initial fishes
    fishes = {}
    for x in initial_fishes:
        fishes[x] = fishes.get(x, 0) + 1
   
    for _ in range(days):
        new_fishes = {x:0 for x in range(0,9)}

        for timer, n in fishes.items():
            if timer == 0:
                new_fishes[8] += n
                new_fishes[6] += n
            else:
                new_fishes[timer-1] += n

        fishes = new_fishes

    return sum(v for v in fishes.values())


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/06.in", sep=",")
    input = util.read_ints("input/06.in", sep=",")

    print("TASK 1")
    util.call_and_print(count_fishes, sample, 80)
    util.call_and_print(count_fishes, input, 80)

    print("\nTASK 2")
    util.call_and_print(count_fishes, sample, 256)
    util.call_and_print(count_fishes, input, 256)
