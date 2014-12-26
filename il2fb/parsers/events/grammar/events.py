# -*- coding: utf-8 -*-

from pyparsing import Combine, LineEnd, Literal, Regex, QuotedString, Or

from ..structures import events
from .converters import to_int
from .helpers import (
    event_time, event_date_time, event_pos, belligerent, target_end_state,
    toggle_value, callsign, human_actor, human_victim, human_aggressor,
    human_crew_member, human_crew_member_victim, static_aggressor,
    static_victim, destroyed_by_human, building_victim, tree, bridge_victim,
    aircraft,
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
).toStructure(events.MissionIsPlaying)

mission_has_begun = Event(
    event_time
    + mission
    + space
    + Literal("BEGIN")
    + LineEnd()
).toStructure(events.MissionHasBegun)

mission_has_ended = Event(
    event_time
    + mission
    + space
    + Literal("END")
    + LineEnd(),
).toStructure(events.MissionHasEnded)

mission_was_won = Event(
    event_date_time
    + mission
    + colon
    + space
    + belligerent
    + space
    + Literal("WON")
    + LineEnd(),
).toStructure(events.MissionWasWon)

target_state_has_changed = Event(
    event_time
    + Literal("Target")
    + space
    + number.setParseAction(to_int).setResultsName("target_index")
    + space
    + target_end_state
    + LineEnd(),
).toStructure(events.TargetStateHasChanged)

human_has_connected = Event(
    event_time
    + callsign
    + " has connected"
    + LineEnd()
).toStructure(events.HumanHasConnected)

human_has_disconnected = Event(
    event_time
    + callsign
    + " has disconnected"
    + LineEnd()
).toStructure(events.HumanHasDisconnected)

human_has_went_to_briefing = Event(
    event_time
    + callsign
    + " entered refly menu"
    + LineEnd()
).toStructure(events.HumanHasWentToBriefing)

human_has_selected_airfield = Event(
    event_time
    + callsign
    + " selected army "
    + belligerent
    + event_pos
).toStructure(events.HumanHasSelectedAirfield)

human_has_spawned = Event(
    event_time
    + human_actor
    + " loaded weapons "
    + QuotedString(quoteChar="'").setResultsName("weapons")
    + " fuel "
    + number.setParseAction(to_int).setResultsName("fuel")
    + "%"
    + LineEnd()
).toStructure(events.HumanHasSpawned)

human_has_took_off = Event(
    event_time
    + human_actor
    + " in flight"
    + event_pos
).toStructure(events.HumanHasTookOff)

human_has_landed = Event(
    event_time
    + human_actor
    + " landed"
    + event_pos
).toStructure(events.HumanHasLanded)

human_has_crashed = Event(
    event_time
    + human_victim
    + " crashed"
    + event_pos
).toStructure(events.HumanHasCrashed)

human_was_damaged_on_ground = Event(
    event_time
    + human_victim
    + " damaged on the ground"
    + event_pos
).toStructure(events.HumanWasDamagedOnGround)

human_has_damaged_himself = Event(
    event_time
    + human_victim
    + " damaged by "
    + Or(["landscape", "NONAME"])
    + event_pos
).toStructure(events.HumanHasDamagedHimself)

human_was_damaged_by_human = Event(
    event_time
    + human_victim
    + " damaged by "
    + human_aggressor
    + event_pos
).toStructure(events.HumanWasDamagedByHuman)

human_was_damaged_by_static = Event(
    event_time
    + human_victim
    + " damaged by "
    + static_aggressor
    + event_pos
).toStructure(events.HumanWasDamagedByStatic)

human_has_committed_suicide = Event(
    event_time
    + human_victim
    + " shot down by landscape"
    + event_pos
).toStructure(events.HumanHasCommittedSuicide)

human_was_shot_down_by_human = Event(
    event_time
    + human_victim
    + " shot down by "
    + human_aggressor
    + event_pos
).toStructure(events.HumanWasShotDownByHuman)

human_was_shot_down_by_static = Event(
    event_time
    + human_victim
    + " shot down by "
    + static_aggressor
    + event_pos
).toStructure(events.HumanWasShotDownByStatic)

