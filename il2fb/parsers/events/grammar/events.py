# -*- coding: utf-8 -*-

from pyparsing import Combine, LineEnd, Literal, Regex, QuotedString

from .converters import to_int
from .helpers import (
    event_time, event_date_time, event_pos, belligerent, target_end_state,
    toggle_value, callsign, human_actor, human_aggressor, human_crew_member,
    human_crew_member_victim,
)
from .primitives import colon, space, number
from ..structures.events import (
    MissionIsPlaying, MissionHasBegun, MissionHasEnded, MissionWasWon,
    TargetStateHasChanged, HumanHasConnected, HumanHasDisconnected,
    HumanHasWentToBriefing, HumanHasSelectedAirfield, HumanHasTookOff,
    HumanHasSpawned, HumanHasToggledLandingLights,
    HumanHasToggledWingtipSmokes, HumanHasChangedSeat,
    HumanCrewMemberHasBailedOut, HumanCrewMemberHasOpenedParachute,
    HumanCrewMemberWasCaptured, HumanCrewMemberWasWounded,
    HumanCrewMemberWasHeavilyWounded, HumanCrewMemberWasKilled,
    HumanCrewMemberWasKilledByHuman,
)


class Event(Combine):

    def toStructure(self, structure):
        to_structure = lambda tokens: structure(**tokens.event)
        return self.setResultsName("event").setParseAction(to_structure)


mission = Literal("Mission")

# Example: "[Sep 15, 2013 8:33:05 PM] Mission: PH.mis is Playing"
mission_is_playing = Event(
    event_date_time
    + mission
    + colon
    + space
    + Regex(r".+\.mis").setResultsName("mission")
    + " is Playing"
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
human_has_connected = Event(
    event_time
    + callsign
    + " has connected"
    + LineEnd()
).toStructure(HumanHasConnected)

# Example: "[8:33:05 PM] User0 has disconnected"
human_has_disconnected = Event(
    event_time
    + callsign
    + " has disconnected"
    + LineEnd()
).toStructure(HumanHasDisconnected)

# Example: "[8:33:05 PM] User0 entered refly menu"
human_has_went_to_briefing = Event(
    event_time
    + callsign
    + " entered refly menu"
    + LineEnd()
).toStructure(HumanHasWentToBriefing)

# Example: "[8:33:05 PM] User0 selected army Red at 100.0 200.99"
human_has_selected_airfield = Event(
    event_time
    + callsign
    + " selected army "
    + belligerent
    + event_pos
).toStructure(HumanHasSelectedAirfield)

# Example: "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"
human_has_spawned = Event(
    event_time
    + human_actor
    + " loaded weapons "
    + QuotedString(quoteChar="'").setResultsName("weapons")
    + " fuel "
    + number.setParseAction(to_int).setResultsName("fuel")
    + "%"
    + LineEnd()
).toStructure(HumanHasSpawned)

# Example: "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"
human_has_took_off = Event(
    event_time
    + human_actor
    + " in flight"
    + event_pos
).toStructure(HumanHasTookOff)

# Example: "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"
human_has_toggled_landing_lights = Event(
    event_time
    + human_actor
    + " turned landing lights "
    + toggle_value
    + event_pos
).toStructure(HumanHasToggledLandingLights)

# Example: "[8:33:05 PM] User0:Pe-8 turned wingtip smokes off at 100.0 200.99"
human_has_toggled_wingtip_smokes = Event(
    event_time
    + human_actor
    + " turned wingtip smokes "
    + toggle_value
    + event_pos
).toStructure(HumanHasToggledWingtipSmokes)

# Example: "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"
human_has_changed_seat = Event(
    event_time
    + human_crew_member
    + " seat occupied by "
    + callsign.suppress()
    + event_pos
).toStructure(HumanHasChangedSeat)

# Example: "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"
human_crew_member_has_bailed_out = Event(
    event_time
    + human_crew_member
    + " bailed out"
    + event_pos
).toStructure(HumanCrewMemberHasBailedOut)

# Example: "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"
human_crew_member_has_opened_parachute = Event(
    event_time
    + human_crew_member
    + " successfully bailed out"
    + event_pos
).toStructure(HumanCrewMemberHasOpenedParachute)

# Example: "[8:33:05 PM] User0:Pe-8(0) was captured at 100.0 200.99"
human_crew_member_was_captured = Event(
    event_time
    + human_crew_member
    + " was captured"
    + event_pos
).toStructure(HumanCrewMemberWasCaptured)

# Example: "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"
human_crew_member_was_wounded = Event(
    event_time
    + human_crew_member
    + " was wounded"
    + event_pos
).toStructure(HumanCrewMemberWasWounded)

# Example: "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"
human_crew_member_was_heavily_wounded = Event(
    event_time
    + human_crew_member
    + " was heavily wounded"
    + event_pos
).toStructure(HumanCrewMemberWasHeavilyWounded)

# Example: "[8:33:05 PM] User0:Pe-8(0) was killed at 100.0 200.99"
human_crew_member_was_killed = Event(
    event_time
    + human_crew_member
    + " was killed"
    + event_pos
).toStructure(HumanCrewMemberWasKilled)

# Example: "[8:33:05 PM] User0:Pe-8(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"
human_crew_member_was_killed_by_human = Event(
    event_time
    + human_crew_member_victim
    + " was killed by "
    + human_aggressor
    + event_pos
).toStructure(HumanCrewMemberWasKilledByHuman)
