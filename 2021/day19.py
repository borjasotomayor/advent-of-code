"""
Day 19
https://adventofcode.com/2021/day/19

1st star: >24h (*)
2nd star: >24h (*)

(*) I was on vacation when this problem was solved, so I wasn't 
    able to solve it right when it was released. 

Well, I was wondering when Advent of Code would unleash the
equivalent of last year's sea creatures, and I guess I got
my answer...

Figuring out the solution ended up involving a fair amount of
trial and error but, fortunately, I landed on an approach that
produces the absolute coordinates of all the scanners
and beacons (as opposed to only finding the number of unique
beacons), which made solving part 2 practically trivial.

That said, this is still a fairly brute force-ish solution.
The key insight was computing the coordinates of a scanner's beacons
relative to one of the beacons. If you find a beacon (in a 
different scanner) that has the same relative positions (with
eleven other beacons in that scanner, for a total of twelve
when you count the beacon you're checking), then those two 
beacons are the same beacon. Then it's just a question of checking
this for every possible pair of beacons... and for each of the 24
ways of transforming the coordinates.

My solution originally ran in close to two minutes, but I managed
to bring it down to 40 seconds, after a few optimizations and
after some judicious use of @lru_cache.
"""

import util
import math
from functools import cached_property, lru_cache

from util import log


# A bunch of useful functions for working with coordinates

@lru_cache(maxsize=None) 
def coords_add(coords1, coords2):
    """
    Add two coordinates together
    """
    x1, y1, z1 = coords1
    x2, y2, z2 = coords2

    return (x1+x2, y1+y2, z1+z2)

@lru_cache(maxsize=None) 
def coords_subtract(coords1, coords2):
    """
    Subtract coords2 from coords1
    """
    x1, y1, z1 = coords1
    x2, y2, z2 = coords2

    return (x1-x2, y1-y2, z1-z2)

def coords_manhattan(coords1, coords2):
    """
    Compute the Manhattan distance between two coordinates
    """
    x1, y1, z1 = coords1
    x2, y2, z2 = coords2

    return abs(x2-x1) + abs(y2-y1) + abs(z2-z1)

@lru_cache(maxsize=None) 
def coords_transform(coords, transform):
    """
    Applies a tranformation to (x, y, z) coordinates.
    A transformation is a (sx, sy, sz, m) tuple where
    sx, sy, sz are multipliers for each coordinate
    (in this problem, they are only ever -1 or 1),
    and m is a tuple of indices (e.g., m=(1,0,2) would
    move the values (x,y,z) into (y,x,z))
    """
    x, y, z = coords
    sx, sy, sz, m = transform
    tx = sx*x
    ty = sy*y
    tz = sz*z

    nrp = [None,None,None]
    nrp[m[0]] = tx
    nrp[m[1]] = ty
    nrp[m[2]] = tz

    return tuple(nrp)


class Beacon:
    """
    Class for representing a beacon associated to a specific scanner
    (i.e., there could be other Beacon objects in other scanners
    that refer to the same beacon)
    """

    def __init__(self, scanner, beacon_num, coords):
        self.scanner = scanner
        self.beacon_num = beacon_num

        # The relative coordinates given in the input
        self.rel_coords = coords

        # The absolute coordinates (relative to scanner 0)
        self.coords = None

    def __get_rel_coordinates_other_beacons(self, absolute):
        """
        Computes the coordinates of all the other beacons in this scanner,
        relative to this beacon.

        If absolute is True, we use the absolute coordinates of the beacons
        (otherwise we use the relative coordinates given in the input)
        """

        if absolute:
            assert self.coords is not None
            x, y, z = self.coords
        else:
            x, y, z = self.rel_coords

        rel_positions = set()
        for beacon in self.scanner.beacons:
            if self != beacon:
                if absolute:
                    assert beacon.coords is not None
                    x2, y2, z2 = beacon.coords
                else:
                    x2, y2, z2 = beacon.rel_coords

                rel_positions.add((x2-x, y2-y, z2-z))
        
        return rel_positions

    # The following properties slightly optimize access to the
    # values computed by the __get_rel_coordinates_other_beacons method
    @cached_property
    def beacons_rel_coordinates_from_rel(self):
        return self.__get_rel_coordinates_other_beacons(absolute=False)

    @cached_property
    def beacons_rel_coordinates_from_abs(self):
        return self.__get_rel_coordinates_other_beacons(absolute=True)

    # Dunder methods for debugging

    def __str__(self):
        return f"S{self.scanner.num}B{self.beacon_num} {self.coords}"    

    def __repr__(self):
        return str(self)


