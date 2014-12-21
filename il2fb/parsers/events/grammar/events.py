# -*- coding: utf-8 -*-

from pyparsing import Combine, LineEnd, Literal, Regex, QuotedString, Or

from ..structures.events import *
from .converters import to_int
from .helpers import (
    event_time, event_date_time, event_pos, belligerent, target_end_state,
    toggle_value, callsign, human_actor, human_victim, human_aggressor,
    human_crew_member, human_crew_member_victim, static_aggressor,
    static_victim, destroyed_by_human, building_victim, tree, bridge_victim,
)
from .primitives import colon, space, number


class Event(Combine):

    def toStructure(self, structure):
        to_structure = lambda tokens: structure(**tokens.event)
        return self.setResultsName("event").setParseAction(to_structure)


mission = Literal("Mission")

mission_is_playing = Event(
    event_date_time
    + mission
    + colon
    + space
    + Regex(r".+\.mis").setResultsName("mission")
    + " is Playing"
    + LineEnd()
).toStructure(MissionIsPlaying)

mission_has_begun = Event(
    event_time
    + mission
    + space
    + Literal("BEGIN")
    + LineEnd()
).toStructure(MissionHasBegun)

mission_has_ended = Event(
    event_time
    + mission
    + space
    + Literal("END")
    + LineEnd(),
).toStructure(MissionHasEnded)

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

target_state_has_changed = Event(
    event_time
    + Literal("Target")
    + space
    + number.setParseAction(to_int).setResultsName("target_index")
    + space
    + target_end_state
    + LineEnd(),
).toStructure(TargetStateHasChanged)

human_has_connected = Event(
    event_time
    + callsign
    + " has connected"
    + LineEnd()
).toStructure(HumanHasConnected)

human_has_disconnected = Event(
    event_time
    + callsign
    + " has disconnected"
    + LineEnd()
).toStructure(HumanHasDisconnected)

human_has_went_to_briefing = Event(
    event_time
    + callsign
    + " entered refly menu"
    + LineEnd()
).toStructure(HumanHasWentToBriefing)

human_has_selected_airfield = Event(
    event_time
    + callsign
    + " selected army "
    + belligerent
    + event_pos
).toStructure(HumanHasSelectedAirfield)

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

human_has_took_off = Event(
    event_time
    + human_actor
    + " in flight"
    + event_pos
).toStructure(HumanHasTookOff)

human_has_landed = Event(
    event_time
    + human_actor
    + " landed"
    + event_pos
).toStructure(HumanHasLanded)

human_has_crashed = Event(
    event_time
    + human_actor
    + " crashed"
    + event_pos
).toStructure(HumanHasCrashed)

human_was_damaged_on_ground = Event(
    event_time
    + human_actor
    + " damaged on the ground"
    + event_pos
).toStructure(HumanWasDamagedOnGround)

human_has_damaged_himself = Event(
    event_time
    + human_actor
    + " damaged by "
    + Or(["landscape", "NONAME"])
    + event_pos
).toStructure(HumanHasDamagedHimself)

human_was_damaged_by_human = Event(
    event_time
    + human_victim
    + " damaged by "
    + human_aggressor
    + event_pos
).toStructure(HumanWasDamagedByHuman)

human_was_damaged_by_static = Event(
    event_time
    + human_victim
    + " damaged by "
    + static_aggressor
    + event_pos
).toStructure(HumanWasDamagedByStatic)

human_has_committed_suicide = Event(
    event_time
    + human_actor
    + " shot down by landscape"
    + event_pos
).toStructure(HumanHasCommittedSuicide)

human_was_shot_down_by_human = Event(
    event_time
    + human_victim
    + " shot down by "
    + human_aggressor
    + event_pos
).toStructure(HumanWasShotDownByHuman)

human_was_shot_down_by_static = Event(
    event_time
    + human_victim
    + " shot down by "
    + static_aggressor
    + event_pos
).toStructure(HumanWasShotDownByStatic)

human_has_toggled_landing_lights = Event(
    event_time
    + human_actor
    + " turned landing lights "
    + toggle_value
    + event_pos
).toStructure(HumanHasToggledLandingLights)

human_has_toggled_wingtip_smokes = Event(
    event_time
    + human_actor
    + " turned wingtip smokes "
    + toggle_value
    + event_pos
).toStructure(HumanHasToggledWingtipSmokes)

human_has_changed_seat = Event(
    event_time
    + human_crew_member
    + " seat occupied by "
    + callsign.suppress()
    + event_pos
).toStructure(HumanHasChangedSeat)

human_crew_member_has_bailed_out = Event(
    event_time
    + human_crew_member
    + " bailed out"
    + event_pos
).toStructure(HumanCrewMemberHasBailedOut)

human_crew_member_has_opened_parachute = Event(
    event_time
    + human_crew_member
    + " successfully bailed out"
    + event_pos
).toStructure(HumanCrewMemberHasOpenedParachute)

human_crew_member_was_captured = Event(
    event_time
    + human_crew_member
    + " was captured"
    + event_pos
).toStructure(HumanCrewMemberWasCaptured)

human_crew_member_was_wounded = Event(
    event_time
    + human_crew_member
    + " was wounded"
    + event_pos
).toStructure(HumanCrewMemberWasWounded)

human_crew_member_was_heavily_wounded = Event(
    event_time
    + human_crew_member
    + " was heavily wounded"
    + event_pos
).toStructure(HumanCrewMemberWasHeavilyWounded)

human_crew_member_was_killed = Event(
    event_time
    + human_crew_member
    + " was killed"
    + event_pos
).toStructure(HumanCrewMemberWasKilled)

human_crew_member_was_killed_by_human = Event(
    event_time
    + human_crew_member_victim
    + " was killed by "
    + human_aggressor
    + event_pos
).toStructure(HumanCrewMemberWasKilledByHuman)

building_was_destroyed_by_human = Event(
    event_time
    + building_victim
    + destroyed_by_human
).toStructure(BuildingWasDestroyedByHuman)

tree_was_destroyed_by_human = Event(
    event_time
    + tree
    + destroyed_by_human
).toStructure(TreeWasDestroyedByHuman)

static_was_destroyed_by_human = Event(
    event_time
    + static_victim
    + destroyed_by_human
).toStructure(StaticWasDestroyedByHuman)

bridge_was_destroyed_by_human = Event(
    event_time
    + space
    + bridge_victim
    + destroyed_by_human
).toStructure(BridgeWasDestroyedByHuman)

event = (
    mission_is_playing
    | mission_has_begun
    | mission_has_ended
    | mission_was_won
    | mission_was_won
    | target_state_has_changed
    | human_has_connected
    | human_has_disconnected
    | human_has_went_to_briefing
    | human_has_selected_airfield
    | human_has_spawned
    | human_has_took_off
    | human_has_landed
    | human_has_crashed
    | human_was_damaged_on_ground
    | human_has_damaged_himself
    | human_was_damaged_by_human
    | human_was_damaged_by_static
    | human_has_committed_suicide
    | human_was_shot_down_by_human
    | human_was_shot_down_by_static
    | human_has_toggled_landing_lights
    | human_has_toggled_wingtip_smokes
    | human_has_changed_seat
    | human_crew_member_has_bailed_out
    | human_crew_member_has_opened_parachute
    | human_crew_member_was_captured
    | human_crew_member_was_wounded
    | human_crew_member_was_heavily_wounded
    | human_crew_member_was_killed
    | human_crew_member_was_killed_by_human
    | building_was_destroyed_by_human
    | tree_was_destroyed_by_human
    | static_was_destroyed_by_human
    | bridge_was_destroyed_by_human
)
