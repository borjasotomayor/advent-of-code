"""
Day 24
https://adventofcode.com/2021/day/24

1st star: 09:15:12 (*)
2nd star: 09:17:12 (*)

(*) I was on vacation when this problem was solved, so I wasn't 
    able to solve it right when it was released. 

At first, I was excited about this problem because I assumed
it would largely revolve around implementing a simple
computer architecture (like 2019's IntCode), but it then
became evident there was a lot more to this problem.

A brute force solution was a no-go. Then, I stared at the values
of the x, y, z variables (using different model numbers) 
for way too long, trying to find a pattern in them, and came
up with nothing. Finally, I decided to effectively "decompile"
the provided assembly code, and actually arrived at the
solution manually (with just some code to extract some
useful information from the provided code)

After producing the solutions, I wrote code that automated the
process of producing a valid model number (which basically
turned this into a code analysis problem). The code_analysis
function explains how valid numbers can be deduced from the
provided code.
"""

import util
import math
from functools import cached_property, lru_cache

from util import log

class ALU:
    """
    Class for representing an ALU

    This is only used to validate whether a model number is valid
    """

    def __init__(self, program, input):
        self.program = program
        self.input = input[:]
        self.vars = {"w":0, "x":0, "y":0, "z":0}

    def run(self):
        """
        Run the ALU program. Doesn't return anything, but
        we can check the values of the variables after
        calling this method.
        """
        for inst in self.program:
            tokens = inst.split()
            op = tokens[0]
            a = tokens[1]
            a_value = self.vars[a]

            if len(tokens) == 3:
                b = tokens[2]
                if b in ("w", "x", "y", "z"):
                    b_value = self.vars[b]
                else:
                    b_value = int(b)

            if op == "inp":
                input = int(self.input.pop(0))
                self.vars[a] = input
            elif op == "add":
                self.vars[a] = a_value + b_value
            elif op == "mul":
                self.vars[a] = a_value * b_value
            elif op == "div":
                assert b_value != 0
                self.vars[a] = a_value // b_value
            elif op == "mod":
                assert a_value >= 0
                assert b_value > 0
                self.vars[a] = a_value % b_value
            elif op == "eql":
                self.vars[a] = 1 if a_value == b_value else 0


def code_analysis(program):
    """
    Analyses the provided program to find a mapping between digits.
    Produces a dictionary that maps a digit index to a (digit2, x)
    tuple, where the following holds true:

        model_number[digit] == model_number[digit2] + x
        
    The provided program actually includes 14 nearly-identical blocks
    of code (one per digit), that only differ in the integer parameters
    to three instructions (let's call them a, b, and c). Each block
    of code will zero out the "z" variable as long as two digits in
    the model number differ by a specific amount. More specifically,
    the provided code effectively does the following for each of the
    14 digits:

    digit = <read next digit from model number>
    if a == 1:
        push (digit, c) into the stack
    elif a == 26:
        pop (digit2, x) from the stack
        if digit - digit2 == b + x:
            z = (z * 1) + 0  # <-- if z is zero, it stays zero
        else:
            z = (z * <some non-one value>) + <some non-zero value>

    So, if we extract the values of a, b, and c from each of the 14
    blocks of code, it is possible to determine the expected difference
    between each of the digits.
    """

    # Extract the a, b, c parameters
    params = []
    for i in range(14):
        a = int(program[18*i + 4].split()[2])
        b = int(program[18*i + 5].split()[2])
        c = int(program[18*i + 15].split()[2])

        params.append((a,b,c))

    # Perform the stack operations to obtain
    # the differences between digits
    digit_map = {}
    stack = []
    for digit, (a, b, c) in enumerate(params):
        if a == 1:
            stack.append((digit, c))
        else:
            digit2, x = stack.pop()

            digit_map[digit] = (digit2, b+x)
            digit_map[digit2] = (digit, -(b+x))

    return digit_map


def generate_model_number(digit_map, target_digit):
    """
    Generates a model number where as many of the digits are set
    to target_digit (or as close as possible, given the
    constraints imposed by the digit_map)
    """
    model_number = [0] * 14

    for i in range(14):
        if model_number[i] != 0:
            # We've already set a value for this digit, keep going
            continue

        d2, x = digit_map[i]

        if 0 <= target_digit - x <= 9:
            model_number[i] = target_digit
            model_number[d2] = target_digit-x
        else:
            model_number[i] = target_digit+x
            model_number[d2] = target_digit

    return "".join(str(d) for d in model_number)        


def validate(program, model_number):
    """
    Run a model number through the ALU to verify that it does
    result in the "z" variable being zero at the end of the
    program.
    """
    digits = [int(c) for c in str(model_number)]
    alu = ALU(program, digits)
    alu.run()

    return alu.vars["z"] == 0


def solve(program, target_digit):
    """
    Solve the problem for a given target digit (i.e., we want as many
    of the digits to be equal to that target)
    """
    
    # Find the differences between the digits
    digit_map = code_analysis(program)

    # Generate the model number
    model_number = generate_model_number(digit_map, target_digit)

    # Make sure it's actually valid
    assert validate(program, model_number)

    return model_number


if __name__ == "__main__":
    util.set_debug(False)

    input = util.read_strs("input/24.in", sep="\n")

    print("TASK 1")
    util.call_and_print(solve, input, 9)

    print("TASK 2")
    util.call_and_print(solve, input, 1)
