"""
Day 16
https://adventofcode.com/2021/day/16

1st star: 00:44:22
2nd star: 00:49:05

Given that I am a network protocol geek, and love digging into specs
of packets, header formats, etc. I loved loved loved this problem.
I wrote it in Python, as I did all my AoC problems, but I kinda want
to reimplement it in C.

The code below is effectively the same code I wrote to obtain the solution,
except for some cleaning up. I invested in writing a Packet class in Part 1, 
and that paid off handsomely in Part 2 (all I had to do was add an eval()
method to the Packet class, and everything fell into place beautifully)
"""

import util
import math
import sys
import re

from util import log

class Packet:
    """
    Class for representing packets
    """

    # Useful constants
    VERSION_LEN = 3
    TYPE_LEN = 3
    HEADER_LEN = VERSION_LEN + TYPE_LEN
    LITERAL_VALUE_BLOCK_LEN = 5
    SUBPACKET_LEN_BITS_LEN = 15
    SUBPACKET_LEN_NUM_LEN = 11

    SUBPACKET_LEN_TYPE_BITS = 0
    SUBPACKET_LEN_TYPE_NUM = 1

    TYPE_SUM = 0
    TYPE_PRODUCT = 1
    TYPE_MINIMUM = 2
    TYPE_MAXIMUM = 3
    TYPE_LITERAL = 4
    TYPE_GT = 5
    TYPE_LT = 6
    TYPE_EQ = 7


    def __init__(self, bin_str):
        """
        Constructor. Takes a binary string (e.g., "0101011101") as its
        only parameter.
        """
        self.bin_str = bin_str
        self.sub_packets = []

        if self.type == Packet.TYPE_LITERAL:
            # This packet contains a literal value. We need to extract
            # the value from the blocks after the header.

            raw_bin_value = self.bin_str[Packet.HEADER_LEN:]

            i = Packet.HEADER_LEN
            bin_value = ""
            self.len_value = 0
            while True:
                pad = self.bin_str[i]
                bin_value += self.bin_str[i+1:i+Packet.LITERAL_VALUE_BLOCK_LEN]
                self.len_value += Packet.LITERAL_VALUE_BLOCK_LEN
                if pad == "0":
                    break
                i += Packet.LITERAL_VALUE_BLOCK_LEN

            self.literal_value = int(bin_value, 2)

        elif self.type != Packet.TYPE_LITERAL:
            # This is an operator packet. We need to recursively compute
            # the subpackets.
            if self.length_type == Packet.SUBPACKET_LEN_TYPE_BITS:
                lb = Packet.HEADER_LEN + 1
                ub = lb + Packet.SUBPACKET_LEN_BITS_LEN
                sub_packets_len = int(self.bin_str[lb:ub],2)

                start = ub
                while sub_packets_len != 0:
                    assert sub_packets_len > 0

                    p = Packet(self.bin_str[start:])
                    self.sub_packets.append(p)
                    sub_packets_len -= p.length
                    start += p.length

            elif self.length_type == Packet.SUBPACKET_LEN_TYPE_NUM:
                lb = Packet.HEADER_LEN + 1
                ub = lb + Packet.SUBPACKET_LEN_NUM_LEN
                num_packets = int(self.bin_str[lb:ub], 2)

                start = ub
                for i in range(num_packets):
                    p = Packet(self.bin_str[start:])
                    self.sub_packets.append(p)
                    start += p.length

        # Might as well trim all the excess bits
        self.bin_str = self.bin_str[:self.length]


    def eval(self):
        """
        Evaluate the value of a packet, recursively evaluating
        sub-packets if necessary
        """
        if self.type == Packet.TYPE_SUM:
            return sum(p.eval() for p in self.sub_packets)
        if self.type == Packet.TYPE_PRODUCT:
            return math.prod(p.eval() for p in self.sub_packets)
        if self.type == Packet.TYPE_MINIMUM:
            return min(p.eval() for p in self.sub_packets)
        if self.type == Packet.TYPE_MAXIMUM:
            return max(p.eval() for p in self.sub_packets)
        if self.type == Packet.TYPE_LITERAL:
            return self.literal_value
        if self.type in (Packet.TYPE_GT, Packet.TYPE_LT, Packet.TYPE_EQ):
            p1 = self.sub_packets[0]
            p2 = self.sub_packets[1]

            if self.type == Packet.TYPE_GT:
                return 1 if p1.eval() > p2.eval() else 0
            if self.type == Packet.TYPE_LT:
                return 1 if p1.eval() < p2.eval() else 0
            if self.type == Packet.TYPE_EQ:
                return 1 if p1.eval() == p2.eval() else 0

    @property
    def version(self):
        return int(self.bin_str[:Packet.VERSION_LEN], 2)

    @property
    def type(self):
        return int(self.bin_str[Packet.VERSION_LEN:Packet.HEADER_LEN], 2)

    @property
    def length_type(self):
        return int(self.bin_str[Packet.HEADER_LEN], 2)

    @property
    def length(self):
        if self.type == 4:
            return 6 + self.len_value
        else:
            if self.length_type == 0:
                return 22 + sum(p.length for p in self.sub_packets)
            elif self.length_type == 1:
                return 18 + sum(p.length for p in self.sub_packets)


    @classmethod
    def from_hex(cls, hex):
        """
        Create a Packet object starting from a hex string
        """
        h_size = len(hex) * 4
        bin_str = bin(int(hex, 16))[2:].zfill(h_size)

        return cls(bin_str)

    def __str__(self):
        """
        Produce a minimal string representation of the packet
        """
        if self.type == 4:
            return f"V={self.version} T={self.type} V={self.literal_value} len={self.length}"
        else:
            s = f"V={self.version} T={self.type} LT={self.length_type} "
            if self.length_type == 0:
                s += f"SPL={int(self.bin_str[7:22],2)} "
            elif self.length_type == 1:
                s += f"SPN={int(self.bin_str[7:18],2)} "
            return s + f"PACKETS={len(self.sub_packets)} len={self.length}"


