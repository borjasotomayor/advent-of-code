"""
Day 23
https://adventofcode.com/2021/day/23

1st star: 02:34:57
2nd star: 02:42:44

Ok, this was a really fun problem, but it took a looong time to get
all the details right. My original intuition was to treat the input
like an actual grid, and run some sort of A* search but, once I
started reading the movement rules more carefully, I realized
it was basically a variation on the Tower of Hanoi puzzle, so
I implemented it as such.

This code is still pretty slow (it takes about 30 seconds to
find the solution for both the sample and actual input on both
tasks). I used a couple of optimizations (branch and bound, memoization,
greedily exploring low-cost moves first, etc.) but I suspect the
game tree could be cut down even further.
"""

import util
import math
import sys
import re
import operator

from util import log


class Peg:
    """
    Class for representing an individual peg
    """

    def __init__(self, capacity, target=None, initial=None):
        """
        A peg has a capacity (the maximum number of rings it can hold),
        and can either be a target peg (in which case it is associated
        with a specific letter) or an auxiliary ring.

        We can optionally provide initial values for the peg.
        """
        self.capacity = capacity
        self.target = target

        if initial is not None:
            self.rings = initial[:]
        else:
            self.rings = []

    @property
    def size(self):
        return len(self.rings)

    @property
    def empty(self):
        return len(self.rings) == 0

    @property
    def auxiliary(self):
        return self.target is None

    def accepts(self, letter):
        """
        Returns True if the peg could accept the given letter.
        """
        if len(self.rings) == self.capacity:
            # The ring is full
            return False
        elif self.target is not None and letter != self.target:
            # This is a target peg, and the letter doesn't match the target
            return False
        elif self.target is not None and letter == self.target:
            # If this is a target ring, and the letter matches the target,
            # make sure that the ring is either empty, or all rings in
            # peg are of the same (target) letter.
            return self.empty or all(r == letter for r in self.rings)
        else:
            # In all other cases, the letter is accepted
            return True

    def push(self, letter):
        """
        Push a ring (of the given letter) into the peg
        """
        assert self.size + 1 <= self.capacity

        self.rings.append(letter)

    def peek(self):
        """
        Peek at the ring at the top of the peg
        """
        if len(self.rings) == 0:
            return None
        else:
            return self.rings[-1]

    def pop(self):
        """
        Pop the ring at the top of the peg
        """
        assert len(self.rings) != 0
        return self.rings.pop()

    @property
    def done(self):
        """
        If the peg is full, and all the rings are of the same (target)
        letter, then this peg is done.
        """
        return self.size == self.capacity and all(r == self.target for r in self.rings)

    @property
    def can_pop(self):
        """
        Are we allowed to pop a ring from the peg?
        """

        if self.empty:
            # If the ring is empty, there's nothing to pop
            return False

        if self.auxiliary:
            # We can always pop from an auxiliary peg
            return True
        else:
            # In a target peg, we are not allowed to pop if the 
            # ring contains only target rings.
            if self.size >= 1 and all(r == self.target for r in self.rings):
                return False
            else:
                return True

    def __str__(self):
        """
        Dunder method for 
        """
        return "-- " + " - ".join(self.rings)



