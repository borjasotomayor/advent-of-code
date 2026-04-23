"""
Day 9
https://adventofcode.com/2024/day/9

This was a really fun, systems-y problem to solve
(in general, I enjoy any problem that is a classic
OS/architecture algorithm in disguise). In this case,
Part 2 basically involved implementing a free list
(https://en.wikipedia.org/wiki/Free_list), although
I'm sure there are more efficient ways of solving
the problem.

For Part 1, I did come up with a pretty efficient
array-based implementation in NumPy (but one that
would make implementing Part 2 challenging)

I also ended up cleaning up my code to use classes,
which made some parts of the code much clearer.
"""

import util

from util import log

import numpy as np
import numpy.typing as npt

class DiskBlockMap:
    """
    Class to represent a disk using a block map
    """

    _disk_map: list[int]
    _num_files: int
    _num_blocks: int
    _block_map: npt.NDArray[np.uint32]

    def __init__(self, disk_map: str):
        """
        Constructor
        """
        self._disk_map = [int(x) for x in disk_map]
        self._num_blocks = sum(self._disk_map)
        self._block_map = np.zeros(self._num_blocks, dtype=np.int32)

        # Convert the disk map into an array of blocks,
        # where every entry contains a file number,
        # or a -1 to denote free space
        # (we could use NumPy's masked arrays instead)
        is_file = True
        file_num = 0
        idx = 0
        for block in self._disk_map:
            for _ in range(block):
                if is_file:
                    self._block_map[idx] = file_num
                else:
                    self._block_map[idx] = -1
                idx += 1
            if is_file:
                file_num += 1
            is_file = not is_file
        
        self._num_files = file_num

    def block_defragment(self) -> None:
        """ 
        Defragment the disk one block at a time
        """
        front = self._disk_map[0]
        back = self._num_blocks - 1
        while front < back:
            self._block_map[front] = self._block_map[back]
            self._block_map[back] = -1
            while front < self._num_blocks and self._block_map[front] != -1:
                front += 1
            while back >= 0 and self._block_map[back] == -1:
                back -= 1

    def __str__(self) -> str:
        """
        Return a string representation like the one in the problem statement
        """
        if self._num_files > 10:
            return "<too many files>"
        else:
            sa = self._block_map.astype(str)
            sa[sa == "-1"] = "."
            return "".join(sa)

    @property
    def checksum(self) -> int:
        """
        Compute checksum
        """
        ca = np.where(self._block_map == -1, 0, self._block_map)
        return int(np.sum(ca * np.arange(self._num_blocks)))


