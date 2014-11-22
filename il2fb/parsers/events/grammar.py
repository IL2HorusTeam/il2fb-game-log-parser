# -*- coding: utf-8 -*-

from pyparsing import (
    Combine, LineStart, LineEnd, Literal, Or, Regex, White, Word, alphas, nums,
    oneOf, printables,
)

from .actions import (
    convert_time, convert_date, convert_int, convert_float, convert_pos,
    convert_toggle_value,
)
from .constants import TOGGLE_VALUES


single_space = White(ws=' ', exact=1)
float_number = Regex(r"\d+.\d+").setParseAction(convert_float)
printable_word = Word(printables.replace(':', ''))

# Example: "AM" or "PM"
day_period = Combine(
    oneOf("A P") + Literal('M')
).setResultsName('day_period')

# Example: "8:33:05 PM" or "08:33:05 PM"
time = Combine(
    Word(nums, min=1, max=2)                     # Hours (e.g. 8, 08 or 18)
    + (Literal(':') + Word(nums, exact=2)) * 2   # Minutes and seconds
    + single_space                               #
    + day_period                                 #
).setResultsName('time').setParseAction(convert_time)

# Example: "[8:33:05 PM] "
event_time = Combine(LineStart() + '[' + time + ']' + single_space)

# Example: "Sep 15, 2013"
date = Combine(
    Word(alphas, exact=3)       # Month abbreviation (e.g. Jan, Feb, Sep, etc.)
    + single_space              #
    + Word(nums, min=1, max=2)  # Day number (e.g. 8, 08 or 18)
    + ','                       #
    + single_space              #
    + Word(nums, exact=4)       # Year
).setResultsName('date').setParseAction(convert_date)

# Example: "Sep 15, 2013 8:33:05 PM"
date_time = Combine(date + single_space + time)

# Example: "[Sep 15, 2013 8:33:05 PM] "
event_date_time = Combine(LineStart() + '[' + date_time + ']' + single_space)

# Example: " at 100.0 200.99"
event_pos = Combine(
    single_space
    + Literal('at')
    + single_space
    + float_number.setResultsName('x')
    + single_space
    + float_number.setResultsName('y')
    + LineEnd()
).setResultsName('pos').setParseAction(convert_pos)

# Example: "on" or "off"
toggle_value = Or([
    Literal(x) for x in TOGGLE_VALUES.values()
]).setResultsName('toggle_value').setParseAction(convert_toggle_value)

# Example: "=XXX=User0"
callsign = printable_word.setResultsName('callsign')

# Example: "=XXX=User0:Pe-8"
aircraft = Combine(
    callsign
    + Literal(":")
    + printable_word.setResultsName('aircraft')
)

# Example: "=XXX=User1:Pe-8"
enemy_aircraft = Combine(
    callsign.setResultsName('enemy_callsign')
    + Literal(":")
    + printable_word.setResultsName('enemy_aircraft')
)

# Example: "(0)"
seat_number = Combine(
    Literal('(')
    + Word(nums).setParseAction(convert_int).setResultsName('seat_number')
    + Literal(')')
)

# Example: "0_Static"
static = Combine(
    Word(nums) + Literal('_Static')
).setResultsName('static')
