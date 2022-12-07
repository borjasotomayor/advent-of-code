"""
Day 7
https://adventofcode.com/2022/day/7

1st star: 00:24:14
2nd star: 00:29:27

Such a fun problem! I love any problem that involves simulating
any sort of computer system (also nice when there's a dash
of recursion thrown in) 

I followed an object-oriented approach from the start, which I 
think really helped me get the second star pretty quickly. 
I cleaned up the code quite a bit, but it's structurally
very similar to my original solution. The biggest change
was realizing that the code for both tasks could be
written fairly elegantly if you write a generator method
for doing a recursive walk of the directory tree.
"""

import util
import math
import sys
import re

from util import log


class Directory:
    """
    Class to store information about a directory
    """

    def __init__(self, name, parent):
        """
        Constructor

        name (str): Name of the directory
        parent (Directory): Parent directory
        """
        self.name = name
        self.parent = parent
        self.contents = {}
        self.size = None

    def __repr__(self):
        """
        Produces a string representation
        """
        if self.parent is None:
            parent = "None"
        else:
            parent = self.parent.name
        return f"Directory({self.name}, {parent})"

    def compute_size(self):
        """
        Recursively compute the size of the directory and
        all subdirectories
        """
        self.size = 0

        for f in self.contents.values():
            if isinstance(f, File):
                self.size += f.size
            elif isinstance(f, Directory):
                self.size += f.compute_size()

        return self.size

    def walk(self, include_files=True, include_dirs=True):
        """
        Generator method for doing a recursive walk
        of the directory tree
        """
        if include_dirs:
            yield self

        for entry in self.contents.values():
            if isinstance(entry, File) and include_files:
                yield entry
            if isinstance(entry, Directory) and include_dirs:
                for subentry in entry.walk(include_files, include_dirs):
                    yield subentry


class File:
    """
    Class to store information about a file
    """

    def __init__(self, name, size):
        self.name = name
        self.size = size



def parse_output(output):
    """
    Parses the terminal output and returns the Directory object
    for the root directory
    """
    i = 0
    root_dir = Directory("/", None)
    cwd = root_dir

    while i < len(output):
        line = output[i]
        assert line[0] == "$"

        cmd = line[1]
        if cmd == "cd":
            new_dir = line[2]
            if new_dir == "/":
                cwd = root_dir
            elif new_dir == "..":
                cwd = cwd.parent
            else:
                if new_dir not in cwd.contents:
                    cwd.contents[new_dir] = Directory(new_dir, cwd)
                cwd = cwd.contents[new_dir]
            i += 1
        elif cmd == "ls":
            # If the command is an "ls", we keep parsing the terminal
            # output until we encounter another command (or the end
            # of the output)
            i += 1
            while i < len(output):
                ls_line = output[i]

                if ls_line[0] == "$":
                    # We've reached the next command
                    break

                if ls_line[0] == "dir":
                    # Directory entry
                    dir_name = ls_line[1]
                    if dir_name not in cwd.contents:
                        cwd.contents[dir_name] = Directory(dir_name, cwd)
                else:
                    # File entry
                    size, file = int(ls_line[0]), ls_line[1]
                    cwd.contents[file] = File(file, size)

                i += 1

    root_dir.compute_size()

    return root_dir


def sum_dir_sizes(output, max_size):
    """
    Task 1: Find all the directories with size less than or equal to max_size
    and add up their sizes.
    """
    root_dir = parse_output(output)
    
    s = 0
    for d in root_dir.walk(include_files=False):
        if d.size <= max_size:
            s += d.size
    
    return s


def delete_dir(output, total_size, target):
    """
    Task 2: Given the total size of the drive, find the smallest 
    directory that, if deleted, would result in at least "target"
    bytes of available space.
    """
    root_dir = parse_output(output)

    available = total_size - root_dir.size

    best_dir = None
    for d in root_dir.walk(include_files=False):
        if best_dir is None or (available + d.size > target and d.size < best_dir.size):
            best_dir = d

    return best_dir.size


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/07.in", sep="\n", sep2=" ")
    input = util.read_strs("input/07.in", sep="\n", sep2=" ")

    print("TASK 1")
    util.call_and_print(sum_dir_sizes, sample, 100000)
    util.call_and_print(sum_dir_sizes, input, 100000)

    print("\nTASK 2")
    util.call_and_print(delete_dir, sample, 70000000, 30000000)
    util.call_and_print(delete_dir, input, 70000000, 30000000)
