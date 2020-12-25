"""
Day 4
https://adventofcode.com/2020/day/4

1st star: 00:08:52
2nd star: 00:21:32

My first version of this code was a garbage fire full of janky parsing
and rote checks (mostly because I didn't have regexes fresh in my mind,
so I validated a lot of the fields much more laboriously). 

After getting the stars, I cleaned the code up considerably 
by writing a Passport class and a basic framework for field validators.
I wouldn't be surprised if these "passports" show up again in future
puzzles, and having a decent API for dealing with them seems
like a worthwhile investment.

UPDATE 12/25: "Narrator: it was not, in fact, a worthwhile investment"
"""

import util
import math
import sys
import re
from passport import Passport, REGULAR_PASSPORT

from util import log


def validate(strings, validate_values):
    """
    Implementation of 1st star (validate_values = False) 
    and 2nd star (validate_values = True)
    """
    valid = 0
    for s in strings:
        passport = Passport.passport_from_str(s, passport_type=REGULAR_PASSPORT)

        log(passport.fields)
        if passport.validate(validate_values):
            log("VALID")
            valid += 1
        log()

    return valid


if __name__ == "__main__":
    util.set_debug(False)

    sample = util.read_strs("input/sample/04.in", sep="\n\n")
    sample_invalid = util.read_strs("input/sample/04-invalid.in", sep="\n\n")
    sample_valid = util.read_strs("input/sample/04-valid.in", sep="\n\n")
    passports = util.read_strs("input/04.in", sep="\n\n")

    print("TASK 1")
    util.call_and_print(validate, sample, False)
    util.call_and_print(validate, passports, False)

    print("\nTASK 2")
    util.call_and_print(validate, sample, True)
    util.call_and_print(validate, sample_invalid, True)
    util.call_and_print(validate, sample_valid, True)
    util.call_and_print(validate, passports, True)