class Scanner:
    """
    Class for representing scanners. Contains Beacon objects corresponding
    to the beacons that are detected by this scanner.
    """

    def __init__(self, num, beacons):
        self.num = num

        # Absolute coordinates of the scanner. Initially unknown.
        self.coords = None

        # Create Beacon objects
        self.beacons = []
        for i, beacon in enumerate(beacons):
            self.beacons.append(Beacon(self, i, beacon))

    @lru_cache(maxsize=None)        
    def find_matching_beacon(self, beacon):
        """
        Given a beacon (from a different scanner) see if there is a matching
        beacon in this scanner. We do this by computing the coordinates
        of all the other beacons relative to a beacon, instead of the scanner),
        and checking whether there are 12 beacons with the same relative positions.

        If there is matching beacon, return the beacon as well as the
        transformation parameters (see coords_transform for details on what
        this means)
        """
        # Get the relative coordinates of the beacons in the same scanner
        # as the given beacon (starting from the beacon's absolute coordinates)
        rel_coordinates1 = beacon.beacons_rel_coordinates_from_abs

        for b2 in self.beacons:
            # Get the coordinates of the beacons in this scanner, relative
            # to the beacon we are checking (b2)
            rel_coordinates2 = b2.beacons_rel_coordinates_from_rel

            # We check all 24 ways to tranform the coordinates
            for sx in (-1, 1):
                for sy in (-1, 1):
                    for sz in (-1, 1):
                        for m in [(0,1,2), (0,2,1), (1,0,2), (1,2,0), (2,1,0), (2,0,1)]:
                            # Compute the transformed coordinates
                            rel_coordinates2_transformed = set()
                            transform = sx, sy, sz, m
                            for rp2 in rel_coordinates2:
                                tcoords = coords_transform(rp2, transform)
                                rel_coordinates2_transformed.add(tcoords)

                            # If there are 11 common beacons (which becomes 12
                            # if we include the beacon we're checking)
                            # we have a match.
                            overlap = rel_coordinates1 & rel_coordinates2_transformed
                            if len(overlap) == 11:
                                return b2, (sx, sy, sz, m)

        return None, None

    def set_coords(self, coords, transform):
        """
        Set the coordinates for the scanner and its beacons,
        applying the given transformation (see coords_transform for
        more details)
        """
        self.coords = coords

        for beacon in self.beacons:
            bcoords = coords_transform(beacon.rel_coords, transform)
            abs_coords = coords_add(coords, bcoords)
            beacon.coords = abs_coords

    def check_overlap(self, other):
        """
        Assuming this scanner has its absolute coordinates set,
        check if it has overlapping beacons with another scanner. If so,
        update the other scanner and set its absolute coordinates
        (and those of its beacons)
        """
        assert self.coords is not None

        scanner_coords = None
        transform = None

        # Check each beacon in this scanner, and see if
        # if matches a beacon in the other scanner.
        for b1 in self.beacons:
            b2, btransform = other.find_matching_beacon(b1)

            if b2 is not None:
                if transform is None:
                    transform = btransform
                else:
                    assert btransform == transform

                # Transform the coordinates of the other scanner's
                # beacon into absolute coordinates, so we can 
                # figure out the position of the scanner.
                tcoords = coords_transform(b2.rel_coords, transform)
                scoords = coords_subtract(b1.coords, tcoords)

                if scanner_coords is None:
                    scanner_coords = scoords
                
                    # Note that we don't need to wait until we've checked
                    # 12 beacons, because find_matching_beacon already
                    # checks for this.
                    break
        
        if scanner_coords is not None:
            other.set_coords(scanner_coords, transform)

    # Dunder methods for debugging

    def __str__(self):
        return f"[S{self.num} {self.rel_coords} {self.coords}]"
    
    def __repr__(self):
        return str(self)


def compute_coords(scanners):
    """
    Computes the absolute coordinates of all the scanners and beacons.
    """

    # The absolute coordinates of scanner 0 are just the relative coordinates
    # given in the input (assuming the scanner is at (0,0,0))
    scanners[0].coords = (0,0,0)
    for beacon in scanners[0].beacons:
        beacon.coords = beacon.rel_coords
    
    # We keep checking overlaps between scanners until they all have their
    # absolute coordinates filled in.
    while True:
        for scanner1 in scanners:
            # If we haven't found the absolute coordinates for scanner1 yet,
            # we can't use it yet to find the coordinates of other scanners.
            # Skip it.
            if scanner1.coords is None:
                continue

            for scanner2 in scanners:
                # We don't check a scanner with itself, and we skip scanners
                # whose coordinates we have already found.
                if scanner1 != scanner2 and scanner2.coords is None:
                    util.log(f"Checking overlap between S{scanner1.num} and S{scanner2.num}")
                    scanner1.check_overlap(scanner2)

        # Check if we've found coordinates for all the scanners.
        if all(s.coords is not None for s in scanners):
            break

def read_input(input):
    """
    Reads in the input and creates all the necessary Scanner and Beacon objects
    """
    scanners = []
    for i, scanner_txt in enumerate(input):
        coords_lines = scanner_txt.split("\n")
        coords_lines.pop(0)
        coords = []
        for x, y, z in util.iter_parse(coords_lines, "{:d},{:d},{:d}"):
            coords.append((x,y,z))   
        scanners.append(Scanner(i, coords))
    return scanners

def solve(input):
    """
    Tasks 1 + 2: Finds the number of beacons and the largest manhattan
    distance between the scanners.
    """
    scanners = read_input(input)
    
    # Compute the coordinates of all the scanners and beacons
    compute_coords(scanners)

    # Find all the unique beacon coordinates
    beacon_coords = set()
    for scanner in scanners:
        for beacon in scanner.beacons:
            assert beacon.coords is not None
            beacon_coords.add(beacon.coords)

    # Find the maximum Manhattan distance
    max_dist = 0
    for scanner1 in scanners:
        for scanner2 in scanners:
            dist = coords_manhattan(scanner1.coords, scanner2.coords)
            if dist > max_dist:
                max_dist = dist

    return len(beacon_coords), max_dist


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/19.in", sep="\n\n")
    input = util.read_strs("input/19.in", sep="\n\n")

    print("TASK 1 + 2")
    util.call_and_print(solve, sample)
    util.call_and_print(solve, input)
