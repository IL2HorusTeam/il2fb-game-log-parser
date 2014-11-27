# -*- coding: utf-8 -*-

import datetime

from il2fb.commons.organization import Belligerents

from il2fb.parsers.events.constants import TARGET_END_STATES
from il2fb.parsers.events.grammar.events import (
    mission_is_playing, mission_has_begun, mission_has_ended,
    mission_was_won, target_state_has_changed,
)
from il2fb.parsers.events.structures import (
    MissionIsPlaying, MissionHasBegun, MissionHasEnded, MissionWasWon,
    TargetStateHasChanged,
)

from ..base import BaseTestCase


class EventsGrammarTestCase(BaseTestCase):

    def test_mission_is_playing(self):
        string = "[Sep 15, 2013 8:33:05 PM] Mission: path/PH.mis is Playing"
        result = mission_is_playing.parseString(string).event

        self.assertIsInstance(result, MissionIsPlaying)
        self.assertEqual(result.date, datetime.date(2013, 9, 15))
        self.assertEqual(result.time, datetime.time(20, 33, 5))
        self.assertEqual(result.mission, "path/PH.mis")

    def test_mission_has_begun(self):
        string = "[8:33:05 PM] Mission BEGIN"
        result = mission_has_begun.parseString(string).event

        self.assertIsInstance(result, MissionHasBegun)
        self.assertEqual(result.time, datetime.time(20, 33, 5))

    def test_mission_has_ended(self):
        string = "[8:33:05 PM] Mission END"
        result = mission_has_ended.parseString(string).event

        self.assertIsInstance(result, MissionHasEnded)
        self.assertEqual(result.time, datetime.time(20, 33, 5))

    def test_mission_was_won(self):
        string = "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"
        result = mission_was_won.parseString(string).event

        self.assertIsInstance(result, MissionWasWon)
        self.assertEqual(result.date, datetime.date(2013, 9, 15))
        self.assertEqual(result.time, datetime.time(20, 33, 5))
        self.assertEqual(result.belligerent, Belligerents.red)


class TargetEndStateHasChangedTestCase(BaseTestCase):

    def test_target_state_has_changed_to_complete(self):
        string = "[8:33:05 PM] Target 3 Complete"
        result = target_state_has_changed.parseString(string).event

        self.assertIsInstance(result, TargetStateHasChanged)
        self.assertEqual(result.time, datetime.time(20, 33, 5))
        self.assertEqual(result.target_index, 3)
        self.assertEqual(result.state, TARGET_END_STATES.COMPLETE)

    def test_target_state_has_changed_to_failed(self):
        string = "[8:33:05 PM] Target 4 Failed"
        result = target_state_has_changed.parseString(string).event

        self.assertIsInstance(result, TargetStateHasChanged)
        self.assertEqual(result.time, datetime.time(20, 33, 5))
        self.assertEqual(result.target_index, 4)
        self.assertEqual(result.state, TARGET_END_STATES.FAILED)
