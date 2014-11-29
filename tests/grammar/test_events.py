# -*- coding: utf-8 -*-

import datetime

from il2fb.commons.organization import Belligerents

from il2fb.parsers.events.constants import TargetEndStates
from il2fb.parsers.events.grammar.events import (
    mission_is_playing, mission_has_begun, mission_has_ended,
    mission_was_won, target_state_has_changed, human_has_connected,
    human_has_disconnected, human_has_went_to_briefing,
    human_has_selected_airfield, human_has_took_off, human_has_spawned,
    human_has_toggled_landing_lights, human_has_toggled_wingtip_smokes,
    human_has_changed_seat, human_crew_member_has_bailed_out,
    human_crew_member_has_opened_parachute, human_crew_member_was_wounded,
    human_crew_member_was_heavily_wounded, human_crew_member_was_killed,
    human_crew_member_was_killed_by_human,
)
from il2fb.parsers.events.structures import (
    Point2D, HumanActor, HumanCrewMember,
)
from il2fb.parsers.events.structures import events

from ..base import BaseTestCase


class EventsGrammarTestCase(BaseTestCase):

    @staticmethod
    def string_to_event(string, grammar):
        return grammar.parseString(string).event

    def assertInAll(self, structure):
        self.assertIn(structure.__name__, events.__all__)

    def test_mission_is_playing(self):
        string = "[Sep 15, 2013 8:33:05 PM] Mission: path/PH.mis is Playing"
        event = self.string_to_event(string, mission_is_playing)

        self.assertIsInstance(event, events.MissionIsPlaying)
        self.assertEqual(event.date, datetime.date(2013, 9, 15))
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.mission, "path/PH.mis")
        self.assertInAll(events.MissionIsPlaying)

    def test_mission_has_begun(self):
        string = "[8:33:05 PM] Mission BEGIN"
        event = self.string_to_event(string, mission_has_begun)

        self.assertIsInstance(event, events.MissionHasBegun)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertInAll(events.MissionHasBegun)

    def test_mission_has_ended(self):
        string = "[8:33:05 PM] Mission END"
        event = self.string_to_event(string, mission_has_ended)

        self.assertIsInstance(event, events.MissionHasEnded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertInAll(events.MissionHasEnded)

    def test_mission_was_won(self):
        string = "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"
        event = self.string_to_event(string, mission_was_won)

        self.assertIsInstance(event, events.MissionWasWon)
        self.assertEqual(event.date, datetime.date(2013, 9, 15))
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.belligerent, Belligerents.red)
        self.assertInAll(events.MissionWasWon)

    def test_target_state_has_changed(self):
        testee = target_state_has_changed

        string = "[8:33:05 PM] Target 3 Complete"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, events.TargetStateHasChanged)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.target_index, 3)
        self.assertEqual(event.state, TargetEndStates.COMPLETE)

        string = "[8:33:05 PM] Target 4 Failed"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, events.TargetStateHasChanged)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.target_index, 4)
        self.assertEqual(event.state, TargetEndStates.FAILED)

        self.assertInAll(events.TargetStateHasChanged)

    def test_human_has_connected(self):
        string = "[8:33:05 PM] User0 has connected"
        event = self.string_to_event(string, human_has_connected)

        self.assertIsInstance(event, events.HumanHasConnected)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertInAll(events.HumanHasConnected)

    def test_human_has_disconnected(self):
        string = "[8:33:05 PM] User0 has disconnected"
        event = self.string_to_event(string, human_has_disconnected)

        self.assertIsInstance(event, events.HumanHasDisconnected)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertInAll(events.HumanHasDisconnected)

    def test_human_has_went_to_briefing(self):
        string = "[8:33:05 PM] User0 entered refly menu"
        event = self.string_to_event(string, human_has_went_to_briefing)

        self.assertIsInstance(event, events.HumanHasWentToBriefing)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertInAll(events.HumanHasWentToBriefing)

    def test_human_has_selected_airfield(self):
        string = "[8:33:05 PM] User0 selected army Red at 100.0 200.99"
        event = self.string_to_event(string, human_has_selected_airfield)

        self.assertIsInstance(event, events.HumanHasSelectedAirfield)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.belligerent, Belligerents.red)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.HumanHasSelectedAirfield)

    def test_human_has_spawned(self):
        string = "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"
        event = self.string_to_event(string, human_has_spawned)

        self.assertIsInstance(event, events.HumanHasSpawned)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanActor("User0", "Pe-8"))
        self.assertEqual(event.weapons, "40fab100")
        self.assertEqual(event.fuel, 40)
        self.assertInAll(events.HumanHasSpawned)

    def test_human_has_took_off(self):
        string = "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"
        event = self.string_to_event(string, human_has_took_off)

        self.assertIsInstance(event, events.HumanHasTookOff)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanActor("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.HumanHasTookOff)

    def test_human_has_toggled_landing_lights(self):
        testee = human_has_toggled_landing_lights

        string = "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, events.HumanHasToggledLandingLights)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanActor("User0", "Pe-8"))
        self.assertEqual(event.value, False)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.HumanHasToggledLandingLights)

        string = "[8:33:05 PM] User0:Pe-8 turned landing lights on at 100.0 200.99"
        event = self.string_to_event(string, testee)
        self.assertEqual(event.value, True)

    def test_human_has_toggled_wingtip_smokes(self):
        testee = human_has_toggled_wingtip_smokes

        string = "[8:33:05 PM] User0:Pe-8 turned wingtip smokes off at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, events.HumanHasToggledWingtipSmokes)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanActor("User0", "Pe-8"))
        self.assertEqual(event.value, False)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.HumanHasToggledWingtipSmokes)

        string = "[8:33:05 PM] User0:Pe-8 turned wingtip smokes on at 100.0 200.99"
        event = self.string_to_event(string, testee)
        self.assertEqual(event.value, True)

    def test_human_has_changed_seat(self):
        string = "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"
        event = self.string_to_event(string, human_has_changed_seat)

        self.assertIsInstance(event, events.HumanHasChangedSeat)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.crew_member, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.HumanHasChangedSeat)

    def test_human_crew_member_has_bailed_out(self):
        string = "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"
        event = self.string_to_event(string, human_crew_member_has_bailed_out)

        self.assertIsInstance(event, events.HumanCrewMemberHasBailedOut)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.crew_member, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.HumanCrewMemberHasBailedOut)

    def test_human_crew_member_has_opened_parachute(self):
        string = "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"
        event = self.string_to_event(string, human_crew_member_has_opened_parachute)

        self.assertIsInstance(event, events.HumanCrewMemberHasOpenedParachute)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.crew_member, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.HumanCrewMemberHasOpenedParachute)

    def test_human_crew_member_was_wounded(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"
        event = self.string_to_event(string, human_crew_member_was_wounded)

        self.assertIsInstance(event, events.HumanCrewMemberWasWounded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.crew_member, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.HumanCrewMemberWasWounded)

    def test_human_crew_member_was_heavily_wounded(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"
        event = self.string_to_event(string, human_crew_member_was_heavily_wounded)

        self.assertIsInstance(event, events.HumanCrewMemberWasHeavilyWounded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.crew_member, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.HumanCrewMemberWasHeavilyWounded)

    def test_human_crew_member_was_killed(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was killed at 100.0 200.99"
        event = self.string_to_event(string, human_crew_member_was_killed)

        self.assertIsInstance(event, events.HumanCrewMemberWasKilled)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.crew_member, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.HumanCrewMemberWasKilled)

    def test_human_crew_member_was_killed_by_human(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(string, human_crew_member_was_killed_by_human)

        self.assertIsInstance(event, events.HumanCrewMemberWasKilledByHuman)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.aggressor, HumanActor("User1", "Bf-109G-6_Late"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.HumanCrewMemberWasKilledByHuman)
