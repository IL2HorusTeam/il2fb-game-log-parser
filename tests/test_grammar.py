# -*- coding: utf-8 -*-

from pyparsing import ParseException

from il2fb.parsers.events.grammar import (
    day_period,
)

from .base import BaseTestCase


class GrammarTestCase(BaseTestCase):

    def test_day_period(self):
        self.assertEqual(day_period.parseString('AM').day_period, 'AM')
        self.assertEqual(day_period.parseString('PM').day_period, 'PM')

        with self.assertRaises(ParseException):
            day_period.parseString('ZZ')
