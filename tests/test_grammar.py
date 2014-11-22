# -*- coding: utf-8 -*-

import datetime

from pyparsing import ParseException

from il2fb.parsers.events.grammar import (
    day_period, time, event_time, date, date_time, event_date_time,
    float_number,
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

    def test_event_time(self):
        result = event_time.parseString("[08:33:05 PM] ")
        self.assertEqual(result.time, datetime.time(20, 33, 05))

    def test_date(self):
        result = date.parseString("Oct 30, 2013")
        self.assertEqual(result.date, datetime.date(2013, 10, 30))

    def test_date_time(self):
        result = date_time.parseString("Oct 30, 2013 8:33:05 PM")

        self.assertEqual(result.date, datetime.date(2013, 10, 30))
        self.assertEqual(result.time, datetime.time(20, 33, 05))

    def test_event_date_time(self):
        result = event_date_time.parseString("[Oct 30, 2013 8:33:05 PM] ")

        self.assertEqual(result.date, datetime.date(2013, 10, 30))
        self.assertEqual(result.time, datetime.time(20, 33, 05))

    def test_float_number(self):
        result = float_number.parseString("123.321")
        self.assertEqual(result[0], 123.321)
