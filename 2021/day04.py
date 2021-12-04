"""
Day 4
https://adventofcode.com/2021/day/4

1st star: 00:13:58
2nd star: 00:17:56

I went full OO on this problem, which involved a bit of extra time in
Task 1, but which I'm pretty sure saved me a lot of time in Task 2.

The code below is not substantially different from what I wrote originally,
except for a fair amount of cleaning up and documenting. I also added a 
bunch of things that aren't strictly necessary to solve the problem, 
like a __str__ method for the BingoBoard class that uses the same formatting
shown in the problem.

So happy with how pretty this polished version turned out.
"""

import util
import math
import sys
import re

from util import log

class BingoBoardEntry:
    """
    Class representing a single entry in the bingo board        
    """

    def __init__(self, number):
        self.number = number
        self.marked = False

    def __repr__(self):
        return f"BingoBoardEntry({self.number}, {self.marked})"

    def get_color_str(self, width):
        """
        Generate a string representation of the entry, where marked
        entries are displayed in the terminal as bold white
        (using ANSI color codes)
        """
        num_str = str(self.number)
        padding_len = max(0, width - len(num_str))
        padding = " " * padding_len

        if self.marked:
            return f"{padding}\u001b[1m\u001b[37;1m{num_str}\u001b[0m"
        else:
            return f"{padding}{num_str}"


class BingoBoard:
    """
    Class representing a bingo board
    """

    def __init__(self, board):
        """Constructor

        Args:
            board (list of lists of ints): The numbers in the board
        """
        # We store BingoBoardEntry objects both in a list of lists
        # (to preserve their location in the board), and in a dictionary
        # (for easy access by number)
        self.__rows = []
        self.__entries = {}

        for row in board:
            new_row = []
            for number in row:
                entry = BingoBoardEntry(number)
                new_row.append(entry)
                self.__entries[number] = entry
            self.__rows.append(new_row)

        self.__nrows = len(self.__rows)
        self.__ncols = len(self.__rows[0])

    @classmethod
    def from_input(cls, board_str):
        """
        Creates a BingoBoard object starting from the string
        representation in the problem
        """
        rows = board_str.split("\n")

        board = []
        for row in rows:
            numbers = [int(x) for x in row.split()]
            board.append(numbers)

        return cls(board)

    def mark(self, number):
        """
        Marks a number in the board
        """
        if number in self.__entries:
            self.__entries[number].marked = True
            
    def is_winning(self):
        """
        Checks whether the board contains a winning row
        or a winning column
        """
        # Check rows
        for row in self.__rows:
            marked = [entry.marked for entry in row]
            if all(marked):
                return True

        # Check columns
        for ncol in range(self.__ncols):
            marked = [row[ncol].marked for row in self.__rows]
            if all(marked):
                return True

        return False

    def sum_unmarked(self):
        """
        Returns the sum of all the unmarked entries
        """
        s = 0
        for entry in self.__entries.values():
            if not entry.marked:
                s += entry.number

        return s

    def __str__(self):
        s = ""
        for row in self.__rows:
            for i, entry in enumerate(row):
                width = 2 if i == 0 else 3
                s += entry.get_color_str(width)
            s +=  "\n"
        return s


def read_input(input):
    """
    Reads the problem input
    """
    numbers = [int(x) for x in input[0].split(",")]

    boards = []
    for board_str in input[1:]:
        board = BingoBoard.from_input(board_str)
        boards.append(board)

    return numbers, boards


def score_winning_board(numbers, boards, winning_pos):
    """
    Find the score of the board that wins at position "winning_pos"
    """
    already_won = set()
    for n in numbers:
        for board in boards:
            board.mark(n)
            if board.is_winning():
                already_won.add(board)
                if len(already_won) == winning_pos:
                    print(f"The winning board is:\n{board}")                
                    return board.sum_unmarked() * n


def task1(input):
    numbers, boards = read_input(input)
    return score_winning_board(numbers, boards, 1)


def task2(input):
    numbers, boards = read_input(input)
    return score_winning_board(numbers, boards, len(boards))


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/04.in", sep="\n\n")
    input = util.read_strs("input/04.in", sep="\n\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
