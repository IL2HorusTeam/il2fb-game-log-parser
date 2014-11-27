# -*- coding: utf-8 -*-

import datetime

from il2fb.commons.organization import Belligerents

from il2fb.parsers.events.constants import TargetEndStates
from il2fb.parsers.events.grammar.events import (
    mission_is_playing, mission_has_begun, mission_has_ended,
    mission_was_won, target_state_has_changed, user_has_connected,
)
from il2fb.parsers.events.structures.events import (
    MissionIsPlaying, MissionHasBegun, MissionHasEnded, MissionWasWon,
    TargetStateHasChanged, UserHasConnected,
)

from ..base import BaseTestCase


class EventsGrammarTestCase(BaseTestCase):

    @staticmethod
    def string_to_event(string, grammar):
        return grammar.parseString(string).event

    def test_mission_is_playing(self):
        string = "[Sep 15, 2013 8:33:05 PM] Mission: path/PH.mis is Playing"
        event = self.string_to_event(string, mission_is_playing)

        self.assertIsInstance(event, MissionIsPlaying)
        self.assertEqual(event.date, datetime.date(2013, 9, 15))
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.mission, "path/PH.mis")

    def test_mission_has_begun(self):
        string = "[8:33:05 PM] Mission BEGIN"
        event = self.string_to_event(string, mission_has_begun)

        self.assertIsInstance(event, MissionHasBegun)
        self.assertEqual(event.time, datetime.time(20, 33, 5))

    def test_mission_has_ended(self):
        string = "[8:33:05 PM] Mission END"
        event = self.string_to_event(string, mission_has_ended)

        self.assertIsInstance(event, MissionHasEnded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))

    def test_mission_was_won(self):
        string = "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"
        event = self.string_to_event(string, mission_was_won)

        self.assertIsInstance(event, MissionWasWon)
        self.assertEqual(event.date, datetime.date(2013, 9, 15))
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.belligerent, Belligerents.red)

    def test_target_state_has_changed(self):
        string = "[8:33:05 PM] Target 3 Complete"
        event = self.string_to_event(string, target_state_has_changed)

        self.assertIsInstance(event, TargetStateHasChanged)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.target_index, 3)
        self.assertEqual(event.state, TargetEndStates.COMPLETE)

        string = "[8:33:05 PM] Target 4 Failed"
        event = self.string_to_event(string, target_state_has_changed)

        self.assertIsInstance(event, TargetStateHasChanged)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.target_index, 4)
        self.assertEqual(event.state, TargetEndStates.FAILED)

    def test_user_has_connected(self):
        string = "[8:33:05 PM] User0 has connected"
        event = user_has_connected.parseString(string).event
        event = self.string_to_event(string, user_has_connected)

        self.assertIsInstance(event, UserHasConnected)
        self.assertEqual(event.callsign, "User0")