class GeneralHanoi:
    """
    Class for implementing a general Towers of Hanoi game
    """

    ENERGY = {"A": 1,
              "B": 10,
              "C": 100,
              "D": 1000}

    TARGET = {"A": 2,
              "B": 4,
              "C": 6,
              "D": 8}

    def __init__(self, initial, peg_size):
        # Create the pegs
        self.pegs = [Peg(1),
                     Peg(1),
                     Peg(peg_size, "A", initial[0]),
                     Peg(1),
                     Peg(peg_size, "B", initial[1]),
                     Peg(1),
                     Peg(peg_size, "C", initial[2]),
                     Peg(1),
                     Peg(peg_size, "D", initial[3]),
                     Peg(1),
                     Peg(1)]
        self.peg_size = peg_size

        # We use this to cache the lists of possible moves
        # for a given configuration of the pegs/rings.
        self.moves_cache = {}

    def reachable(self, src, dst):
        """
        Check if a ring is reachable from the source ring to the
        destination ring, subject to the constraint that we can't
        move past a ring that is "blocking the hallway" (this
        is a feature of this specific version of the game,
        and not found in the Towers of Hanoi)
        """
        lb = min(src, dst)
        ub = max(src, dst)

        for i in range(lb, ub+1):
            if i == src:
                continue
            if self.pegs[i].auxiliary and not self.pegs[i].empty:
                return False

        return True
        
    def possible_moves(self, peg_num):
        """
        Return all the possible froms from a peg.

        For each move, returns a (src, dst, energy, target) tuple,
        where target is True if the move would result in a ring
        moving into its target peg.
        """

        peg = self.pegs[peg_num]

        if peg.size == 0:
            # If there are no rings in the peg, there's nothing to move
            return []
        elif peg.auxiliary:
            # If this is an auxiliary peg, we can only move to a target peg
            letter = peg.peek()
            target_peg = GeneralHanoi.TARGET[letter]

            if self.pegs[target_peg].accepts(letter) and self.reachable(peg_num, target_peg):
                return [[peg_num, target_peg, self.energy(peg_num, target_peg), True]]
            else:
                return []
        elif not peg.auxiliary and peg.can_pop:
            # If this is a target ring, we could potentially move to multiple
            # locations.
            letter = peg.peek()
            moves = []
            for i, p in enumerate(self.pegs):
                if p.accepts(letter) and self.reachable(peg_num, i):
                    moves.append((peg_num, i, self.energy(peg_num, i), p.target == letter))
            return moves
        else:
            return []

    def energy(self, src, dst):
        """
        Compute the energy of a given move
        """
        letter = self.pegs[src].peek()

        if self.pegs[src].auxiliary:
            out_steps = 0
        else:
            out_steps = self.peg_size + 1 - self.pegs[src].size 

        hallway_steps = abs(dst-src) 

        if self.pegs[dst].auxiliary:
            in_steps = 0
        else:
            in_steps = self.peg_size - self.pegs[dst].size

        return (out_steps + hallway_steps + in_steps) * GeneralHanoi.ENERGY[letter]

    def move(self, src, dst):
        """
        Move a ring from one peg to another
        """
        letter = self.pegs[src].pop()
        self.pegs[dst].push(letter)

    @property
    def done(self):
        """
        Check if the game is done (if all the rings are in their target pegs)
        """
        return all(p.done for p in self.pegs if not p.auxiliary)

    @property
    def hash(self):
        """
        Computes a string hash of the game state, which we use for
        caching/memoization
        """
        h = ""
        for peg in self.pegs:
            h += "".join(peg.rings)
            h += "." * (peg.capacity - peg.size)
        return h

    def solve(self, total_energy=0, max_energy=None, memo=None):
        """
        Find the solution with the lowest total energy.

        Parameters:
        - total_energy: the energy we have consumed so far
        - max_energy: the maximum energy we're willing to consume
          (i.e., the energy of the best solution we've found so
           far; no point exploring solutions that would have
           higher energy)
        - memo: A dictionary for memoization

        Returns (solved, energy), where solved is True if a
        solution is found. If solution is not found, energy
        is None.
        """

        if memo is None:
            memo = {}

        # Check if we can return a result from the memoization
        # dictionary.
        if self.hash in memo:
            if memo[self.hash] is None:
                return False, None
            elif total_energy in memo[self.hash]:
                rv = memo[self.hash][total_energy]
                if rv is None:
                    return False, None
                else:
                    return True, rv

        # Base case: The game is done, so we return
        if self.done:
            return True, total_energy

        # Compute the next possible moves (potentially extracting
        # them from the moves cache)
        if self.hash in self.moves_cache:
            all_moves = self.moves_cache[self.hash]
        else:
            all_moves = []
            for i, peg in enumerate(self.pegs):
                all_moves += self.possible_moves(i)

            # Greedy optimization: start by checking the moves that
            # move rings into their target pegs, followed by the moves
            # in ascending cost
            all_moves.sort(key=operator.itemgetter(2))
            all_moves.sort(key=operator.itemgetter(3), reverse=True)
            self.moves_cache[self.hash] = all_moves

        if len(all_moves) == 0:
            # Base case: No moves, we're stuck
            memo[self.hash] = None
            return False, None
        else:
            # Recursive case: we explore all possible next moves. Once we
            # find a solution, we start skipping any path that would lead
            # to a solution with higher energy.
            
            best_energy = None
            for src, dst, energy, _ in all_moves:
                # If this move would have a higher cost than the best solution
                # so far, we skip it
                if max_energy is not None and total_energy + energy > max_energy:
                    continue

                # Make the move, and make the recursive call
                self.move(src, dst)
                solved, next_energy = self.solve(total_energy + energy, max_energy, memo)

                if solved and (best_energy is None or next_energy < best_energy):
                    # If we found a solution, and it's better than what we've
                    # seen so far in this loop, update best_energy
                    best_energy = next_energy

                if solved and (max_energy is None or next_energy < max_energy):
                    # If we found a solution, and it's better than anything
                    # we've seen so far, update max_energy
                    max_energy = next_energy

                # Undo the move
                self.move(dst, src)

            # If we found a solution, return it (and update the memoization dictionary)
            if best_energy is not None:
                memo.setdefault(self.hash, {})[total_energy] = best_energy
                return True, best_energy
            else:
                memo.setdefault(self.hash, {})[total_energy] = None
                return False, None

    def __str__(self):
        return "\n".join(f"{i} {p}" for i, p in enumerate(self.pegs))


def task1(input):
    """
    Task 1: Solve with pegs of size 2
    """
    hanoi = GeneralHanoi(input, peg_size=2)
    return hanoi.solve()


def task2(input):
    """
    Task 1: Solve with pegs of size 4
    """
    hanoi = GeneralHanoi(input, peg_size=4)
    return hanoi.solve()


if __name__ == "__main__":
    util.set_debug(False)

    print("TASK 1")
    util.call_and_print(task1, [["A","B"],["D","C"],["C","B"],["A","D"]])
    util.call_and_print(task1, [["B","B"],["C","A"],["D","A"],["C","D"]])

    print("\nTASK 2")
    util.call_and_print(task2, [["A","D","D","B"],["D","B","C","C"],["C","A","B","B"],["A","C","A","D"]])
    util.call_and_print(task2, [["B","D","D","B"],["C","B","C","A"],["D","A","B","A"],["C","C","A","D"]])
