# coding: utf-8

import datetime

from pyparsing import ParseException

from il2fb.parsers.events.grammar.primitives import (
    float_number, day_period, time, date, date_time,
)

from ..base import BaseTestCase


class FloatNumberTestCase(BaseTestCase):

    def test_positive_float_number(self):
        result = float_number.parseString("123.321")
        self.assertEqual(result[0], 123.321)

    def test_negative_float_number(self):
        result = float_number.parseString("-456.654")
        self.assertEqual(result[0], -456.654)


class DayPeriodTestCase(BaseTestCase):

    def test_day_period_is_am(self):
        self.assertEqual(day_period.parseString("AM").day_period, "AM")

    def test_day_period_is_pm(self):
        self.assertEqual(day_period.parseString("PM").day_period, "PM")

    def test_day_period_is_invalid(self):
        with self.assertRaises(ParseException):
            day_period.parseString("ZZ")


class PrimitivesTestCase(BaseTestCase):

    def test_time(self):
        expected = datetime.time(20, 33, 5)

        self.assertEqual(time.parseString("8:33:05 PM").time, expected)
        self.assertEqual(time.parseString("08:33:05 PM").time, expected)

    def test_date(self):
        result = date.parseString("Oct 30, 2013").date
        self.assertEqual(result, datetime.date(2013, 10, 30))

    def test_date_time(self):
        result = date_time.parseString("Oct 30, 2013 8:33:05 PM")

        self.assertEqual(result.date, datetime.date(2013, 10, 30))
        self.assertEqual(result.time, datetime.time(20, 33, 5))
