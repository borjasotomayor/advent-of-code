"""
Day 20
https://adventofcode.com/2021/day/20

1st star: 11:42:34 (*)
2nd star: 11:45:12 (*)

(*) I was on vacation when this problem was solved, so I wasn't 
    able to solve it right when it was released. 

NumPy to the rescue again! If only it could have rescued me
from that devious input...
"""

import util
import math
import numpy as np

from util import log


def apply_algorithm(algorithm, image, infinity):
    """
    Apply the algorithm to the image, assuming that the values
    outside the image are "infinity" (""0" for dark pixels,
    "1" for light pixels)"
    """

    # Pad the image with a border of width 2, and use
    # the "infinity" value in the pad. We also convert
    # the array to a string array to make it easier
    pimage = np.pad(image, 2, constant_values=infinity)

    # We will be filling in this array
    output = []

    # Compute the value of each position of the output image
    for i in range(1,pimage.shape[0]-1):
        row = []
        for j in range(1,pimage.shape[1]-1):
            subarray = pimage[i-1:i+2, j-1:j+2]
            bin_str = "".join("".join(row) for row in subarray)

            index = int(bin_str, 2)
            row.append("1" if algorithm[index] == "#" else "0")
        output.append(row)

    output = np.array(output)

    # We return the output image, and the new value for infinity
    # (any value in the border of the image would do)
    return output, output[0][0]


def enhance(algorithm, image, n):
    """
    Apply the algorithm to the image n times
    """

    infinity = "0"
    for _ in range(n):
        image, infinity = apply_algorithm(algorithm, image, infinity)

    return image.astype(np.int8).sum()


def read_input(input):
    """
    Read the input. We convert the image to a NumPy array of string 0's and
    1's to make it easier to create the binary numbers (and to perform the
    final sum)
    """
    algorithm, image_lines = input

    array = []
    for line in image_lines.split("\n"):
        row = []
        for char in line:
            row.append("1" if char == "#" else "0")
        array.append(row)

    return algorithm, np.array(array)


def task1(input):
    """
    Task 1: Apply the algorithm two times
    """
    algorithm, image = read_input(input)
    return enhance(algorithm, image, 2)


def task2(input):
    """
    Task 2: Apply the algorithm 50 times
    """
    algorithm, image = read_input(input)
    return enhance(algorithm, image, 50)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/20.in", sep="\n\n")
    input = util.read_strs("input/20.in", sep="\n\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
