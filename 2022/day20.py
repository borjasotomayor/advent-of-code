"""
Day 20
https://adventofcode.com/2022/day/20

1st star: 00:26:15	
2nd star: 01:14:31	

Modular arithmetic truly is the bane of my existence in Advent of Code.
I got through Part 1 fairly quickly by implementing a doubly-linked list,
which (at least to me) was easier to reason about than dealing with
list indices, etc.

Then, in Part 2 I essentially arrived at the correct solution, but
was absolutely convinced that we had to shift the elements of the list modulo
the size of the list. Suppose we have a list with seven elements:

    A  B  C  D  E  F  G

And we want to shift E 12 times to the right:

    A  B  C  D  E  F  G
                   1  2
    3  4  5  6  7  8  9
    10 11 12

It's the same as shifting it 5 times, right? BZZZZT! Turns out it's 
modulo the size of the list... minus one 

*facepalm*

The intuition is that, given any arrangement of the list, you need len(list)-1 
swaps to return to the original arrangement. Suppose we have a list of seven
elements:

    A B C D E F G

And we shift E six times:

  Start: A B C D E F G
1 swap : A B C D F E G
2 swaps: A B C D F G E
3 swaps: E B C D F G A
4 swaps: B E C D F G A
5 swaps: B C E D F G A
6 swaps: B C D E F G A

The fact that A appears at the end now is just a representation issue; 
the lists at the start and end are the same arrangement of values.
"""

import util
import math
import sys
import re

from util import log

class Node:
    """
    Represents a node in a doubly-linked list
    """

    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None

    def __repr__(self):
        return f"[{self.prev.value} <--> {self.value} <--> {self.next.value}]"

    @staticmethod
    def swap(node1, node2):
        """
        Swaps two nodes, where node1 is node2's prev (and node2 is node1's next)
        """
        node0 = node1.prev
        node1_prev = node1.prev
        node1_next = node1.next
        node2_prev = node2.prev
        node2_next = node2.next
        node3 = node2.next

        node0.next = node2
        node2.prev = node0
        node2.next = node1
        node1.prev = node2
        node1.next = node3
        node3.prev = node1


    def move(self, mod=None):
        """
        Moves a node according to the value of the node.
        Optionally, provide a modulus.
        """

        n = abs(self.value)
        if mod is not None:
            n = n % mod
        if self.value < 0:                
            for _ in range(n):
                Node.swap(self.prev, self)
        elif self.value > 0:
            for _ in range(n):
                Node.swap(self, self.next)


def log_list(node0):
    """
    Helper function to log the contents of a list
    """
    cur = node0
    vals = []
    while True:
        vals.append(cur.value)
        cur = cur.next
        if cur == node0:
            break
    log(", ".join(str(x) for x in vals))


def mix(values, key=1, n_mix=1):
    """
    Perform the mixing operation, optionally providing a "decryption key"
    and doing multiple mixes.
    """

    # Create the nodes
    nodes = [Node(v*key) for v in values]

    # Set the prev/next pointers, and locate
    # the node with value 0
    node0 = None
    for i, n in enumerate(nodes):
        n.prev = nodes[i-1]
        n.next = nodes[(i+1)%len(nodes)]
        if n.value == 0:
            node0 = n

    assert node0 is not None

    # Do the mixes    
    for _ in range(n_mix):
        for n in nodes:
            n.move(mod=len(nodes)-1)

    log_list(node0)

    # Locate the 1000th, 2000th, and 3000th values
    cur = node0
    vals = []
    for i in range(1,3001):
        cur = cur.next
        if i % 1000 == 0:
            vals.append(cur.value)

    return sum(vals)


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_ints("input/sample/20.in", sep="\n")
    input = util.read_ints("input/20.in", sep="\n")

    print("TASK 1")
    util.call_and_print(mix, sample)
    util.call_and_print(mix, input)

    print("\nTASK 2")
    util.call_and_print(mix, sample, 811589153, 10)
    util.call_and_print(mix, input, 811589153, 10)
