"""
Day 5
https://adventofcode.com/2022/day/5

1st star: 00:11:31
2nd star: 00:13:03

Gotta say, I'm not really a fan of problems were you
spend 80% of your time parsing the input :-/ My original
solution did a lot of quick-and-dirty parsing, so I then
refactored and polished all the parsing code into its
own function. Once that's done, the implementation
of the "crane" function is fairly simple.
"""

import util
import copy

from util import log


def read_input(filename):
    """
    Custom function for reading the input, since the read_* 
    functions in my util module strip whitespace, which
    is significant in this problem.

    This function also does the legwork of parsing the stacks, etc.
    """
    with open(filename) as f:
        txt = f.read()
        stacks_str, moves_str = txt.split(sep="\n\n")  
        stacks_lines = stacks_str.split("\n")
        moves_lines = moves_str.split("\n")

    # Remove the last line of the stacks portion
    indices_line = stacks_lines.pop()

    # The last number in that line conveniently gives
    # us the number of stacks
    num_stacks = int(indices_line.split()[-1])
    
    # Parse the stacks lists
    stacks = [[] for _ in range(num_stacks)]
    for line in stacks_lines:
        # Read the character corresponding to each stack
        # If it is not blank, insert it into the corresponding
        # stack list
        for s in range(num_stacks):
            c = line[1 + s*4]
            if c != " ":
                stacks[s].insert(0, c)

    # Parse the moves
    moves = []
    for n, sfrom, sto in util.iter_parse(moves_lines, "move {:d} from {:d} to {:d}"):        
        moves.append((n, sfrom-1, sto-1))

    return stacks, moves


def crane(stacks, moves, multiple=False):
    """
    Process the provided moves on the provided stacks.

    Crates are moved one by one, unless multiple is True,
    in which case the carane picks multiple crates at once.
    """

    # We meed to make a deep copy since we'll be modifying
    # the stacks and other calls to this function may want
    # to use the same stacks
    stacks = copy.deepcopy(stacks)

    for n, sfrom, sto in moves:
        to_move = []
        for _ in range(n):
            crate = stacks[sfrom].pop()
            to_move.append(crate)

        if multiple:
            stacks[sto] += reversed(to_move)
        else:
            stacks[sto] += to_move

    # Compute the top values
    value = []
    for s in stacks:
        value.append(s[-1])
    
    return "".join(value)


if __name__ == "__main__":
    util.set_debug(False)

    stacks_sample, moves_sample = read_input("input/sample/05.in")
    stacks, moves = read_input("input/05.in")
    
    print("TASK 1")
    util.call_and_print(crane, stacks_sample, moves_sample)
    util.call_and_print(crane, stacks, moves)

    print("\nTASK 2")
    util.call_and_print(crane, stacks_sample, moves_sample, True)
    util.call_and_print(crane, stacks, moves, True)
    