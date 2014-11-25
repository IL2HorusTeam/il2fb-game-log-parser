# -*- coding: utf-8 -*-

from il2fb.commons.organization import Belligerents
from pyparsing import (
    Combine, LineStart, LineEnd, Literal, Or, White, Word, WordStart, WordEnd,
    alphas, nums, alphanums, oneOf, Suppress, Optional, Regex,
)

from .constants import TOGGLE_VALUES
from .converters import (
    to_time, to_date, to_int, to_float, to_pos,
    to_toggle_value, to_belligerent,
)
from .structures import MissionIsPlaying, MissionBegin, MissionEnd


#------------------------------------------------------------------------------
# Primitives
#------------------------------------------------------------------------------

space = White(ws=' ', exact=1)

colon = Literal(':')
comma = Literal(',')
point = Literal('.')

l_paren = Literal('(')
r_paren = Literal(')')

l_bracket = Literal('[')
r_bracket = Literal(']')

plus_or_minus = Literal('+') | Literal('-')

number = Word(nums)
integer = Combine(Optional(plus_or_minus) + number)
float_number = Combine(
    integer + Optional(point + number)
).setParseAction(to_float)

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
).setResultsName('time').setParseAction(to_time)

# Example: "[8:33:05 PM] "
event_time = Combine(LineStart() + '[' + time + ']' + space)

# Example: "Sep 15, 2013"
date = Combine(
    Word(alphas, exact=3)       # Month abbreviation (e.g. Jan, Feb, Sep, etc.)
    + space                     #
    + Word(nums, min=1, max=2)  # Day number (e.g. 8, 08 or 18)
    + comma                     #
    + space                     #
    + Word(nums, exact=4)       # Year
).setResultsName('date').setParseAction(to_date)

# Example: "Sep 15, 2013 8:33:05 PM"
date_time = Combine(date + space + time)

# Example: "[Sep 15, 2013 8:33:05 PM] "
event_date_time = Combine(
    LineStart()
    + l_bracket
    + date_time
    + r_bracket
    + space
)

# Example: " at 100.0 200.99"
event_pos = Combine(
    space
    + Suppress('at')
    + space
    + float_number.setResultsName('x')
    + space
    + float_number.setResultsName('y')
    + LineEnd()
).setResultsName('pos').setParseAction(to_pos)

# Example: "on" or "off"
toggle_value = Or([
    Literal(x) for x in TOGGLE_VALUES.values()
]).setResultsName('toggle_value').setParseAction(to_toggle_value)

# Example: "=XXX=User0"
callsign = Word(
    alphanums + "!#%$&)(+*-/.=<>@[]_^{}|~"
).setResultsName('callsign')

# Example: "Pe-8"
aircraft = Word(
    alphanums + "_-"
).setResultsName('aircraft')

# Example: "=XXX=User0:Pe-8"
pilot = (
    callsign + colon.suppress() + aircraft
).setResultsName('pilot')

enemy = pilot.setResultsName('enemy')

# Example: "(0)"
seat_number = (
    l_paren.suppress() + number + r_paren.suppress()
).setParseAction(to_int).setResultsName('seat_number')

# Example: "User:Pe-8(0)"
crew_member = WordStart() + pilot + seat_number + WordEnd()

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
]).setResultsName('belligerent').setParseAction(to_belligerent)

# Example: " destroyed by User:Pe-8 at 100.0 200.99"
destroyed_by = Combine(
    space
    + Literal('destroyed')
    + space
    + Literal('by')
    + space
    + pilot
    + event_pos
)


#------------------------------------------------------------------------------
# Events
#------------------------------------------------------------------------------

def Event(expr, structure):
    to_structure = lambda tokens: structure(tokens.event)
    return Combine(expr).setResultsName('event').setParseAction(to_structure)

mission = Literal('Mission')

# Example: "[Sep 15, 2013 8:33:05 PM] Mission: PH.mis is Playing"
mission_playing = Event(
    event_date_time
    + mission
    + colon
    + space
    + Regex(r".+\.mis").setResultsName('mission')
    + space
    + Literal('is')
    + space
    + Literal('Playing')
    + LineEnd(),
    structure=MissionIsPlaying
)

# Example: "[8:33:05 PM] Mission BEGIN"
mission_begin = Event(
    event_time
    + mission
    + space
    + Literal('BEGIN')
    + LineEnd(),
    structure=MissionBegin
)

# Example: "[8:33:05 PM] Mission END"
mission_end = Event(
    event_time
    + mission
    + space
    + Literal('END')
    + LineEnd(),
    structure=MissionEnd
)
