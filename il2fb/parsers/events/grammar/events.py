# -*- coding: utf-8 -*-

from pyparsing import Combine, LineEnd, Regex, QuotedString

from ..structures import events
from .converters import to_int
from .helpers import (
    aircraft, aircraft_victim, belligerent, bridge_victim, building_victim,
    callsign, event_date_time, event_pos, event_time, human_aircraft_actor,
    human_aircraft_aggressor, human_aircraft_victim, human_crew_member,
    human_crew_member_victim, static_aggressor, static_victim,
    target_end_state, toggle_value, tree, by_himself,
)
from .primitives import space, number


class Event(Combine):

    def toStructure(self, structure):
        to_structure = lambda tokens: structure(**tokens.event)
        return self.setResultsName("event").setParseAction(to_structure)


mission_is_playing = Event(
    event_date_time
    + "Mission: "
    + Regex(r".+\.mis").setResultsName("mission")
    + " is Playing"
    + LineEnd()
).toStructure(events.MissionIsPlaying)

mission_has_begun = Event(
    event_time
    + "Mission BEGIN"
    + LineEnd()
).toStructure(events.MissionHasBegun)

mission_has_ended = Event(
    event_time
    + "Mission END"
    + LineEnd(),
).toStructure(events.MissionHasEnded)

mission_was_won = Event(
    event_date_time
    + "Mission: "
    + belligerent
    + " WON"
    + LineEnd(),
).toStructure(events.MissionWasWon)

target_state_has_changed = Event(
    event_time
    + "Target "
    + number.setParseAction(to_int).setResultsName("target_index")
    + space
    + target_end_state
    + LineEnd(),
).toStructure(events.TargetStateWasChanged)

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

human_aircraft_has_spawned = Event(
    event_time
    + human_aircraft_actor
    + " loaded weapons "
    + QuotedString(quoteChar="'").setResultsName("weapons")
    + " fuel "
    + number.setParseAction(to_int).setResultsName("fuel")
    + "%"
    + LineEnd()
).toStructure(events.HumanAircraftHasSpawned)

human_aircraft_has_took_off = Event(
    event_time
    + human_aircraft_actor
    + " in flight"
    + event_pos
).toStructure(events.HumanAircraftHasTookOff)

human_aircraft_has_landed = Event(
    event_time
    + human_aircraft_actor
    + " landed"
    + event_pos
).toStructure(events.HumanAircraftHasLanded)

human_aircraft_has_crashed = Event(
    event_time
    + human_aircraft_victim
    + " crashed"
    + event_pos
).toStructure(events.HumanAircraftHasCrashed)

human_has_damaged_his_aircraft = Event(
    event_time
    + human_aircraft_victim
    + " damaged"
    + by_himself
    + event_pos
).toStructure(events.HumanHasDamagedHisAircraft)

human_has_destroyed_his_aircraft = Event(
    event_time
    + human_aircraft_victim
    + " shot down"
    + by_himself
    + event_pos
).toStructure(events.HumanHasDestroyedHisAircraft)

human_aircraft_was_damaged_on_ground = Event(
    event_time
    + human_aircraft_victim
    + " damaged on the ground"
    + event_pos
).toStructure(events.HumanAircraftWasDamagedOnGround)

human_aircraft_was_damaged_by_human_aircraft = Event(
    event_time
    + human_aircraft_victim
    + " damaged by "
    + human_aircraft_aggressor
    + event_pos
).toStructure(events.HumanAircraftWasDamagedByHumanAircraft)

human_aircraft_was_damaged_by_static = Event(
    event_time
    + human_aircraft_victim
    + " damaged by "
    + static_aggressor
    + event_pos
).toStructure(events.HumanAircraftWasDamagedByStatic)

human_aircraft_was_shot_down_by_human_aircraft = Event(
    event_time
    + human_aircraft_victim
    + " shot down by "
    + human_aircraft_aggressor
    + event_pos
).toStructure(events.HumanAircraftWasShotDownByHumanAircraft)

human_aircraft_was_shot_down_by_static = Event(
    event_time
    + human_aircraft_victim
    + " shot down by "
    + static_aggressor
    + event_pos
).toStructure(events.HumanAircraftWasShotDownByStatic)

