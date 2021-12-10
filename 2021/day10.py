"""
Day 10
https://adventofcode.com/2021/day/10

1st star: 00:08:58
2nd star: 00:16:27

This was a fun little problem if you're familiar with the various uses
of stacks. My original code was a tangled mess of if-else's where I was
checking for individual characters in lots of places, so this also became
a nice exercise in refactoring.
"""

import util
import math
import sys
import re

from util import log


# We define a couple of handy dictionaries

SCORE_CORRUPT = {")": 3, 
                 "]": 57,
                 "}": 1197,
                 ">": 25137}

SCORE_INCOMPLETE = {")": 1, 
                    "]": 2,
                    "}": 3,
                    ">": 4}

FLIP = {"{": "}",
        "(": ")",
        "[": "]",
        "<": ">",
        "}": "{",
        ")": "(",
        "]": "[",
        ">": "<"}


def compute_single_score(line, corrupt_only):
    """
    Computes the score for a single line.

    If corrupt_only is True, returns a score if the line is corrupt, 
    and None if it is incomplete. 
    
    If corrupt_only is False, returns a score if the line is incomplete,
    and None if it is corrupt.
    """

    # Check for unbalanced symbols using a stack
    stack = []
    for c in line:
        if c in ("(", "[", "{", "<"):
            stack.append(c)
        elif c in (")", "]", "}", ">"):
            top = stack.pop()

            # Unbalanced symbol!
            if top != FLIP[c]:
                if corrupt_only:
                    return SCORE_CORRUPT[c]
                else:
                    return None

    assert len(stack) != 0

    if corrupt_only:
        return None

    # Compute missing characters       
    missing = []
    for c in stack[::-1]:
        missing.append(FLIP[c])

    # Compute score
    score = 0
    for c in missing:
        score = 5*score + SCORE_INCOMPLETE[c]

    return score


def compute_scores(lines, corrupt_only):
    """
    Generate a list of scores (one per line, skipping incomplete
    lines when corrupt_only is True, and skipping corrupt lines when
    corrupt_only is False)
    """
    scores = []
    for line in lines:
        score = compute_single_score(line, corrupt_only)
        if score is not None:
            scores.append(score)
    
    return scores


def task1(input):
    """
    Compute the score of the corrupt lines and return the sum
    """
    scores = compute_scores(input, corrupt_only=True)
    return sum(scores)
    

def task2(input):
    """
    Compute the score of the incomplete lines and return the median
    """
    scores = compute_scores(input, corrupt_only=False)
    scores.sort()
    return scores[len(scores)//2]


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/10.in", sep="\n")
    input = util.read_strs("input/10.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
