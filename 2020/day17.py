"""
Day 17
https://adventofcode.com/2020/day/17

1st star: 00:50:00
2nd star: 01:05:10

I spent waaay too much racking my brains thinking I needed a super-fancy
data structure, when a dictionary mapping tuples to values (with some
range checking) was all I needed. An OO approach worked out well for
this program because it ensured I could abstract away most of the
messiness of dealing with infnite 3d/4d space.
"""

import util
import math
import sys
import re

from util import log

class ConwayCube:
    """
    Class for manipulating the multidimensional Conway Cubes
    
    The coordinates are stored in a dictionary mapping tuples
    (the x,y,z,w coordinates) to a value. A set of active
    coordinates would probably do the trick too.

    We then just need to keep track of the ranges of each
    dimension, to make sure we always process a finite amount
    of space.
    """

    def __init__(self):
        self.xyz = {}
        self.x_range = [0, 0]
        self.y_range = [0, 0]
        self.z_range = [0, 1]
        self.w_range = [0, 1]


    def from_grid(self, grid):
        """
        Load from the provided grid
        """
        for y, row in enumerate(grid):
            for x, char in enumerate(row):
                self.set_coord(char, x, y, 0, 0)        


    def __update_range(self, dim_range, val):
        """
        Given a range (a list containing a lower and upper bound),
        update the range so that val will be valid in the range.
        """
        lb, ub = dim_range

        if val < lb:
            dim_range[0] = val
        elif val >= ub:
            dim_range[1] = val + 1
        

    def __update_ranges(self, x, y, z, w):
        """
        Given an (x, y, z, w) point, update all the ranges.
        """
        self.__update_range(self.x_range, x)
        self.__update_range(self.y_range, y)
        self.__update_range(self.z_range, z)
        self.__update_range(self.w_range, w)


    def get_coord(self, x, y, z, w=0):
        """
        Get the value at coordinate (x, y, z, w)
        """
        self.__update_ranges(x, y, z, w) 
        return self.xyz.setdefault((x, y, z, w), '.')


    def set_coord(self, value, x, y, z, w=0):
        """
        Set the value at coordinate (x, y, z, w)
        """
        self.__update_ranges(x, y, z, w) 
        self.xyz[(x,y,z,w)] = value


    def update(self, x, y, z, w=None):
        """
        Apply the update rule at (x, y, z) or (x, y, z, w)
        Does not actually update the grid, just returns
        what the new value would be.
        """

        if w is None:
            dws = (0,)
            w = 0
        else:
            dws = (-1, 0, 1)

        cur_value = self.get_coord(x, y, z, w)
        n_active = 0

        done = False
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    for dw in dws:
                        if not (dx==0 and dy==0 and dz==0 and dw==0):
                            neighbor = self.get_coord(x+dx, y+dy, z+dz, w+dw)
                            if neighbor == "#":
                                n_active += 1

                            if n_active > 3:
                                done = True
                                break
                    if done:
                        break
                if done:
                    break
            if done:
                break

        if cur_value == "#":
            if n_active in (2,3):
                return "#"
            else:
                return "."
        elif cur_value == ".":
            if n_active == 3:
                return "#"
            else:
                return "."


    def cycle3d(self):
        """
        Do one cycle in 3d-space and return the updated cube
        """
        cc2 = ConwayCube()

        xlb, xub = self.x_range
        ylb, yub = self.y_range
        zlb, zub = self.z_range
        for x in range(xlb-1, xub+1):
            for y in range(ylb-1, yub+1):
                for z in range(zlb-1, zub+1):
                    new_val = self.update(x, y, z)
                    cc2.set_coord(new_val, x, y, z)

        return cc2


    def cycle4d(self):
        """
        Do one cycle in 4d-space and return the updated cube
        """
        cc2 = ConwayCube()

        xlb, xub = self.x_range
        ylb, yub = self.y_range
        zlb, zub = self.z_range
        wlb, wub = self.w_range
        for x in range(xlb-1, xub+1):
            for y in range(ylb-1, yub+1):
                for z in range(zlb-1, zub+1):
                    for w in range(wlb-1, wub+1):
                        new_val = self.update(x, y, z, w)
                        cc2.set_coord(new_val, x, y, z, w)

        return cc2


    def print(self):
        """
        Print the cube
        """
        for w in range(*self.w_range):
            for z in range(*self.z_range):
                print(f"z={z}, w={w}")
                for y in range(*self.y_range):
                    for x in range(*self.x_range):
                        v = self.get_coord(x, y, z)
                        print(v, end="")
                    print()
                print()


    def count_active(self):
        """
        Count the number of active cubes
        """
        n_active = 0
        xlb, xub = self.x_range
        ylb, yub = self.y_range
        zlb, zub = self.z_range
        wlb, wub = self.w_range
        for x in range(xlb, xub):
            for y in range(ylb, yub):
                for z in range(zlb, zub):
                    for w in range(wlb, wub):
                        v = self.get_coord(x, y, z, w)
                        if v == "#":
                            n_active +=1
        return n_active


def task1(input):
    cc = ConwayCube()
    cc.from_grid(input)

    for _ in range(6):
        cc = cc.cycle3d()

    return cc.count_active()


def task2(input):
    cc = ConwayCube()
    cc.from_grid(input)

    for _ in range(6):
        cc = cc.cycle4d()

    return cc.count_active()



if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/17.in", sep="\n")
    grid = util.read_strs("input/17.in", sep="\n")

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, grid)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, grid)

