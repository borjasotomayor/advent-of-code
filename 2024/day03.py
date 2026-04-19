"""
Day 3
https://adventofcode.com/2024/day/3

The kind of problem where regexes come in very handy.
I actually got the regex right pretty quickly, and then
wasted a bunch of time on Part 2 because I (incorrectly)
assumed that we were supposed to process the strings one
line at a time (re-enabling the mul operation at the
start of each string).
"""

import util
import re

from util import log

# Regex with groups to capture the mul, do, and don't operations
# (and the operands of the mul operation)
#
# Produces something like this:
# [('mul(2,4)', '2', '4'), 
#  ("don't()", '', ''), 
#  ('mul(5,5)', '5', '5'), 
#  ('mul(11,8)', '11', '8'), 
#  ('do()', '', ''), 
#  ('mul(8,5)', '8', '5')]
MULT_COND_RE=r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"


def add_multiplications(program: str, conditionals: bool) -> int:
    """
    Given a program, add up the result of the "mul" operations.
    If conditionals is True, enable/disable the "mul" operator
    based on the "do()" and "don't" operators.
    """
    total = 0
    mul_enabled = True
    for m in re.finditer(MULT_COND_RE, program):
        op, a, b = m.groups()
        if conditionals and op == "do()":
            mul_enabled = True
        if conditionals and op == "don't()":
            mul_enabled = False  
        elif op.startswith("mul") and mul_enabled:
            total += int(a) * int(b)

    return total


if __name__ == "__main__":
    util.set_debug(False)

    sample1 = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
    sample2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
    input = util.read_strs("input/03.in", sep="\n")
    program = "".join(input)

    print("TASK 1")
    util.call_and_print(add_multiplications, sample1, False)
    util.call_and_print(add_multiplications, program, False)

    print("\nTASK 2")
    util.call_and_print(add_multiplications, sample2, True)
    util.call_and_print(add_multiplications, program, True)