def sum_versions(packet):
    """
    Recursively add up the versions from all the packets
    (and their subpackets)
    """

    rv = packet.version

    for p in packet.sub_packets:
        rv += sum_versions(p)

    return rv


def task1(hex):
    """
    Task 1: Add up the versions in all the packets.
    """    
    return sum_versions(Packet.from_hex(hex))


def eval(hex):
    """
    Task 2: Evaluate a packet
    """
    return Packet.from_hex(hex).eval()


def test_packets():
    """
    Print the example packets (and their subpackets) from the problem 
    to make sure everything looks good.
    """

    p1 = Packet.from_hex("D2FE28")
    print(p1)
    print()

    p2 = Packet.from_hex("38006F45291200")
    print(p2)
    for p in p2.sub_packets:
        print(p)
    print()

    p3 = Packet.from_hex("EE00D40C823060")
    print(p3)
    for p in p3.sub_packets:
        print(p)
    print()


if __name__ == "__main__":
    util.set_debug(False)

    test_packets()

    input = util.read_strs("input/16.in")[0]

    print("TASK 1")
    util.call_and_print(task1, "8A004A801A8002F478")
    util.call_and_print(task1, "620080001611562C8802118E34")
    util.call_and_print(task1, "C0015000016115A2E0802F182340")
    util.call_and_print(task1, "A0016C880162017C3686B18A3D4780")
    util.call_and_print(task1, input)

    print("\nTASK 2")
    util.call_and_print(eval, "C200B40A82")
    util.call_and_print(eval, "04005AC33890")
    util.call_and_print(eval, "880086C3E88112")
    util.call_and_print(eval, "CE00C43D881120")
    util.call_and_print(eval, "D8005AC2A8F0")
    util.call_and_print(eval, "F600BC2D8F")
    util.call_and_print(eval, "9C005AC2F8F0")
    util.call_and_print(eval, "9C0141080250320F1802104A08")
    util.call_and_print(eval, input)
