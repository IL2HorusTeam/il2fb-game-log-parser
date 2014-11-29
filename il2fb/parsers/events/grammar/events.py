# -*- coding: utf-8 -*-

from pyparsing import Combine, LineEnd, Literal, Regex, QuotedString

from .converters import to_int
from .helpers import (
    event_time, event_date_time, event_pos, belligerent, target_end_state,
    callsign, pilot, crew_member,
)
from .primitives import colon, space, number
from ..structures.events import (
    MissionIsPlaying, MissionHasBegun, MissionHasEnded, MissionWasWon,
    TargetStateHasChanged, UserHasConnected, UserHasDisconnected,
    UserHasWentToBriefing, UserHasSelectedAirfield, UserHasTookOff,
    UserHasSpawned, UserHasChangedSeat,
)


class Event(Combine):

    def toStructure(self, structure):
        to_structure = lambda tokens: structure(**tokens.event)
        return self.setResultsName("event").setParseAction(to_structure)


mission = Literal("Mission")
has = space + Literal("has") + space

# Example: "[Sep 15, 2013 8:33:05 PM] Mission: PH.mis is Playing"
mission_is_playing = Event(
    event_date_time
    + mission
    + colon
    + space
    + Regex(r".+\.mis").setResultsName("mission")
    + space
    + Literal("is")
    + space
    + Literal("Playing")
    + LineEnd()
).toStructure(MissionIsPlaying)

# Example: "[8:33:05 PM] Mission BEGIN"
mission_has_begun = Event(
    event_time
    + mission
    + space
    + Literal("BEGIN")
    + LineEnd()
).toStructure(MissionHasBegun)

# Example: "[8:33:05 PM] Mission END"
mission_has_ended = Event(
    event_time
    + mission
    + space
    + Literal("END")
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
    + Literal("WON")
    + LineEnd(),
).toStructure(MissionWasWon)

# Example: "[8:33:05 PM] Target 3 Complete"
target_state_has_changed = Event(
    event_time
    + Literal("Target")
    + space
    + number.setParseAction(to_int).setResultsName("target_index")
    + space
    + target_end_state
    + LineEnd(),
).toStructure(TargetStateHasChanged)

# Example: "[8:33:05 PM] User0 has connected"
user_has_connected = Event(
    event_time
    + callsign
    + has
    + Literal("connected")
    + LineEnd()
).toStructure(UserHasConnected)

# Example: "[8:33:05 PM] User0 has disconnected"
user_has_disconnected = Event(
    event_time
    + callsign
    + has
    + Literal("disconnected")
    + LineEnd()
).toStructure(UserHasDisconnected)

# Example: "[8:33:05 PM] User0 entered refly menu"
user_has_went_to_briefing = Event(
    event_time
    + callsign
    + space
    + Literal("entered")
    + space
    + Literal("refly")
    + space
    + Literal("menu")
    + LineEnd()
).toStructure(UserHasWentToBriefing)

# Example: "[8:33:05 PM] User0 selected army Red at 100.0 200.99"
user_has_selected_airfield = Event(
    event_time
    + callsign
    + space
    + Literal("selected")
    + space
    + Literal("army")
    + space
    + belligerent
    + event_pos
).toStructure(UserHasSelectedAirfield)

# Example: "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"
user_has_took_off = Event(
    event_time
    + pilot
    + space
    + Literal("in")
    + space
    + Literal("flight")
    + event_pos
).toStructure(UserHasTookOff)

# Example: "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"
user_has_spawned = Event(
    event_time
    + pilot
    + space
    + Literal("loaded")
    + space
    + Literal("weapons")
    + space
    + QuotedString(quoteChar="'").setResultsName("weapons")
    + space
    + Literal("fuel")
    + space
    + number.setParseAction(to_int).setResultsName("fuel")
    + Literal("%")
    + LineEnd()
).toStructure(UserHasSpawned)

# Example: "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"
user_has_changed_seat = Event(
    event_time
    + crew_member
    + " seat occupied by "
    + callsign.suppress()
    + event_pos
).toStructure(UserHasChangedSeat)
