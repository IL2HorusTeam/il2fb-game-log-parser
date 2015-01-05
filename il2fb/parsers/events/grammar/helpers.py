# -*- coding: utf-8 -*-

from il2fb.commons.organization import Belligerents
from pyparsing import (
    Combine, LineStart, LineEnd, Literal, CaselessLiteral, Or, Word, WordStart,
    WordEnd, alphanums, Suppress, Regex,
)

from ..constants import TOGGLE_VALUES, TARGET_END_STATES
from .converters import (
    to_int, to_pos, to_toggle_value, to_belligerent, to_human_aircraft,
    to_human_aircraft_crew_member, to_ai_aircraft_crew_member,
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
    Literal(x) for x in TOGGLE_VALUES._fields
]).setResultsName("value").setParseAction(to_toggle_value)

# Example: "Complete" or "Failed"
target_end_state = Or([
    Literal(x) for x in TARGET_END_STATES._asdict().values()
]).setResultsName("state")


# Example: "3do/Buildings/Finland/CenterHouse1_w/live.sim"
building = Regex(
    r"3do/Buildings/(?P<building_group>.+)/(live|mono).sim"
).setParseAction(lambda t: t.building_group).setResultsName("building")

building_victim = building.setResultsName("victim")

# Example: "3do/Tree/Line_W/live.sim"
tree = Regex(r"3do/Tree/.+/(live|mono).sim").suppress()

# Example: "0_Static"
static = Combine(
    number + Literal("_Static")
).setResultsName("static")

static_aggressor = static.setResultsName("aggressor")
static_victim = static.setResultsName("victim")

# Example: "Bridge0"
bridge = Combine(
    Literal("Bridge") + number
).setResultsName("bridge")

bridge_victim = bridge.setResultsName("victim")

# Example: "Red" or "Blue"
belligerent = Or([
    CaselessLiteral(x.title()) for x in Belligerents.names()
]).setResultsName("belligerent").setParseAction(to_belligerent)

# Example: "(0)"
seat_number = (
    l_paren.suppress() + number + r_paren.suppress()
).setResultsName("seat_number").setParseAction(to_int)

# Example: "Pe-8"
aircraft = Word(
    alphanums + "_-"
).setResultsName("aircraft")

ai_aircraft_actor = aircraft.setResultsName("actor")
ai_aircraft_aggressor = ai_aircraft_actor.setResultsName("aggressor")
ai_aircraft_victim = ai_aircraft_actor.setResultsName("victim")

# Example: "Pe-8(0)"
ai_aircraft_crew_member = (
    WordStart() + aircraft + seat_number + WordEnd()
).setResultsName("actor").setParseAction(to_ai_aircraft_crew_member)

ai_aircraft_crew_member_victim = (
    ai_aircraft_crew_member
    .setResultsName("victim")
)

# Example: "=XXX=User0"
callsign = Word(
    alphanums + "!#%$&)(+*-/.=<>@[]_^{}|~"
).setResultsName("callsign")

# Example: "=XXX=User0:Pe-8"
human_aircraft = (
    callsign + colon.suppress() + aircraft
)

human_aircraft_actor = (
    human_aircraft
    .setResultsName("actor")
    .setParseAction(to_human_aircraft)
)
human_aircraft_aggressor = human_aircraft_actor.setResultsName("aggressor")
human_aircraft_victim = human_aircraft_actor.setResultsName("victim")

# Example: "User:Pe-8(0)"
human_aircraft_crew_member = (
    WordStart() + human_aircraft + seat_number + WordEnd()
).setResultsName("actor").setParseAction(to_human_aircraft_crew_member)

human_aircraft_crew_member_victim = (
    human_aircraft_crew_member
    .setResultsName("victim")
)

by_himself = space + Literal("by") + space + Or(["landscape", "NONAME"])
