# -*- coding: utf-8 -*-

import re
import unittest2 as unittest

from il2ds_log_parser.regex import *


class BaseTestCase(unittest.TestCase):

    def _assert_time(self, groupdict, expected):
        self.assertTrue(groupdict)
        self.assertEqual(groupdict.get('time'), expected)

    def _assert_datetime(self, groupdict, expected):
        self.assertTrue(groupdict)
        self.assertEqual(groupdict.get('date'), expected['date'])
        self.assertEqual(groupdict.get('time'), expected['time'])


class TestTimestamp(BaseTestCase):

    def test_timestamp(self):
        rx = re.compile(RX_TIME)

        m = rx.match("[8:33:05 AM]")
        self.assertIsNotNone(m)
        self._assert_time(m.groupdict(), "8:33:05 AM")

        m = rx.match("[8:33:05 AM] foo")
        self.assertIsNotNone(m)
        self._assert_time(m.groupdict(), "8:33:05 AM")

        m = rx.match("[8:33:05 PM]")
        self.assertIsNotNone(m)
        self._assert_time(m.groupdict(), "8:33:05 PM")

        m = rx.match("[10:33:05 PM]")
        self.assertIsNotNone(m)
        self._assert_time(m.groupdict(), "10:33:05 PM")


    def test_datetimestamp(self):
        rx = re.compile(RX_DATE_TIME)

        m = rx.match("[Sep 15, 2013 8:33:05 PM]")
        self.assertIsNotNone(m)
        self._assert_datetime(m.groupdict(), {
            'date': "Sep 15, 2013",
            'time': "8:33:05 PM",
        })

        m = rx.match("[Sep 7, 2013 10:33:05 AM]")
        self.assertIsNotNone(m)
        self._assert_datetime(m.groupdict(), {
            'date': "Sep 7, 2013",
            'time': "10:33:05 AM",
        })


class TestMissionFlow(BaseTestCase):

    def test_mission_playing(self):
        rx = re.compile(RX_MISSION_PLAYING)

        m = rx.match("[Sep 15, 2013 8:33:08 PM] Mission: Helsinky.mis is Playing")
        self.assertIsNotNone(m)
        d = m.groupdict()
        self.assertEqual(d.get('date'), "Sep 15, 2013")
        self.assertEqual(d.get('time'), "8:33:08 PM")
        self.assertEqual(d.get('mission'), "Helsinky.mis")

        m = rx.match("[Sep 15, 2013 8:33:08 PM] Mission: test\Helsinky.mis is Playing")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict().get('mission'), "test\Helsinky.mis")

    def test_mission_begin(self):
        rx = re.compile(RX_MISSION_BEGIN)

        m = rx.match("[8:33:05 AM] Mission BEGIN")
        self.assertIsNotNone(m)
        self._assert_time(m.groupdict(), "8:33:05 AM")

    def test_mission_end(self):
        rx = re.compile(RX_MISSION_END)

        m = rx.match("[8:33:05 AM] Mission END")
        self.assertIsNotNone(m)
        self._assert_time(m.groupdict(), "8:33:05 AM")
