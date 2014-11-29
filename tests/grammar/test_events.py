# -*- coding: utf-8 -*-

import datetime

from il2fb.commons.organization import Belligerents

from il2fb.parsers.events.constants import TargetEndStates
from il2fb.parsers.events.grammar.events import (
    mission_is_playing, mission_has_begun, mission_has_ended,
    mission_was_won, target_state_has_changed, user_has_connected,
    user_has_disconnected, user_has_went_to_briefing,
    user_has_selected_airfield, user_has_took_off, user_has_spawned,
    user_has_changed_seat, crew_member_has_bailed_out,
    crew_member_has_opened_parachute, user_has_toggled_landing_lights,
    user_has_toggled_wingtip_smokes, crew_member_was_wounded,
    crew_member_was_heavily_wounded,
)
from il2fb.parsers.events.structures import Point2D
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
        string = "[8:33:05 PM] Target 3 Complete"
        event = self.string_to_event(string, target_state_has_changed)

        self.assertIsInstance(event, events.TargetStateHasChanged)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.target_index, 3)
        self.assertEqual(event.state, TargetEndStates.COMPLETE)

        string = "[8:33:05 PM] Target 4 Failed"
        event = self.string_to_event(string, target_state_has_changed)

        self.assertIsInstance(event, events.TargetStateHasChanged)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.target_index, 4)
        self.assertEqual(event.state, TargetEndStates.FAILED)

        self.assertInAll(events.TargetStateHasChanged)

    def test_user_has_connected(self):
        string = "[8:33:05 PM] User0 has connected"
        event = self.string_to_event(string, user_has_connected)

        self.assertIsInstance(event, events.UserHasConnected)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertInAll(events.UserHasConnected)

    def test_user_has_disconnected(self):
        string = "[8:33:05 PM] User0 has disconnected"
        event = self.string_to_event(string, user_has_disconnected)

        self.assertIsInstance(event, events.UserHasDisconnected)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertInAll(events.UserHasDisconnected)

    def test_user_has_went_to_briefing(self):
        string = "[8:33:05 PM] User0 entered refly menu"
        event = self.string_to_event(string, user_has_went_to_briefing)

        self.assertIsInstance(event, events.UserHasWentToBriefing)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertInAll(events.UserHasWentToBriefing)

    def test_user_has_selected_airfield(self):
        string = "[8:33:05 PM] User0 selected army Red at 100.0 200.99"
        event = self.string_to_event(string, user_has_selected_airfield)

        self.assertIsInstance(event, events.UserHasSelectedAirfield)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.belligerent, Belligerents.red)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.UserHasSelectedAirfield)

    def test_user_has_took_off(self):
        string = "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"
        event = self.string_to_event(string, user_has_took_off)

        self.assertIsInstance(event, events.UserHasTookOff)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.aircraft, "Pe-8")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.UserHasTookOff)

    def test_user_has_spawned(self):
        string = "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"
        event = self.string_to_event(string, user_has_spawned)

        self.assertIsInstance(event, events.UserHasSpawned)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.aircraft, "Pe-8")
        self.assertEqual(event.weapons, "40fab100")
        self.assertEqual(event.fuel, 40)
        self.assertInAll(events.UserHasSpawned)

    def test_user_has_changed_seat(self):
        string = "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"
        event = self.string_to_event(string, user_has_changed_seat)

        self.assertIsInstance(event, events.UserHasChangedSeat)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.aircraft, "Pe-8")
        self.assertEqual(event.seat_number, 0)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.UserHasChangedSeat)

    def test_crew_member_has_bailed_out(self):
        string = "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"
        event = self.string_to_event(string, crew_member_has_bailed_out)

        self.assertIsInstance(event, events.CrewMemberHasBailedOut)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.aircraft, "Pe-8")
        self.assertEqual(event.seat_number, 0)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.CrewMemberHasBailedOut)

    def test_crew_member_has_opened_parachute(self):
        string = "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"
        event = self.string_to_event(string, crew_member_has_opened_parachute)

        self.assertIsInstance(event, events.CrewMemberHasOpenedParachute)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.aircraft, "Pe-8")
        self.assertEqual(event.seat_number, 0)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.CrewMemberHasOpenedParachute)

    def test_user_has_toggled_landing_lights(self):
        testee = user_has_toggled_landing_lights

        string = "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, events.UserHasToggledLandingLights)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.aircraft, "Pe-8")
        self.assertEqual(event.value, False)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.UserHasToggledLandingLights)

        string = "[8:33:05 PM] User0:Pe-8 turned landing lights on at 100.0 200.99"
        event = self.string_to_event(string, testee)
        self.assertEqual(event.value, True)

    def test_user_has_toggled_wingtip_smokes(self):
        testee = user_has_toggled_wingtip_smokes

        string = "[8:33:05 PM] User0:Pe-8 turned wingtip smokes off at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, events.UserHasToggledWingtipSmokes)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.aircraft, "Pe-8")
        self.assertEqual(event.value, False)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.UserHasToggledWingtipSmokes)

        string = "[8:33:05 PM] User0:Pe-8 turned wingtip smokes on at 100.0 200.99"
        event = self.string_to_event(string, testee)
        self.assertEqual(event.value, True)

    def test_crew_member_was_wounded(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"
        event = self.string_to_event(string, crew_member_was_wounded)

        self.assertIsInstance(event, events.CrewMemberWasWounded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.aircraft, "Pe-8")
        self.assertEqual(event.seat_number, 0)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.CrewMemberWasWounded)

    def test_crew_member_was_heavily_wounded(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"
        event = self.string_to_event(string, crew_member_was_heavily_wounded)

        self.assertIsInstance(event, events.CrewMemberWasHeavilyWounded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.aircraft, "Pe-8")
        self.assertEqual(event.seat_number, 0)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertInAll(events.CrewMemberWasHeavilyWounded)
