# -*- coding: utf-8 -*-

import datetime

from pyparsing import ParseException

from il2fb.parsers.events.grammar import (
    day_period, time,
)

from .base import BaseTestCase


class GrammarTestCase(BaseTestCase):

    def test_day_period(self):
        self.assertEqual(day_period.parseString("AM").day_period, "AM")
        self.assertEqual(day_period.parseString("PM").day_period, "PM")

        with self.assertRaises(ParseException):
            day_period.parseString("ZZ")

    def test_time(self):
        expected = datetime.time(20, 33, 05)

        self.assertEqual(time.parseString("8:33:05 PM").time, expected)
        self.assertEqual(time.parseString("08:33:05 PM").time, expected)
