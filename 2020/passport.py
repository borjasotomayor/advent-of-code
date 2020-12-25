"""
This is my beautifully refactored Passport code from Day 4, which I
never got to use. I was *convinced* we were going to see passports
in more problems but, alas, it was not to be.
"""

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


class Field:

    def __init__(self, name, required, validator=None):
        self.name = name
        self.required = required
        self.validator = validator


class PassportType:

    def __init__(self, name):
        self.name = name
        self.fields = {}

    def add_field(self, field):
        self.fields[field.name] = field

    def validate_field(self, field_name, value):
        """
        Validate a single field.
        """
        field = self.fields[field_name]

        if field.validator is None:
            return True

        if field.validator.validate(value):
            log(f"{field_name} {value} validates.")
            return True
        else:
            log(f"{field_name} {value} does NOT validate")
            return False

    def validate_fields(self, fields, validate_values):
        for field_name, field in self.fields.items():
            if field_name not in fields:
                if field.required:
                    return False
                else:
                    continue
            if validate_values:
                if not self.validate_field(field_name, fields[field_name]):
                    return False

        return True


class Passport:

    def __init__(self, fields, passport_type=None):
        self.passport_type = passport_type
        self.fields = fields


    def validate(self, validate_values=True):
        """
        Validate all the fields. If validate_values is False,
        the values themselves are not validated (we only validate
        that all required fields are present)
        """
        if self.passport_type is None:
            return True
        else:
            return self.passport_type.validate_fields(self.fields, validate_values)

    @classmethod
    def passport_from_str(cls, passport_str, passport_type=None):
        fields = {}

        fields_str = passport_str.strip().split()
        for field in fields_str:
            k, v = field.split(":")
            fields[k] = v

        return cls(fields, passport_type)


REGULAR_PASSPORT = PassportType("regular")
REGULAR_PASSPORT.add_field(Field("byr", True, IntValidator(1920, 2002)))
REGULAR_PASSPORT.add_field(Field("iyr", True, IntValidator(2010, 2020)))
REGULAR_PASSPORT.add_field(Field("eyr", True, IntValidator(2020, 2030)))
REGULAR_PASSPORT.add_field(Field("hgt", True, MeasurementValidator({"cm": (150, 193), "in": (59, 76)})))
REGULAR_PASSPORT.add_field(Field("hcl", True, RegexValidator("#[0-9a-f]{6}")))
REGULAR_PASSPORT.add_field(Field("ecl", True, RegexValidator("amb|blu|brn|gry|grn|hzl|oth")))
REGULAR_PASSPORT.add_field(Field("pid", True, RegexValidator("[0-9]{9}")))
REGULAR_PASSPORT.add_field(Field("cid", False, None))
