# -*- coding: utf-8 -*-

import unittest2 as unittest

from il2ds_log_parser import parse_log
from il2ds_log_parser.constants import (EVT_MISSION_PLAYING, EVT_MISSION_BEGIN,
    EVT_MISSION_END, )
from il2ds_log_parser.parser import parse_time, parse_date


class DatetimeTestCase(unittest.TestCase):

    def test_parse_time(self):
        result = parse_time("8:33:05 AM")
        self.assertEqual(result, "08:33:05")

        result = parse_time("8:33:05 PM")
        self.assertEqual(result, "20:33:05")

    def test_parse_date(self):
        result = parse_date("Sep 1, 2013")
        self.assertEqual(result, "2013-09-01")

        result = parse_date("Sep 15, 2013")
        self.assertEqual(result, "2013-09-15")


class GameFlowTestCase(unittest.TestCase):

    def test_parse_mission_playing(self):
        result = parse_log("[Sep 15, 2013 8:33:08 PM] Mission: Helsinky.mis is Playing")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_MISSION_PLAYING)
        self.assertEqual(result.get('date'), "2013-09-15")
        self.assertEqual(result.get('time'), "20:33:08")
        self.assertEqual(result.get('mission'), "Helsinky.mis")

    def test_parse_mission_begin(self):
        result = parse_log("[8:33:08 PM] Mission BEGIN")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_MISSION_BEGIN)
        self.assertEqual(result.get('time'), "20:33:08")

    def test_parse_mission_end(self):
        result = parse_log("[8:33:08 PM] Mission END")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_MISSION_END)
        self.assertEqual(result.get('time'), "20:33:08")
