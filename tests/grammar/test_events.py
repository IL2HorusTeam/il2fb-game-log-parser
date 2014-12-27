# -*- coding: utf-8 -*-

import datetime

from il2fb.commons.organization import Belligerents

from il2fb.parsers.events.constants import TargetEndStates
from il2fb.parsers.events.grammar.events import (
    ai_aircraft_has_despawned, ai_aircraft_was_damaged_on_ground,
    bridge_was_destroyed_by_human_aircraft,
    building_was_destroyed_by_human_aircraft,
    human_aircraft_was_damaged_by_human_aircraft,
    human_aircraft_was_damaged_by_static,
    human_aircraft_was_damaged_on_ground,
    human_aircraft_was_shot_down_by_human_aircraft,
    human_aircraft_was_shot_down_by_static, human_crew_member_has_bailed_out,
    human_crew_member_has_touched_down, human_crew_member_was_captured,
    human_crew_member_was_heavily_wounded, human_crew_member_was_killed,
    human_crew_member_was_killed_by_human_aircraft,
    human_crew_member_was_wounded, human_has_changed_seat,
    human_has_destroyed_his_aircraft, human_has_connected,
    human_aircraft_has_crashed, human_has_damaged_his_aircraft,
    human_has_disconnected, human_aircraft_has_landed,
    human_has_selected_airfield, human_aircraft_has_spawned,
    human_has_toggled_landing_lights, human_has_toggled_wingtip_smokes,
    human_aircraft_has_took_off, human_has_went_to_briefing, mission_has_begun,
    mission_has_ended, mission_is_playing, mission_was_won,
    static_was_destroyed, static_was_destroyed_by_human_aircraft,
    target_state_has_changed, tree_was_destroyed_by_human_aircraft,
)
from il2fb.parsers.events.structures import (
    Point2D, HumanAircraft, HumanCrewMember,
)
from il2fb.parsers.events.structures import events

from ..base import BaseTestCase


