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
"""

import util
import math
import sys
import re

from util import log

# Validators (inspired by the kind of field validators you find in many
# frameworks, such as Django)
#
# A validator is a class with a "validate(value)" method. The Passport
# class can associate different validators with each field (and the
# validator constructor can customize how the value will be validated)

class IntValidator:
    """
    Validates that an integer is between a lower and upper bound
    (both inclusive)
    """
    def __init__(self, lb, ub):
        self.lb = lb
        self.ub = ub

    def validate(self, value):
        value = int(value)

        return self.lb <= value <= self.ub


class RegexValidator:
    """
    Validates that a string matches a regular expression
    """
    def __init__(self, regex):
        self.re = re.compile(regex)

    def validate(self, value):
        if self.re.fullmatch(value) is not None:
            return True
        else:
            return False         


class MeasurementValidator:
    """
    Similar to IntValidator, but allowing for units of measurement
    after the integer.

    The ranges parameter to the constructor is a dictionary mapping
    units of measurement to integer ranges, e.g.:

    {"cm": (150, 193), "in": (59, 76)}
    """
    def __init__(self, ranges):
        self.ranges = ranges

    def validate(self, value):
        unit = value[-2:]

        if unit not in self.ranges:
            return False

        amount = int(value[:-2])

        lb, ub = self.ranges[unit]

        return lb <= amount <= ub


class Passport:

    FIELDS = [("byr", True, IntValidator(1920, 2002)),
              ("iyr", True, IntValidator(2010, 2020)),
              ("eyr", True, IntValidator(2020, 2030)),
              ("hgt", True, MeasurementValidator({"cm": (150, 193), "in": (59, 76)})),
              ("hcl", True, RegexValidator("#[0-9a-f]{6}")),
              ("ecl", True, RegexValidator("amb|blu|brn|gry|grn|hzl|oth")),
              ("pid", True, RegexValidator("[0-9]{9}")),
              ("cid", False, None)]

    def __init__(self, passport_str):
        self.fields = {}

        fields = passport_str.strip().split()
        for field in fields:
            k, v = field.split(":")
            self.fields[k] = v


    def validate_field(self, key, required, validator):
        """
        Validate a single field.
        
        Parameters:
          - key (string): Field to check
          - required (boolean): Whether the field is required. i.e., if required,
            and the field is not present in the passport, it will not validate.
          - validator (Validator): A validator to be applied to the field.
            Can be None, in which case the value won't be validated.
        """
        if key not in self.fields:
            return not required

        if validator is None:
            return True

        if validator.validate(self.fields[key]):
            log(f"{key} {self.fields[key]} validates.")
            return True
        else:
            log(f"{key} {self.fields[key]} does NOT validate")
            return False


    def validate(self, validate_values=True):
        """
        Validate all the fields. If validate_values is False,
        the values themselves are not validated (we only validate
        that all required fields are present)
        """
        for field, required, validator in Passport.FIELDS:
            if not validate_values:
                validator = None
            if not self.validate_field(field, required, validator):
                return False

        return True



def validate(strings, validate_values):
    """
    Implementation of 1st star (validate_values = False) 
    and 2nd star (validate_values = True)
    """
    valid = 0
    for s in strings:
        passport = Passport(s)

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


