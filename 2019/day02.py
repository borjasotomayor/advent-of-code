"""
Day 2
https://adventofcode.com/2019/day/2

1st star: 00:09:46
2nd star: 00:14:39

The first IntCode problem! If only we knew back in Day 2 how much fun
we'd have with IntCode. My first version of this problem was a bunch
of ad-hoc code implementing just enough IntCode to find the solution,
but I later re-wrote it to use my IntCode class.
"""

import util
from intcode import IntCode


def task1(prog):
    """
    Task 1: Set inputs and run program.
    """
    prog[1] = 12
    prog[2] = 2
    vm = IntCode(prog)
    vm.run()

    return vm.memory[0]


def task2(prog):
    """
    Task 2: Try a series of inputs, and return the ones
    that produce a specific output.
    """
    for noun in range(0, 100):
        for verb in range(0, 100):
            vm = IntCode(prog)
            vm.memory[1] = noun
            vm.memory[2] = verb
            vm.run()
            if vm.memory[0] == 19690720:
                return 100 * noun + verb

    return None


if __name__ == "__main__":
    util.set_debug(False)

    input = util.read_ints("input/02.in", sep=",")

    print("TASK 1")
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, input)
