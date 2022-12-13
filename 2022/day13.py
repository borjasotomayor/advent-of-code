"""
Day 13
https://adventofcode.com/2022/day/13

1st star: 00:15:11
2nd star: 00:22:05

This was a really fun problem where a design decision in
Part 1 turned out to be a really good call in Part2.
I basically approached it as implementing a "cmp" function
from the get-go, which made implementing Part 2 pretty
straightforward (except I didn't realize Python 3 had
nuked the "cmp" parameter in sort(), so I had to learn
about cmp_to_key on the fly)
"""

import util
from functools import cmp_to_key

from util import log

def cmp(l1, l2):
    """
    Comparison function for comparing two lists
    Returns:
      -1: l1 < l2 ("l1 and l2 are in the right order")
       0: l1 == l2
       1: l1 > l2 ("l1 and l2 are in the wrong order")
    """
    
    for e1, e2 in zip(l1, l2):
        if isinstance(e1, int) and isinstance(e2, int):
            if e1 < e2:
                return -1
            elif e1 > e2:
                return 1
        elif isinstance(e1, list) and isinstance(e2, list):
            c = cmp(e1, e2)
            if c != 0:
                return c
        elif isinstance(e1, list) and isinstance(e2, int):
            c = cmp(e1, [e2])
            if c != 0:
                return c
        elif isinstance(e1, int) and isinstance(e2, list):
            c = cmp([e1], e2)
            if c != 0:
                return c

    if len(l1) < len(l2):
        return -1
    elif len(l1) > len(l2):
        return 1
    else:
        return 0


def task1(pairs):
    """
    Task 1: Add up the indices of the packets that are in
    the right order
    """
    right_order = 0
    for i, (l1, l2) in enumerate(pairs):
        if cmp(l1, l2) == -1:
            right_order += i+1

    return right_order


DIVIDER1 = [[2]]
DIVIDER2 = [[6]]

def task2(pairs):
    """
    Task 2: Sort all the lists, and return the product of 
    the indices of the "dividers"
    """

    all_lists = []
    for p in pairs:
        all_lists += p

    all_lists.append(DIVIDER1)
    all_lists.append(DIVIDER2)

    all_lists.sort(key=cmp_to_key(cmp))

    return (all_lists.index(DIVIDER1) + 1) * (all_lists.index(DIVIDER2) + 1)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/13.in", sep="\n\n", sep2="\n")
    input = util.read_strs("input/13.in", sep="\n\n", sep2="\n")

    sample_pairs = [(eval(l1), eval(l2)) for l1, l2 in sample]
    input_pairs = [(eval(l1), eval(l2)) for l1, l2 in input]

    print("TASK 1")
    util.call_and_print(task1, sample_pairs)
    util.call_and_print(task1, input_pairs)

    print("\nTASK 2")
    util.call_and_print(task2, sample_pairs)
    util.call_and_print(task2, input_pairs)