human_has_toggled_landing_lights = Event(
    event_time
    + human_aircraft_actor
    + " turned landing lights "
    + toggle_value
    + event_pos
).toStructure(events.HumanHasToggledLandingLights)

human_has_toggled_wingtip_smokes = Event(
    event_time
    + human_aircraft_actor
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

human_crew_member_has_touched_down = Event(
    event_time
    + human_crew_member
    + " successfully bailed out"
    + event_pos
).toStructure(events.HumanCrewMemberHasTouchedDown)

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

human_crew_member_was_killed_by_human_aircraft = Event(
    event_time
    + human_crew_member_victim
    + " was killed by "
    + human_aircraft_aggressor
    + event_pos
).toStructure(events.HumanCrewMemberWasKilledByHumanAircraft)

building_was_destroyed_by_human_aircraft = Event(
    event_time
    + building_victim
    + " destroyed by "
    + human_aircraft_aggressor
    + event_pos
).toStructure(events.BuildingWasDestroyedByHumanAircraft)

tree_was_destroyed_by_human_aircraft = Event(
    event_time
    + tree
    + " destroyed by "
    + human_aircraft_aggressor
    + event_pos
).toStructure(events.TreeWasDestroyedByHumanAircraft)

static_was_destroyed = Event(
    event_time
    + static_victim
    + " crashed"
    + event_pos
).toStructure(events.StaticWasDestroyed)

static_was_destroyed_by_human_aircraft = Event(
    event_time
    + static_victim
    + " destroyed by "
    + human_aircraft_aggressor
    + event_pos
).toStructure(events.StaticWasDestroyedByHumanAircraft)

bridge_was_destroyed_by_human_aircraft = Event(
    event_time
    + space
    + bridge_victim
    + " destroyed by "
    + human_aircraft_aggressor
    + event_pos
).toStructure(events.BridgeWasDestroyedByHumanAircraft)

ai_aircraft_has_despawned = Event(
    event_time
    + aircraft
    + " removed"
    + event_pos
).toStructure(events.AIAircraftHasDespawned)

ai_aircraft_was_damaged_on_ground = Event(
    event_time
    + aircraft_victim
    + " damaged on the ground"
    + event_pos
).toStructure(events.AIAircraftWasDamagedOnGround)

ai_has_damaged_his_aircraft = Event(
    event_time
    + aircraft_victim
    + " damaged"
    + by_himself
    + event_pos
).toStructure(events.AIHasDamagedHisAircraft)

ai_aircraft_has_crashed = Event(
    event_time
    + aircraft_victim
    + " crashed"
    + event_pos
).toStructure(events.AIAircraftHasCrashed)

event = (
    mission_is_playing
    | mission_has_begun
    | mission_has_ended
    | mission_was_won
    | target_state_has_changed

    | human_has_connected
    | human_has_disconnected
    | human_has_selected_airfield
    | human_has_went_to_briefing
    | human_has_changed_seat
    | human_has_toggled_landing_lights
    | human_has_toggled_wingtip_smokes
    | human_has_damaged_his_aircraft
    | human_has_destroyed_his_aircraft

    | human_aircraft_has_crashed
    | human_aircraft_has_landed
    | human_aircraft_has_spawned
    | human_aircraft_has_took_off
    | human_aircraft_was_damaged_by_human_aircraft
    | human_aircraft_was_damaged_by_static
    | human_aircraft_was_damaged_on_ground
    | human_aircraft_was_shot_down_by_human_aircraft
    | human_aircraft_was_shot_down_by_static

    | human_crew_member_has_bailed_out
    | human_crew_member_has_touched_down
    | human_crew_member_was_captured
    | human_crew_member_was_heavily_wounded
    | human_crew_member_was_killed
    | human_crew_member_was_killed_by_human_aircraft
    | human_crew_member_was_wounded

    | static_was_destroyed
    | static_was_destroyed_by_human_aircraft

    | building_was_destroyed_by_human_aircraft
    | bridge_was_destroyed_by_human_aircraft
    | tree_was_destroyed_by_human_aircraft

    | ai_aircraft_has_despawned
    | ai_aircraft_was_damaged_on_ground
    | ai_has_damaged_his_aircraft
    | ai_aircraft_has_crashed
)
