# coding: utf-8

from pyparsing import (
    Combine, Literal, White, Word, nums, Optional, oneOf, alphas
)

from .converters import to_float, to_date, to_time


space = White(ws=" ", exact=1)

colon = Literal(":")
comma = Literal(",")
point = Literal(".")

l_paren = Literal("(")
r_paren = Literal(")")

l_bracket = Literal("[")
r_bracket = Literal("]")

plus_or_minus = Literal("+") | Literal("-")

number = Word(nums)
integer = Combine(Optional(plus_or_minus) + number)
float_number = Combine(
    integer + Optional(point + number)
).setParseAction(to_float)

# Example: "AM" or "PM"
day_period = Combine(
    oneOf("A P") + Literal("M")
).setResultsName("day_period")

# Example: "8:33:05 PM" or "08:33:05 PM"
time = Combine(
    Word(nums, min=1, max=2)              # Hours (e.g. 8, 08 or 18)
    + (colon + Word(nums, exact=2)) * 2   # Minutes and seconds
    + space
    + day_period
).setResultsName("time").setParseAction(to_time)

# Example: "Sep 15, 2013"
date = Combine(
    Word(alphas, exact=3)       # Month abbreviation (e.g. Jan, Feb, Sep, etc.)
    + space                     #
    + Word(nums, min=1, max=2)  # Day number (e.g. 8, 08 or 18)
    + comma                     #
    + space                     #
    + Word(nums, exact=4)       # Year
).setResultsName("date").setParseAction(to_date)

# Example: "Sep 15, 2013 8:33:05 PM"
date_time = Combine(date + space + time)
