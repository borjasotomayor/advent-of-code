"""
Day 13
https://adventofcode.com/2021/day/13

1st star: 00:18:43
2nd star: 00:21:19

This was a very satisfying problem to do with NumPy, which makes it
very easy to extract subarrays from a larger array, and even includes
methods to flip arrays easily.
"""

import util
import math
import sys
import re

from util import log

import numpy as np


def fold_paper(paper, folds, times=None):
    """
    Fold a paper according to the given folds, up to a number of times
    (if times is None, just do all the folds)
    """

    folded = 0
    for dim, v in folds:
        if dim == "y":
            top = paper[:v]
            bottom = paper[v+1:]

            paper = top + np.flipud(bottom)
        elif dim == "x":
            left = paper[:, :v]
            right = paper[:, v+1:]

            paper = left + np.fliplr(right)

        folded += 1
        if times is not None and folded >= times:
            break

    # Turns all non-zero values to ones, to make it easier
    # to manipulate later on.
    paper[paper != 0] = 1

    return paper


def read_input(input):
    """
    Read the input. Returns a numpy array, and a list of (dimension, value)
    pairs specifying the folds.
    """
    dots_lines, folds_lines = input

    dots_lines = dots_lines.split()
    dots = [(x, y) for x, y in util.iter_parse(dots_lines, "{:d},{:d}")]

    max_x = max(x for x, _ in dots)
    max_y = max(y for _, y in dots)

    paper = np.zeros((max_y+1, max_x+1), dtype=np.int8)
    for x, y in dots:
        paper[y][x] = 1

    folds_lines = folds_lines.split("\n")
    folds = [(dim, v) for dim, v in util.iter_parse(folds_lines, "fold along {}={:d}")]

    return paper, folds


def task1(input):
    """
    Task 1: Fold once and count the dots.
    """
    paper, folds = read_input(input)
    folded_paper = fold_paper(paper, folds, times=1)
    return folded_paper.sum()


def task2(input):
    """
    Task 2: Do all the folds, and return a string representation
    of the folded paper.
    """
    paper, folds = read_input(input)
    folded_paper = fold_paper(paper, folds)
    return np.array2string(folded_paper, separator="",
                           formatter={"int": lambda x: "#" if x == 1 else " "})


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/13.in", sep="\n\n")
    input = util.read_strs("input/13.in", sep="\n\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    print(task2(sample))
    print(task2(input))
