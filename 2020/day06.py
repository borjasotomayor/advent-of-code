"""
Day 6
https://adventofcode.com/2020/day/6

1st star: 00:06:22
2nd star: 00:08:58

This was pretty straightforward to do if your language of choice has
good support for sets, and you're comfortable with set operations
(I can imagine the code getting pretty hairy if you have to do all
the set operations manually).

The code below is pretty close to what I wrote originally, modulo some
basic cleaning up.
"""

import util
import math
import sys
import re
import string

from util import log


def task1(groups):
    count = 0

    for group in groups:
        unique_questions = set()
        for answers in group.split():
            unique_questions.update(answers)
        count += len(unique_questions)
        log(unique_questions, count)

    return count


def task2(groups):
    count = 0
    
    for group in groups:
        unique_questions = set(string.ascii_lowercase)
        for answers in group.split():
            unique_questions.intersection_update(answers)
        count += len(unique_questions)
        log(unique_questions, count)

    return count


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/06.in", sep="\n\n")
    input = util.read_strs("input/06.in", sep="\n\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
