"""
Day 1
https://adventofcode.com/2020/day/1

1st star: 00:07:01 (*)
2nd star: 00:09:34

This solution is basically the one I wrote on Day 1.
I used list slicing to keep things a bit cleaner, but if the cost of
copying the lists (via slicing) had been a bottleneck, I would've
used for + range() (even though I really dislike doing so in Python)

(*) There was an outage during the day 1 puzzle unlock. I wrote
the code for the first star in around 1-2 minutes, but wasn't able
to submit until the outage was resolved.
"""

import util
import math

def task1(numbers):
    for i, x in enumerate(numbers):
        for y in numbers[i+1:]:
                if x + y == 2020:
                    return x*y

def task2(numbers):
    for i, x in enumerate(numbers):
        for y in numbers[i+1:]:
            for z in numbers[i+2:]:
                if x + y + z == 2020:
                    return x*y*z


if __name__ == "__main__":
    nums = util.read_ints("input/01.in")
    sample = [1721, 979, 366, 299, 675, 1456]

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, nums)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, nums)
