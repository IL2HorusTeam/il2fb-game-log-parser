# -*- coding: utf-8 -*-

import unittest2 as unittest

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
