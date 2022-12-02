"""
Day 2
https://adventofcode.com/2022/day/2

1st star: 00:05:33
2nd star: 00:07:05

My first solution was an ungodly mess of if-then-elses that got the
job done in just a few minutes, so this required a lot of cleaning up.
"""

import util
import math
import sys
import re

from util import log


# Useful mappings

POINTS = {"R": 1, "P": 2, "S": 3}

DEFEATS = {"R": "S", 
           "P": "R", 
           "S": "P"}

DEFEATED_BY = {"R": "P", 
               "P": "S", 
               "S": "R"}


def translate_hand(char):
    """
    Translate an input character (X, Y, Z, A, B, C) into R, P, S
    """
    ALIAS = {"A": "R", "B": "P", "C": "S",
             "X": "R", "Y": "P", "Z": "S",}

    hand = ALIAS.get(char)

    if hand is None:
        raise ValueError(f"Unrecognized hand: {char}")
    else:
        return hand



def play(hand_opponent, hand_mine):
    """
    Play a game of Rock, Paper, Scissors
    """
    mine_defeats = DEFEATS[hand_mine]
    mine_defeated_by = DEFEATED_BY[hand_mine]

    points = POINTS[hand_mine]
    if hand_opponent == mine_defeats:
        # I win!
        points += 6
    elif hand_opponent == mine_defeated_by:
        # I lose :-(
        pass
    elif hand_opponent == hand_mine:
        points += 3

    return points


def achieve_outcome(hand_opponent, outcome):
    """
    Play a game with a specific outcome (X=lose, Y=tie, Z=win)
    """
    if outcome == "X":
        # Gotta lose
        hand_mine = DEFEATS[hand_opponent]
    elif outcome == "Y":
        # Gotta tie
        hand_mine = hand_opponent
    elif outcome == "Z":
        # Gotta win
        hand_mine = DEFEATED_BY[hand_opponent]

    return play(hand_opponent, hand_mine)


def task1(input):
    """
    Play multiple games of Rock, Paper, Scissors and add up the points
    """
    total_points = 0
    for opponent, mine in input:
        hand_opponent = translate_hand(opponent)
        hand_mine = translate_hand(mine)

        total_points += play(hand_opponent, hand_mine)

    return total_points


def task2(input):
    """
    Play multiple games of Rock, Paper, Scissors, where we
    aim for a specific outcome in each game, and add up the points
    """
    total_points = 0
    for opponent, outcome in input:
        hand_opponent = translate_hand(opponent)

        total_points += achieve_outcome(hand_opponent, outcome)

    return total_points



if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/02.in", sep="\n", sep2=" ")
    input = util.read_strs("input/02.in", sep="\n", sep2=" ")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