human_has_toggled_landing_lights = Event(
    event_time
    + human_actor
    + " turned landing lights "
    + toggle_value
    + event_pos
).toStructure(events.HumanHasToggledLandingLights)

human_has_toggled_wingtip_smokes = Event(
    event_time
    + human_actor
    + " turned wingtip smokes "
    + toggle_value
    + event_pos
).toStructure(events.HumanHasToggledWingtipSmokes)

human_has_changed_seat = Event(
    event_time
    + human_crew_member
    + " seat occupied by "
    + callsign.suppress()
    + event_pos
).toStructure(events.HumanHasChangedSeat)

human_crew_member_has_bailed_out = Event(
    event_time
    + human_crew_member
    + " bailed out"
    + event_pos
).toStructure(events.HumanCrewMemberHasBailedOut)

human_crew_member_has_opened_parachute = Event(
    event_time
    + human_crew_member
    + " successfully bailed out"
    + event_pos
).toStructure(events.HumanCrewMemberHasOpenedParachute)

human_crew_member_was_captured = Event(
    event_time
    + human_crew_member_victim
    + " was captured"
    + event_pos
).toStructure(events.HumanCrewMemberWasCaptured)

human_crew_member_was_wounded = Event(
    event_time
    + human_crew_member_victim
    + " was wounded"
    + event_pos
).toStructure(events.HumanCrewMemberWasWounded)

human_crew_member_was_heavily_wounded = Event(
    event_time
    + human_crew_member_victim
    + " was heavily wounded"
    + event_pos
).toStructure(events.HumanCrewMemberWasHeavilyWounded)

human_crew_member_was_killed = Event(
    event_time
    + human_crew_member_victim
    + " was killed"
    + event_pos
).toStructure(events.HumanCrewMemberWasKilled)

human_crew_member_was_killed_by_human = Event(
    event_time
    + human_crew_member_victim
    + " was killed by "
    + human_aggressor
    + event_pos
).toStructure(events.HumanCrewMemberWasKilledByHuman)

building_was_destroyed_by_human = Event(
    event_time
    + building_victim
    + destroyed_by_human
).toStructure(events.BuildingWasDestroyedByHuman)

tree_was_destroyed_by_human = Event(
    event_time
    + tree
    + destroyed_by_human
).toStructure(events.TreeWasDestroyedByHuman)

static_was_destroyed = Event(
    event_time
    + static_victim
    + " crashed"
    + event_pos
).toStructure(events.StaticWasDestroyed)

static_was_destroyed_by_human = Event(
    event_time
    + static_victim
    + destroyed_by_human
).toStructure(events.StaticWasDestroyedByHuman)

bridge_was_destroyed_by_human = Event(
    event_time
    + space
    + bridge_victim
    + destroyed_by_human
).toStructure(events.BridgeWasDestroyedByHuman)

ai_aircraft_has_despawned = Event(
    event_time
    + aircraft
    + " removed"
    + event_pos
).toStructure(events.AIAircraftHasDespawned)

event = (
    mission_is_playing
    | mission_has_begun
    | mission_has_ended
    | mission_was_won
    | target_state_has_changed

    | human_has_changed_seat
    | human_has_committed_suicide
    | human_has_connected
    | human_has_crashed
    | human_has_damaged_himself
    | human_has_disconnected
    | human_has_landed
    | human_has_selected_airfield
    | human_has_spawned
    | human_has_toggled_landing_lights
    | human_has_toggled_wingtip_smokes
    | human_has_took_off
    | human_has_went_to_briefing
    | human_was_damaged_by_human
    | human_was_damaged_by_static
    | human_was_damaged_on_ground
    | human_was_shot_down_by_human
    | human_was_shot_down_by_static

    | human_crew_member_has_bailed_out
    | human_crew_member_has_opened_parachute
    | human_crew_member_was_captured
    | human_crew_member_was_heavily_wounded
    | human_crew_member_was_killed
    | human_crew_member_was_killed_by_human
    | human_crew_member_was_wounded

    | static_was_destroyed
    | static_was_destroyed_by_human

    | building_was_destroyed_by_human
    | bridge_was_destroyed_by_human
    | tree_was_destroyed_by_human

    | ai_aircraft_has_despawned
)
