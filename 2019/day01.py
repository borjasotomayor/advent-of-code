"""
Day 1
https://adventofcode.com/2019/day/1

1st star: 00:01:35
2nd star: 00:05:01
"""

import util
import math

def task1(numbers):
    sum = 0
    for n in numbers:
        x = int(math.floor(n/3) - 2)
        sum += x
    return sum

def task2(numbers):
    sum = 0
    for n in numbers:
        while n > 0:
            n = int(math.floor(n/3) - 2)
            if n > 0:
                sum += n
            
    return sum    


if __name__ == "__main__":
    nums = util.read_ints("input/01.in")

    print("TASK 1")
    util.call_and_print(task1, [12])
    util.call_and_print(task1, [14])
    util.call_and_print(task1, [1969])
    util.call_and_print(task1, [100756])
    util.call_and_print(task1, nums)

    print("\nTASK 2")
    util.call_and_print(task2, [12])
    util.call_and_print(task2, [14])
    util.call_and_print(task2, [1969])
    util.call_and_print(task2, [100756])
    util.call_and_print(task2, nums)