class EventsGrammarTestCase(BaseTestCase):

    @staticmethod
    def string_to_event(string, grammar):
        return grammar.parseString(string).event

    def test_mission_is_playing(self):
        string = "[Sep 15, 2013 8:33:05 PM] Mission: path/PH.mis is Playing"
        event = self.string_to_event(string, mission_is_playing)

        self.assertIsInstance(event, events.MissionIsPlaying)
        self.assertEqual(event.date, datetime.date(2013, 9, 15))
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.mission, "path/PH.mis")

    def test_mission_has_begun(self):
        string = "[8:33:05 PM] Mission BEGIN"
        event = self.string_to_event(string, mission_has_begun)

        self.assertIsInstance(event, events.MissionHasBegun)
        self.assertEqual(event.time, datetime.time(20, 33, 5))

    def test_mission_has_ended(self):
        string = "[8:33:05 PM] Mission END"
        event = self.string_to_event(string, mission_has_ended)

        self.assertIsInstance(event, events.MissionHasEnded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))

    def test_mission_was_won(self):
        string = "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"
        event = self.string_to_event(string, mission_was_won)

        self.assertIsInstance(event, events.MissionWasWon)
        self.assertEqual(event.date, datetime.date(2013, 9, 15))
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.belligerent, Belligerents.red)

    def test_target_state_has_changed(self):
        testee = target_state_has_changed

        string = "[8:33:05 PM] Target 3 Complete"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, events.TargetStateWasChanged)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.target_index, 3)
        self.assertEqual(event.state, TargetEndStates.COMPLETE)

        string = "[8:33:05 PM] Target 4 Failed"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, events.TargetStateWasChanged)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.target_index, 4)
        self.assertEqual(event.state, TargetEndStates.FAILED)

    def test_human_has_connected(self):
        string = "[8:33:05 PM] User0 has connected"
        event = self.string_to_event(string, human_has_connected)

        self.assertIsInstance(event, events.HumanHasConnected)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")

    def test_human_has_disconnected(self):
        string = "[8:33:05 PM] User0 has disconnected"
        event = self.string_to_event(string, human_has_disconnected)

        self.assertIsInstance(event, events.HumanHasDisconnected)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")

    def test_human_has_selected_airfield(self):
        string = "[8:33:05 PM] User0 selected army Red at 100.0 200.99"
        event = self.string_to_event(string, human_has_selected_airfield)

        self.assertIsInstance(event, events.HumanHasSelectedAirfield)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.belligerent, Belligerents.red)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_has_went_to_briefing(self):
        string = "[8:33:05 PM] User0 entered refly menu"
        event = self.string_to_event(string, human_has_went_to_briefing)

        self.assertIsInstance(event, events.HumanHasWentToBriefing)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")

    def test_human_has_toggled_landing_lights(self):
        testee = human_has_toggled_landing_lights

        string = "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, events.HumanHasToggledLandingLights)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.value, False)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

        string = "[8:33:05 PM] User0:Pe-8 turned landing lights on at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertEqual(event.value, True)

    def test_human_has_toggled_wingtip_smokes(self):
        testee = human_has_toggled_wingtip_smokes

        string = "[8:33:05 PM] User0:Pe-8 turned wingtip smokes off at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, events.HumanHasToggledWingtipSmokes)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.value, False)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

        string = "[8:33:05 PM] User0:Pe-8 turned wingtip smokes on at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertEqual(event.value, True)

    def test_human_has_changed_seat(self):
        string = "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"
        event = self.string_to_event(string, human_has_changed_seat)

        self.assertIsInstance(event, events.HumanHasChangedSeat)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_has_damaged_his_aircraft(self):

        def _assert(string):
            event = self.string_to_event(
                string, human_has_damaged_his_aircraft
            )
            self.assertIsInstance(event, events.HumanHasDamagedHisAircraft)
            self.assertEqual(event.time, datetime.time(20, 33, 5))
            self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
            self.assertEqual(event.pos, Point2D(100.0, 200.99))

        _assert("[8:33:05 PM] User0:Pe-8 damaged by landscape at 100.0 200.99")
        _assert("[8:33:05 PM] User0:Pe-8 damaged by NONAME at 100.0 200.99")

    def test_human_has_destroyed_his_aircraft(self):
        string = "[8:33:05 PM] User0:Pe-8 shot down by landscape at 100.0 200.99"
        event = self.string_to_event(string, human_has_destroyed_his_aircraft)

        self.assertIsInstance(event, events.HumanHasDestroyedHisAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_aircraft_has_spawned(self):
        string = "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"
        event = self.string_to_event(string, human_aircraft_has_spawned)

        self.assertIsInstance(event, events.HumanAircraftHasSpawned)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.weapons, "40fab100")
        self.assertEqual(event.fuel, 40)

    def test_human_aircraft_has_took_off(self):
        string = "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"
        event = self.string_to_event(string, human_aircraft_has_took_off)

        self.assertIsInstance(event, events.HumanAircraftHasTookOff)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_aircraft_has_landed(self):
        string = "[8:33:05 PM] User0:Pe-8 landed at 100.0 200.99"
        event = self.string_to_event(string, human_aircraft_has_landed)

        self.assertIsInstance(event, events.HumanAircraftHasLanded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_aircraft_has_crashed(self):
        string = "[8:33:05 PM] User0:Pe-8 crashed at 100.0 200.99"
        event = self.string_to_event(string, human_aircraft_has_crashed)

        self.assertIsInstance(event, events.HumanAircraftHasCrashed)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_aircraft_was_damaged_on_ground(self):
        string = "[8:33:05 PM] User0:Pe-8 damaged on the ground at 100.0 200.99"
        event = self.string_to_event(
            string, human_aircraft_was_damaged_on_ground
        )

        self.assertIsInstance(event, events.HumanAircraftWasDamagedOnGround)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_aircraft_was_damaged_by_human_aircraft(self):
        string = "[8:33:05 PM] User0:Pe-8 damaged by User1:Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string, human_aircraft_was_damaged_by_human_aircraft
        )

        self.assertIsInstance(
            event, events.HumanAircraftWasDamagedByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.aggressor, HumanAircraft("User1", "Bf-109G-6_Late"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_aircraft_was_damaged_by_static(self):
        string = "[8:33:05 PM] User0:Pe-8 damaged by 0_Static at 100.0 200.99"
        event = self.string_to_event(
            string, human_aircraft_was_damaged_by_static
        )

        self.assertIsInstance(event, events.HumanAircraftWasDamagedByStatic)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.aggressor, "0_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_aircraft_was_shot_down_by_human_aircraft(self):
        string = "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string, human_aircraft_was_shot_down_by_human_aircraft
        )

        self.assertIsInstance(
            event, events.HumanAircraftWasShotDownByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.victim, HumanAircraft("User0", "Pe-8")
        )
        self.assertEqual(
            event.aggressor, HumanAircraft("User1", "Bf-109G-6_Late")
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_aircraft_was_shot_down_by_static(self):
        string = "[8:33:05 PM] User0:Pe-8 shot down by 0_Static at 100.0 200.99"
        event = self.string_to_event(
            string, human_aircraft_was_shot_down_by_static
        )

        self.assertIsInstance(event, events.HumanAircraftWasShotDownByStatic)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.aggressor, "0_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_crew_member_has_bailed_out(self):
        string = "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"
        event = self.string_to_event(string, human_crew_member_has_bailed_out)

        self.assertIsInstance(event, events.HumanCrewMemberHasBailedOut)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_crew_member_has_touched_down(self):
        string = "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"
        event = self.string_to_event(
            string, human_crew_member_has_touched_down
        )

        self.assertIsInstance(event, events.HumanCrewMemberHasTouchedDown)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_crew_member_was_captured(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was captured at 100.0 200.99"
        event = self.string_to_event(string, human_crew_member_was_captured)

        self.assertIsInstance(event, events.HumanCrewMemberWasCaptured)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_crew_member_was_wounded(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"
        event = self.string_to_event(string, human_crew_member_was_wounded)

        self.assertIsInstance(event, events.HumanCrewMemberWasWounded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_crew_member_was_heavily_wounded(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"
        event = self.string_to_event(
            string, human_crew_member_was_heavily_wounded
        )

        self.assertIsInstance(event, events.HumanCrewMemberWasHeavilyWounded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_crew_member_was_killed(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was killed at 100.0 200.99"
        event = self.string_to_event(string, human_crew_member_was_killed)

        self.assertIsInstance(event, events.HumanCrewMemberWasKilled)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_human_crew_member_was_killed_by_human_aircraft(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string, human_crew_member_was_killed_by_human_aircraft
        )

        self.assertIsInstance(
            event, events.HumanCrewMemberWasKilledByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.aggressor, HumanAircraft("User1", "Bf-109G-6_Late"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_building_was_destroyed_by_human_aircraft(self):
        string = "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
        event = self.string_to_event(
            string, building_was_destroyed_by_human_aircraft
        )

        self.assertIsInstance(
            event, events.BuildingWasDestroyedByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Finland/CenterHouse1_w")
        self.assertEqual(event.aggressor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

        string = "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/live.sim destroyed by User1:Pe-8 at 300.0 400.99"
        event = self.string_to_event(
            string, building_was_destroyed_by_human_aircraft
        )

        self.assertIsInstance(
            event, events.BuildingWasDestroyedByHumanAircraft
        )
        self.assertEqual(event.victim, "Russia/Piter/House3_W")

    def test_tree_was_destroyed_by_human_aircraft(self):
        string = "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
        event = self.string_to_event(
            string, tree_was_destroyed_by_human_aircraft
        )

        self.assertIsInstance(event, events.TreeWasDestroyedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.aggressor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_static_was_destroyed(self):
        string = "[8:33:05 PM] 0_Static crashed at 100.0 200.99"
        event = self.string_to_event(string, static_was_destroyed)

        self.assertIsInstance(event, events.StaticWasDestroyed)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "0_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_static_was_destroyed_by_human_aircraft(self):
        string = "[8:33:05 PM] 0_Static destroyed by User0:Pe-8 at 100.0 200.99"
        event = self.string_to_event(
            string, static_was_destroyed_by_human_aircraft
        )

        self.assertIsInstance(event, events.StaticWasDestroyedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "0_Static")
        self.assertEqual(event.aggressor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_bridge_was_destroyed_by_human_aircraft(self):
        string = "[8:33:05 PM]  Bridge0 destroyed by User0:Pe-8 at 100.0 200.99"
        event = self.string_to_event(
            string, bridge_was_destroyed_by_human_aircraft
        )

        self.assertIsInstance(event, events.BridgeWasDestroyedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Bridge0")
        self.assertEqual(event.aggressor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_ai_aircraft_has_despawned(self):
        string = "[8:33:05 PM] Pe-8 removed at 100.0 200.99"
        event = self.string_to_event(string, ai_aircraft_has_despawned)

        self.assertIsInstance(event, events.AIAircraftHasDespawned)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.aircraft, "Pe-8")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_ai_aircraft_was_damaged_on_ground(self):
        string = "[8:33:05 PM] Pe-8 damaged on the ground at 100.0 200.99"
        event = self.string_to_event(string, ai_aircraft_was_damaged_on_ground)

        self.assertIsInstance(event, events.AIAircraftWasDamagedOnGround)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.aircraft, "Pe-8")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
