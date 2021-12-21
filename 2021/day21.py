"""
Day 21
https://adventofcode.com/2021/day/21

1st star: 00:11:49
2nd star: 00:47:45

While Part 1 was a fairly straightforward simulation, Part 2
was a fun recursive problem that basically involved producing 
a game tree, but using memoization to make sure it could be 
computed efficiently. 

I lost a fair amount of time because I didn't fully internalize 
the phrase "The game is played the same as before" and kept getting
very low counts, until I figured out that I needed to keep track
of the roll (modulo 6), instead of the next turn (as typically
happens when exploring a game tree). Of course, then the recursion
exploded, but thankfully @lru_cache came to the rescue.
"""

import util
import math
import sys
import re

from functools import lru_cache

from util import log


def dirac_dice(p1_start, p2_start):
    """
    Simulate a game with deterministic dice
    """
    dice = 0
    p1_score = 0
    p2_score = 0
    p1_pos = p1_start
    p2_pos = p2_start

    while True:
        # Player 1 rolls the dice three times
        p1_move = (dice+2)*3 
        dice += 3

        # Update the position and score
        p1_pos = ((p1_pos + p1_move - 1) % 10) + 1
        p1_score += p1_pos

        if p1_score >= 1000:
            break

        # Player 2 rolls the dice three times
        p2_move = (dice+2)*3
        dice += 3

        # Update the position and score
        p2_pos = ((p2_pos + p2_move - 1) % 10) + 1
        p2_score += p2_pos

        if p2_score >= 1000:
            break

    return min(p1_score,p2_score) * dice


def count_wins(p1_start, p2_start):
    """
    Counts the number of wins using the quantum die.
    """

    @lru_cache(maxsize = None)
    def count_wins_r(p1_score, p2_score, p1_pos, p2_pos, roll):
        """
        Recursive function for counting up the number of wins.
        We make a recursive call for every roll, and keep
        track of what roll we're in:

        Player 1: Rolls 0, 1, and 2
        Player 2: Rolls 3, 4, and 5

        We have to take into account that player 1 only accrues
        new points after roll 2 (and player 2 after roll 5)

        We use memoization with lru_cache; otherwise, the function
        takes too long to run.
        """

        # Base case: Either Player 1 or Player 2 completed their 
        # three rolls and they scored above 21
        if roll == 3 and p1_score >= 21:
            return (1,0)
        if roll == 0 and p2_score >= 21:
            return (0,1)             

        # Recursive case: We recursively count up what happens after
        # rolling a 1, 2, or 3
        p1_wins = 0
        p2_wins = 0

        next_roll = (roll + 1) % 6

        for i in (1,2,3):
            # Player 1's rolls
            if roll in (0,1,2):
                np1_pos = ((p1_pos + i - 1) % 10) + 1

                # Player 1's score only increases after roll 2
                np1_score = p1_score + np1_pos if roll == 2 else p1_score

                p1w, p2w = count_wins_r(np1_score, p2_score, np1_pos, p2_pos, next_roll)
            # Player 2's rolls
            elif roll in (3,4,5):
                np2_pos = ((p2_pos + i - 1) % 10) + 1

                # Player 2's score only increases after roll 5
                np2_score = p2_score + np2_pos if roll == 5 else p2_score

                p1w, p2w = count_wins_r(p1_score, np2_score, p1_pos, np2_pos, next_roll)

            # Tally up the wins
            p1_wins += p1w
            p2_wins += p2w

        return p1_wins, p2_wins

    p1_wins, p2_wins = count_wins_r(0, 0, p1_start, p2_start, roll=0)

    return max(p1_wins, p2_wins)


if __name__ == "__main__":
    util.set_debug(False)

    print("TASK 1")
    util.call_and_print(dirac_dice, 4, 8)
    util.call_and_print(dirac_dice, 5, 9)

    print("\nTASK 2")
    util.call_and_print(count_wins, 4, 8)
    util.call_and_print(count_wins, 5, 9)
