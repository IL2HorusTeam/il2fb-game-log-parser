# -*- coding: utf-8 -*-

from il2fb.commons.organization import Belligerents
from pyparsing import (
    Combine, LineStart, LineEnd, Literal, CaselessLiteral, Or, Word, WordStart,
    WordEnd, alphanums, Suppress,
)

from ..constants import ToggleValues, TargetEndStates
from .converters import (
    to_int, to_pos, to_toggle_value, to_belligerent, to_target_end_state,
    to_human_aircraft, to_human_crew_member,
)
from .primitives import (
    space, colon, l_bracket, r_bracket, l_paren, r_paren, number, float_number,
    time, date_time,
)


# Example: "[8:33:05 PM] "
event_time = Combine(LineStart() + l_bracket + time + r_bracket + space)

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
    + Suppress("at")
    + space
    + float_number.setResultsName("x")
    + space
    + float_number.setResultsName("y")
    + LineEnd()
).setResultsName("pos").setParseAction(to_pos)

# Example: "on" or "off"
toggle_value = Or([
    Literal(x) for x in ToggleValues.names()
]).setResultsName("toggle_value").setParseAction(to_toggle_value)

# Example: "=XXX=User0"
callsign = Word(
    alphanums + "!#%$&)(+*-/.=<>@[]_^{}|~"
).setResultsName("callsign")

# Example: "Pe-8"
aircraft = Word(
    alphanums + "_-"
).setResultsName("aircraft")

# Example: "=XXX=User0:Pe-8"
pilot = (
    callsign + colon.suppress() + aircraft
).setResultsName("pilot")

human_aggressor = pilot.setResultsName("aggressor")

# Example: "(0)"
seat_number = (
    l_paren.suppress() + number + r_paren.suppress()
).setResultsName("seat_number").setParseAction(to_int)

# Example: "User:Pe-8(0)"
crew_member = (
    WordStart() + pilot + seat_number + WordEnd()
).setResultsName("crew_member").setParseAction(to_human_crew_member)

# Example: "0_Static"
static = Combine(
    number + Literal("_Static")
).setResultsName("static")

# Example: "Bridge0"
bridge = Combine(
    Literal("Bridge") + number
).setResultsName("bridge")

# Example: "Red" or "Blue"
belligerent = Or([
    CaselessLiteral(x.title()) for x in Belligerents.names()
]).setResultsName("belligerent").setParseAction(to_belligerent)

# Example: " destroyed by User:Pe-8 at 100.0 200.99"
destroyed_by = Combine(
    space
    + Literal("destroyed")
    + space
    + Literal("by")
    + space
    + pilot
    + event_pos
)

# Example: "Complete" or "Failed"
target_end_state = Or([
    Literal(x) for x in TargetEndStates.values()
]).setResultsName("target_end_state").setParseAction(to_target_end_state)
