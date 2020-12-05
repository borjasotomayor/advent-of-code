"""
Day 2
https://adventofcode.com/2020/day/2

1st star: 00:05:17
2nd star: 00:10:15

This is pretty close to what I wrote on Day 2; I only cleaned up
the 'parsing' of each line, which was originally much jankier.
"""

import util
import math

def task1(passwords):
    valid = 0

    for s in passwords:
        bounds, letter, password = s.strip().split()

        lb, ub = (int(x) for x in bounds.split("-"))

        letter = letter[0]

        count = password.count(letter)

        if lb <= count <= ub:
            valid += 1

    return valid


def task2(passwords):
    valid = 0

    for s in passwords:
        indices, letter, password = s.strip().split()

        i, j = (int(x) for x in indices.split("-"))

        letter = letter[0]

        li = password[i-1]
        lj = password[j-1]

        # Really wish Python had an "xor" operator
        if (li == letter or lj == letter) and not (li == letter and lj == letter):
            valid += 1

    return valid


if __name__ == "__main__":
    sample = util.read_strs("input/sample/02.in", sep="\n")
    passwords = util.read_strs("input/02.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, passwords)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, passwords)
