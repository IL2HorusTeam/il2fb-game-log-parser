# -*- coding: utf-8 -*-

from il2fb.commons.organization import Belligerents
from pyparsing import (
    Combine, LineStart, LineEnd, Literal, Or, White, Word, alphas, nums,
    alphanums, oneOf, Suppress, Optional,
)

from .actions import (
    convert_time, convert_date, convert_int, convert_float, convert_pos,
    convert_toggle_value, convert_belligerent,
)
from .constants import TOGGLE_VALUES


#------------------------------------------------------------------------------
# Primmitives
#------------------------------------------------------------------------------

space = White(ws=' ', exact=1)

colon = Literal(':')
comma = Literal(',')
point = Literal('.')
plus_or_minus = Literal('+') | Literal('-')

number = Word(nums)
integer = Combine(Optional(plus_or_minus) + number)
float_number = Combine(
    integer + Optional(point + Optional(number))
).setParseAction(convert_float)

callsign_chars = alphanums + "!#%$&)(+*-/.=<>@[]_^{}|~"
aircraft_chars = Word(alphanums + "_-")

#------------------------------------------------------------------------------
# Helpers
#------------------------------------------------------------------------------

# Example: "AM" or "PM"
day_period = Combine(
    oneOf("A P") + Literal('M')
).setResultsName('day_period')

# Example: "8:33:05 PM" or "08:33:05 PM"
time = Combine(
    Word(nums, min=1, max=2)              # Hours (e.g. 8, 08 or 18)
    + (colon + Word(nums, exact=2)) * 2   # Minutes and seconds
    + space
    + day_period
).setResultsName('time').setParseAction(convert_time)

# Example: "[8:33:05 PM] "
event_time = Combine(LineStart() + '[' + time + ']' + space)

# Example: "Sep 15, 2013"
date = Combine(
    Word(alphas, exact=3)       # Month abbreviation (e.g. Jan, Feb, Sep, etc.)
    + space              #
    + Word(nums, min=1, max=2)  # Day number (e.g. 8, 08 or 18)
    + comma                     #
    + space              #
    + Word(nums, exact=4)       # Year
).setResultsName('date').setParseAction(convert_date)

# Example: "Sep 15, 2013 8:33:05 PM"
date_time = Combine(date + space + time)

# Example: "[Sep 15, 2013 8:33:05 PM] "
event_date_time = Combine(LineStart() + '[' + date_time + ']' + space)

# Example: " at 100.0 200.99"
event_pos = Combine(
    space
    + Suppress('at')
    + space
    + float_number.setResultsName('x')
    + space
    + float_number.setResultsName('y')
    + LineEnd()
).setResultsName('pos').setParseAction(convert_pos)

# Example: "on" or "off"
toggle_value = Or([
    Literal(x) for x in TOGGLE_VALUES.values()
]).setResultsName('toggle_value').setParseAction(convert_toggle_value)

# Example: "=XXX=User0"
callsign = Word(callsign_chars).setResultsName('callsign')

# Example: "=XXX=User0:Pe-8"
aircraft = (
    callsign
    + colon.suppress()
    + aircraft_chars.setResultsName('aircraft')
)

# Example: "=XXX=User1:Pe-8"
enemy_aircraft = (
    callsign.setResultsName('enemy_callsign')
    + colon.suppress()
    + aircraft_chars.setResultsName('enemy_aircraft')
)

# Example: "(0)"
seat_number = (
    Suppress('(')
    + number.setParseAction(convert_int).setResultsName('seat_number')
    + Suppress(')')
)

# Example: "User:Pe-8(0)"
crew_member = aircraft + seat_number

# Example: "0_Static"
static = Combine(
    number + Literal('_Static')
).setResultsName('static')

# Example: "Bridge0"
bridge = Combine(
    Literal('Bridge') + number
).setResultsName('bridge')

# Example: "Red" or "Blue"
belligerent = Or([
    Literal(x.title()) for x in Belligerents.names()
]).setResultsName('belligerent').setParseAction(convert_belligerent)

# Example: " destroyed by User:Pe-8 at 100.0 200.99"
destroyed_by = Combine(
    space
    + Literal('destroyed')
    + space
    + Literal('by')
    + space
    + aircraft
    + event_pos
)

#------------------------------------------------------------------------------
# Events
#------------------------------------------------------------------------------

# TODO:
