"""
Day 5
https://adventofcode.com/2021/day/5

1st star: 00:39:32
2nd star: 00:49:07

Another IntCode problem that was originally a tangled mess of code,
and which I re-wrote to use my IntCode class.
"""

import util
from intcode import IntCode


def run_test(prog, system_id):
    """
    Inputs a system id to the IntCode VM, and then runs it
    until it outputs a non-zero code (and returns the code)
    """
    vm = IntCode(input)
    vm.input(system_id)

    while True:
        code = vm.output()
        if code != 0:
            return code


if __name__ == "__main__":
    util.set_debug(False)

    input = util.read_ints("input/05.in", sep=",")

    print("TASK 1")
    util.call_and_print(run_test, input, 1)

    print("\nTASK 2")
    util.call_and_print(run_test, input, 5)
