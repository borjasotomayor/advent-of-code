"""
Day 1
https://adventofcode.com/2023/day/1

1st star: 00:03:10
2nd star: 00:24:17

The first part of the problem was, as usual, pretty easy.
Also as usual, I expected the second part to be some minor
twist that could be solved in 2-3 minutes.

I was wrong :-P

I ended up going down the path of solving a much more
general problem (replacing all the text-digits in a string),
which gets hairy because some of the substrings you need
to replace can overlap (e.g, "eightwone" -> "821"). My
original solution included some kludgy substitutions like
("twone", "21"), ("eightwo", "82"), etc. that were
fortunately enough to solve the problem (there didn't
seem to be more than two overlapping digits at a time)

The solution below is a more polished solution that should
work even if there are arbitrarily long chains of overlapping
text-digits (but it is slightly inefficient, and only works
when the strings overlap at most in one characted, which
is true here).

Of course, someone then pointed out that a much simpler solution is
to just search for one digit from the start of the string,
and another from the end of the string, instead of trying
to replace all of them. *facepalm*
"""

import util
import math
import sys
import re

from util import log


def calibration_values(strings: list[str]) -> int:
    """
    Given a list of strings, extract the digits in
    that string, and then find the calibration
    value (the two-digit number resulting from the
    first and last digit)
    """
    total = 0
    for string in strings:
        numbers = []
        for char in string:
            if char.isnumeric():
                numbers.append(int(char))
        number = numbers[0]*10 + numbers[-1]
        total += number

    return total


DIGITS = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5",
          "six": "6", "seven": "7", "eight": "8", "nine": "9"}


def check_for_digit(string: str, pos: int) -> tuple[str, str] | None:
    """
    Check whether a string has a text-digit at a given position
    (if so, returns the text-digit and its number representation)
    """
    for text_digit in DIGITS:
        if string[pos:pos + len(text_digit)] == text_digit:
            return text_digit, DIGITS[text_digit]
    return None


def replace_digits(string: str) -> str:
    """
    Given a string with text-digits in it ("one", "two", ...)
    replace the text with numbers, taking into account that some
    text-digits overlap in their first/last characters
    (e.g., "eight" + "two" == "eightwo")
    """

    new_s = ""
    i = 0
    while i < len(string):
        # Check for a digit in the current position
        check = check_for_digit(string, i)

        if check is None:
            # If there is no digit, advance to the next index
            new_s += string[i]
            i += 1
        else:
            # If there is a digit, check whether there is another
            # digit starting at the last character of this digit
            text_digit, number = check
            new_s += number
            check = check_for_digit(string, i + len(text_digit) - 1)

            # If there is no other digit, advance past the current digit
            if check is None:
                i += len(text_digit)
            else:
                # If there is another digit, we advance to the position
                # where that digit starts, and it will be caught at
                # the top of the loop
                # This is slightly inefficient because we're calling
                # check_for_digit twice on the same position.
                i += len(text_digit) - 1

    return new_s


def task2(strings: list[str]) -> int:
    """
    Task 2: Before computing the calibration values,
    replace text-digits in the string
    """
    new_strings = [replace_digits(string) for string in strings]
    return calibration_values(new_strings)


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = util.read_strs("input/sample/01-1.in", sep="\n")
    sample2 = util.read_strs("input/sample/01-2.in", sep="\n")
    input = util.read_strs("input/01.in", sep="\n")

    print("TASK 1")
    util.call_and_print(calibration_values, sample1)
    util.call_and_print(calibration_values, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample2)
    util.call_and_print(task2, input)
