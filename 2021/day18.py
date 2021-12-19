"""
Day 18
https://adventofcode.com/2021/day/18

1st star: 23:14:00 (*)
2nd star: 23:19:56 (*)

(*) I was on vacation when this problem was solved, so I wasn't 
    able to solve it right when it was released. The first part
    took me about about two hours, but mostly because I went straight
    to writing a cleaned-up solution at a more leisurely pace,
    and the second part took about 5 minutes.

Because I wasn't rushing to produce a solution at release time,
I spent the time to write a nice Tree class for this problem,
and was even able to reuse some code for producing a text
version of a tree (from a class I teach), which really helped
with debugging. I also remembered (from way back in College)
that you can overlay a singly/doubly linked list
on the nodes of a trees to make traversals easier, and that
helped a lot with this problem.

I dread to think what this code would've initially looked like
if I was rushing to produce something that would solve the
problem.

"""

import util
import math

from util import log

class Tree:
    """
    Tree class for representing snailfish numbers
    """

    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

        # Pointers to previous and next nodes (used only
        # in the leaf nodes)
        self.prev = None
        self.next = None


    @property
    def is_leaf(self):
        """Returns True if this is a lead node, False otherwise"""
        return self.value is not None


    def find_explodable(self, height):
        """
        Find an explodable pair at the given height
        """

        if self.is_leaf:
            # Leaves are never explodable
            return None
        else:
            if self.left.is_leaf and self.right.is_leaf and height == 0:
                # If this is a pair containing two numbers, and we've
                # no more height to go, this is an explodable pair
                return self
            else:
                # Recursive case: Check the left and right subtrees.
                left_explodable = self.left.find_explodable(height - 1)
                if left_explodable is not None:
                    return left_explodable
                right_explodable = self.right.find_explodable(height - 1)
                return right_explodable


    def explode(self):
        """
        Explodes an explodable node
        """
        assert not self.is_leaf
        assert self.left.is_leaf and self.right.is_leaf

        # Update all the pointers
        if self.left.prev is not None:
            self.left.prev.value += self.left.value
            self.left.prev.next = self

        if self.right.next is not None:
            self.right.next.value += self.right.value
            self.right.next.prev = self

        # Convert this node to a lead node with value 0
        self.value = 0
        self.prev = self.left.prev
        self.next = self.right.next
        self.left = None
        self.right = None


    def find_splittable(self):
        """
        Find the first splittable node
        """
        if self.is_leaf:
            if self.value >=10:
                return self
            else:
                return None
        else:
            left_splittable = self.left.find_splittable()
            if left_splittable is not None:
                return left_splittable
            right_splittable = self.right.find_splittable()
            return right_splittable


    def split(self):
        """
        Split a splittable node
        """
        assert self.is_leaf
        assert self.value >= 10

        # Create the new nodes
        lvalue = int(math.floor(self.value/2))
        rvalue = int(math.ceil(self.value/2))    
        lnode = Tree(value=lvalue)
        rnode = Tree(value=rvalue)

        # Update all the pointers
        lnode.prev = self.prev
        lnode.next = rnode
        rnode.prev = lnode
        rnode.next = self.next
        
        if self.next is not None:
            self.next.prev = rnode
        if self.prev is not None:
            self.prev.next = lnode

        # Turns this node into an inner noder,
        # with the two nodes we just created
        # as children
        self.value = None
        self.left = lnode
        self.right = rnode
        self.prev = None
        self.next = None


    def reduce(self):
        """
        Reduce the tree
        """
        while True:
            expl = self.find_explodable(height=4)
            if expl is not None:
                expl.explode()
                #print("EXPLODE", self.to_list())
                #self.print()
                continue

            splittable = self.find_splittable()
            if splittable is None:
                break
            else:
                splittable.split()
                #print("SPLIT", self.to_list())
                #self.print()


    def leftmost(self):
        """
        Returns the leftmost node
        """
        if self.is_leaf:
            return self
        else:
            return self.left.leftmost()


    def rightmost(self):
        """
        Returns the rightmost tree
        """
        if self.is_leaf:
            return self
        else:
            return self.right.rightmost()


    def add(self, other):
        """
        Adds two trees. Modifies the trees in-place.
        """
        rm = self.rightmost()
        lm = other.leftmost()

        # Update the pointers
        rm.next = lm
        lm.prev = rm

        new_tree = Tree(left=self, right=other)
        new_tree.reduce()

        return new_tree


    def magnitude(self):
        """
        Compute the magnitude of the snailfish number
        """
        if self.is_leaf:
            return self.value
        else:
            return 3*self.left.magnitude() + 2*self.right.magnitude()


    def to_list(self):
        """
        Convert the tree to a list representation
        """
        if self.is_leaf:
            return self.value
        else:
            return [self.left.to_list(), self.right.to_list()]


    def print(self):
        """
        Prints out the tree.
        """

        def print_r(tree, prefix, last):        
            if len(prefix) > 0:
                if last:
                    lprefix1 = prefix[:-3] + "  └──"
                else:
                    lprefix1 = prefix[:-3] + "  ├──"
            else:
                lprefix1 = ""
        
            if len(prefix) > 0:
                lprefix2 = prefix[:-3] + "  │"
            else:
                lprefix2 = ""
                
            if tree.is_leaf:
                prev = "null" if tree.prev is None else tree.prev.value
                next = "null" if tree.next is None else tree.next.value
                ltext = f"{tree.value} (prev={prev}, next={next})"
            else:
                ltext = "" if prefix=="" else "┐"
                
            print(lprefix2)
            print(lprefix1 + ltext)
        
            if tree.is_leaf:
                return
            else:
                newprefix = prefix + u"  │"
                print_r(tree.left, newprefix, False)

                newprefix = prefix + u"   "
                print_r(tree.right, newprefix, True)
                        
        print_r(self, "", False)        


    @classmethod
    def from_list(cls, lst):
        """
        Create a tree starting from a list representation
        """

        def build_tree(v, prev):

            if not isinstance(v, list):
                leaf = cls(value=v)
                leaf.prev = prev
                if prev is not None:
                    prev.next = leaf
                return leaf, leaf
            else:
                left_tree, prev = build_tree(v[0], prev)
                right_tree, prev = build_tree(v[1], prev)

                inner = cls(left=left_tree, right=right_tree)
                inner.left.parent = inner
                inner.left.left_child = True

                inner.right.parent = inner
                inner.right.left_child = False

                return inner, prev

        tree, _ = build_tree(lst, None)

        return tree


def task1(input):
    """
    Task 1: Add up all the snailfish numbers, and return the magnitude
    """

    trees = [Tree.from_list(eval(l)) for l in input]
    trees.reverse()

    while len(trees) != 1:
        op1 = trees.pop()
        op2 = trees.pop()

        res = op1.add(op2)

        trees.append(res)

    return trees[0].magnitude()


def task2(input):
    """
    Task 2: Find the sum with the largest magnitude
    """

    max_magnitude = 0
    for lst1 in input:
        for lst2 in input:
            if lst1 is not lst2:
                tree1 = Tree.from_list(eval(lst1))
                tree2 = Tree.from_list(eval(lst2))

                res = tree1.add(tree2)
                magnitude = res.magnitude()

                if magnitude > max_magnitude:
                    max_magnitude = magnitude

    return max_magnitude


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/18.in", sep="\n")
    input = util.read_strs("input/18.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
