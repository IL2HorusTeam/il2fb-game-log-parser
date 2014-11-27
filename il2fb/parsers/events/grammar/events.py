# -*- coding: utf-8 -*-

from pyparsing import Combine, LineEnd, Literal, Regex

from .converters import to_int
from .helpers import (
    event_time, event_date_time, belligerent, target_end_state, callsign,
)
from .primitives import colon, space, number
from ..structures.events import (
    MissionIsPlaying, MissionHasBegun, MissionHasEnded, MissionWasWon,
    TargetStateHasChanged, UserHasConnected,
)


class Event(Combine):

    def toStructure(self, structure):
        to_structure = lambda tokens: structure(**tokens.event)
        return self.setResultsName('event').setParseAction(to_structure)


mission = Literal('Mission')

# Example: "[Sep 15, 2013 8:33:05 PM] Mission: PH.mis is Playing"
mission_is_playing = Event(
    event_date_time
    + mission
    + colon
    + space
    + Regex(r".+\.mis").setResultsName('mission')
    + space
    + Literal('is')
    + space
    + Literal('Playing')
    + LineEnd()
).toStructure(MissionIsPlaying)

# Example: "[8:33:05 PM] Mission BEGIN"
mission_has_begun = Event(
    event_time
    + mission
    + space
    + Literal('BEGIN')
    + LineEnd()
).toStructure(MissionHasBegun)

# Example: "[8:33:05 PM] Mission END"
mission_has_ended = Event(
    event_time
    + mission
    + space
    + Literal('END')
    + LineEnd(),
).toStructure(MissionHasEnded)

# Example: "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"
mission_was_won = Event(
    event_date_time
    + mission
    + colon
    + space
    + belligerent
    + space
    + Literal('WON')
    + LineEnd(),
).toStructure(MissionWasWon)

# Example: "[8:33:05 PM] Target 3 Complete"
target_state_has_changed = Event(
    event_time
    + Literal('Target')
    + space
    + number.setParseAction(to_int).setResultsName('target_index')
    + space
    + target_end_state
    + LineEnd(),
).toStructure(TargetStateHasChanged)

# Example: "[8:45:57 PM] User0 has connected"
user_has_connected = Event(
    event_time
    + callsign
    + space
    + Literal('has')
    + space
    + Literal('connected')
    + LineEnd()
).toStructure(UserHasConnected)