class DiskBlockList:
    """
    Class for representing a disk using a list of used/free clusters
    of blocks
    """
    _disk_map: list[int]
    _num_files: int
    _num_blocks: int

    # We manage the list as a doubly-linked list
    _head: "ListNode | None"
    _tail: "ListNode | None"

    class ListNode:
        """
        Node in the linked list
        """
        prev: "DiskBlockList.ListNode | None"
        next: "DiskBlockList.ListNode | None"
        is_file: bool
        num_blocks: int
        file_num: int | None

        def __init__(self, is_file: bool, num_blocks: int, file_num: int | None):
            """
            Node constructor
            """
            self.prev = None
            self.next = None
            self.is_file = is_file
            self.num_blocks = num_blocks
            self.file_num = file_num

    def __init__(self, disk_map: str):
        """
        Constructor
        """
        self._disk_map = [int(x) for x in disk_map]
        self._num_blocks = sum(self._disk_map)
        self._block_map = np.zeros(self._num_blocks, dtype=np.int32)
        self._head = None
        self._tail = None

        # Convert the disk map into a list where each
        # node represents a cluster of blocks that either
        # belong to a file or are empty space.
        is_file = True
        file_num = 0
        for num_blocks in self._disk_map:
            if is_file:
                self._append_blocks(is_file, num_blocks, file_num)
                file_num += 1
            else:
                self._append_blocks(is_file, num_blocks)
            is_file = not is_file
        
        self._num_files = file_num

    def _append_blocks(self, is_file: bool, num_blocks: int, file_num: int | None = None) -> None:
        """
        Helper method to create nodes in the list
        """
        node = DiskBlockList.ListNode(is_file, num_blocks, file_num)

        if self._head is None and self._tail is None:
            self._head = node
            self._tail = node
        else:
            assert self._head is not None and self._tail is not None
            self._tail.next = node
            node.prev = self._tail
            self._tail = node

    def file_defragment(self) -> None:
        """
        Defragment the disk one file at a time
        """
        assert self._head is not None
        p_file: "DiskBlockList.ListNode" | None = self._tail
        p_first_free: "DiskBlockList.ListNode" | None = self._head

        file_num = self._num_files - 1
        assert p_file is not None
        assert p_file.file_num == file_num
        
        while file_num > 0 and p_file is not None:
            # To avoid confusion, we'll refer to the current node
            # as "node" (since it could change from a file to a free node)
            node = p_file

            # Try to find an empty space large enough for this file
            p_free: "DiskBlockList.ListNode" | None = p_first_free
            while p_free is not None and p_free != node and not (not p_free.is_file and p_free.num_blocks >= node.num_blocks):
                p_free = p_free.next

            if p_free is not None and p_free != node:
                # We found a block large enough
                # (and we also didn't go past the file; we only want
                # spaces that are to the left of the file)

                # Convert the free block into a file block
                new_free_blocks = p_free.num_blocks - node.num_blocks
                
                p_free.is_file = True
                p_free.file_num = node.file_num
                p_free.num_blocks = node.num_blocks

                # If this still leaves a gap with the next file,
                # create a new free block between the file and the next file
                if new_free_blocks > 0 and p_free.next is not None:
                    assert p_free.next.is_file
                    new_node = DiskBlockList.ListNode(False, new_free_blocks, None)
                    new_node.prev = p_free
                    new_node.next = p_free.next

                    new_node.next.prev = new_node
                    p_free.next = new_node

                # Finally, convert the file block into a free block
                node.is_file = False
                node.file_num = None

                # If there is free space to the left, we merge with it
                if node.prev is not None and not node.prev.is_file:
                    node.prev.num_blocks += node.num_blocks
                    node.prev.next = node.next
                    if node.next is None:
                        self._tail = node.prev
                    else:
                        node.next.prev = node.prev
                    node = node.prev

                # If there is free space to the right, we merge with it
                # (note we don't do an elif, so it's possible for this
                # to handle merging three contiguous free blocks)
                if node.next is not None and not node.next.is_file:
                    node.num_blocks += node.next.num_blocks
                    node.next = node.next.next
                    if node.next is None:
                        self._tail = node
                    else:
                        node.next.prev = node
            
            # Advance (going backwards) to the next file node
            file_num -= 1
            while p_file is not None and p_file.file_num != file_num:   
                p_file = p_file.prev            

            # Update the pointer to the first free node
            while p_first_free is not None and not p_first_free.is_file:   
                p_first_free = p_first_free.next   

    def __str__(self) -> str:
        """
        Return a string representation like the one in the problem statement
        """
        if self._num_files > 10:
            return "<too many files>"
        else:
            p = self._head
            sl = []
            while p is not None:
                if p.is_file:
                    char = str(p.file_num)
                else:
                    char = "."
                sl.append(char * p.num_blocks)
                p = p.next
            return "|".join(sl)
        
    @property
    def checksum(self) -> int:
        """
        Compute checksum
        """
        p = self._head
        rv = 0
        block_num = 0
        while p is not None:
            if p.is_file:
                assert p.file_num is not None
                for b in range(block_num, block_num + p.num_blocks):
                    rv += b * p.file_num
            
            block_num += p.num_blocks
            p = p.next
        
        return rv


def task1(disk_str: str) -> int:
    """
    Part 1: Defragment one block at a time
    """
    disk = DiskBlockMap(disk_str)
    disk.block_defragment()
    return disk.checksum


def task2(disk_str: str) -> int:
    """
    Part 2: Defragment one file at a time
    """
    disk = DiskBlockList(disk_str)
    disk.file_defragment()
    return disk.checksum


if __name__ == "__main__":
    util.set_debug(True)

    sample = util.read_strs("input/sample/09.in")[0]
    input = util.read_strs("input/09.in")[0]

    print("TASK 1")
    util.call_and_print(task1, sample)
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(task2, sample)
    util.call_and_print(task2, input)
