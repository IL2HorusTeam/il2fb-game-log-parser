# -*- coding: utf-8 -*-

import unittest

from il2ds_log_parser import parse_evt
from il2ds_log_parser.events import *
from il2ds_log_parser.regex import *
from il2ds_log_parser.parser import (parse_time, parse_date,
    TimeStampedRegexParser, DateTimeStampedRegexParser, PositionedRegexParser,
    SeatRegexParser, VictimOfUserRegexParser, VictimOfStaticRegexParser,
    SeatVictimOfUserRegexParser, MultipleParser, RegistrationError, )


class DatetimeTestCase(unittest.TestCase):

    def test_parse_time(self):
        result = parse_time("08:33:05 AM")
        self.assertEqual(result, "08:33:05")

        result = parse_time("8:33:05 PM")
        self.assertEqual(result, "20:33:05")

    def test_parse_date(self):
        result = parse_date("Sep 1, 2013")
        self.assertEqual(result, "2013-09-01")

        result = parse_date("Sep 15, 2013")
        self.assertEqual(result, "2013-09-15")


class TimeStampedRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = TimeStampedRegexParser("^Hello,\s\S+!$")

        result = parser("Hi, user!")
        self.assertIsNone(result)

        result = parser("Hello, user!")
        self.assertIsNotNone(result)
        self.assertIsNone(result.get('time'))
        self.assertIsNone(result.get('type'))

    def test_call_with_time(self):
        parser = TimeStampedRegexParser(
            "{time}Hello,\s\S+!$".format(time=RX_TIME))

        result = parser("Hello, user!")
        self.assertIsNone(result)

        result = parser("[1:00:00 AM] Hello, user!")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), "01:00:00")
        self.assertIsNone(result.get('type'))

    def test_call_with_type(self):
        parser = TimeStampedRegexParser("Hello,\s\S+!$", 'TYPE')

        result = parser("Hello, user!")
        self.assertIsNotNone(result)
        self.assertIsNone(result.get('time'))
        self.assertEqual(result.get('type'), 'TYPE')

    def test_str(self):
        parser = TimeStampedRegexParser("^Hello!$")
        self.assertEqual(str(parser), "^Hello!$")

    def test_str_with_type(self):
        parser = TimeStampedRegexParser("^Hello!$", 'TYPE')
        self.assertEqual(str(parser), "TYPE: ^Hello!$")

    def test_equal(self):
        parser1 = TimeStampedRegexParser("^Hello!$",)
        parser2 = TimeStampedRegexParser("^Hello!$", 'TYPE')
        self.assertEqual(parser1, parser2)

        parser3 = TimeStampedRegexParser("^Hi!$", 'TYPE')
        self.assertNotEqual(parser1, parser3)


class DateStampedRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = DateTimeStampedRegexParser(
            "{datetime}Hello!$".format(datetime=RX_DATE_TIME))
        result = parser("[Sep 1, 2013 1:00:00 AM] Hello!")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('date'), "2013-09-01")
        self.assertEqual(result.get('time'), "01:00:00")


class PositionedRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = PositionedRegexParser(
            "{time}Hello{pos}".format(time=RX_TIME, pos=RX_POS))
        result = parser("[1:00:00 AM] Hello at 100.0 200.99")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), "01:00:00")
        pos = result.get('pos')
        self.assertIsNotNone(pos)
        self.assertEqual(pos.get('x'), 100.0)
        self.assertEqual(pos.get('y'), 200.99)


class SeatRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = SeatRegexParser(
            "{time_seat}hello{pos}".format(
                time_seat=RX_TIME_SEAT, pos=RX_POS))
        result = parser("[1:00:00 AM] User:Ubercraft(0) hello at 100.0 200.99")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), "01:00:00")
        self.assertEqual(result.get('callsign'), "User")
        self.assertEqual(result.get('aircraft'), "Ubercraft")
        self.assertEqual(result.get('seat'), 0)
        pos = result.get('pos')
        self.assertIsNotNone(pos)
        self.assertEqual(pos.get('x'), 100.0)
        self.assertEqual(pos.get('y'), 200.99)


class VictimOfUserRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = VictimOfUserRegexParser(
            "{time_aircraft}\swas\sgreeted\sby\s{eair}{pos}".format(
                time_aircraft=RX_TIME_AIRCRAFT,
                eair=RX_ENEMY_CALLSIGN_AIRCRAFT, pos=RX_POS))
        result = parser("[1:00:00 AM] User1:Ubercraft was greeted by User2:Ubercraft at 100.0 200.99")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), "01:00:00")
        self.assertEqual(result.get('callsign'), "User1")
        self.assertEqual(result.get('aircraft'), "Ubercraft")
        attacker = result.get('attacker')
        self.assertIsNotNone(attacker)
        self.assertEqual(attacker.get('callsign'), "User2")
        self.assertEqual(attacker.get('aircraft'), "Ubercraft")
        pos = result.get('pos')
        self.assertIsNotNone(pos)
        self.assertEqual(pos.get('x'), 100.0)
        self.assertEqual(pos.get('y'), 200.99)


class VictimOfStaticRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = VictimOfStaticRegexParser(
            "{time_aircraft}\swas\sgreeted\sby\s{static}{pos}".format(
                time_aircraft=RX_TIME_AIRCRAFT, static=RX_STATIC, pos=RX_POS))
        result = parser("[1:00:00 AM] User:Ubercraft was greeted by 0_Static at 100.0 200.99")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), "01:00:00")
        self.assertEqual(result.get('callsign'), "User")
        self.assertEqual(result.get('aircraft'), "Ubercraft")
        self.assertEqual(result.get('attacker'), "0_Static")
        pos = result.get('pos')
        self.assertIsNotNone(pos)
        self.assertEqual(pos.get('x'), 100.0)
        self.assertEqual(pos.get('y'), 200.99)


class SeatVictimOfUserRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = SeatVictimOfUserRegexParser(
            "{time_seat}was\sgreeted\sby\s{eair}{pos}".format(
                time_seat=RX_TIME_SEAT,
                eair=RX_ENEMY_CALLSIGN_AIRCRAFT, pos=RX_POS))
        result = parser("[1:00:00 AM] User1:Ubercraft(0) was greeted by User2:Ubercraft at 100.0 200.99")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), "01:00:00")
        self.assertEqual(result.get('callsign'), "User1")
        self.assertEqual(result.get('aircraft'), "Ubercraft")
        self.assertEqual(result.get('seat'), 0)
        attacker = result.get('attacker')
        self.assertIsNotNone(attacker)
        self.assertEqual(attacker.get('callsign'), "User2")
        self.assertEqual(attacker.get('aircraft'), "Ubercraft")
        pos = result.get('pos')
        self.assertIsNotNone(pos)
        self.assertEqual(pos.get('x'), 100.0)
        self.assertEqual(pos.get('y'), 200.99)


class MultipleParserTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = MultipleParser()

    def _build_parser(self):
        return TimeStampedRegexParser(
            "{time}Hello,\s(?P<name>\S+)!$".format(time=RX_TIME))

    def test_register_unregister(self):

        parser1 = self._build_parser()
        parser2 = self._build_parser()

        self.assertNotEqual(parser1, parser2)
        self.parser.register(parser1)
        self.assertTrue(self.parser.is_registered(parser1))

        with self.assertRaises(Exception) as ctx:
            self.parser.register(parser2)

        self.assertIsInstance(ctx.exception, RegistrationError)
        self.assertEqual(
            ctx.exception.message,
            "Parser is already registered: {parser}".format(parser=parser2))

        self.parser.unregister(parser1)
        self.assertFalse(self.parser.is_registered(parser1))

        with self.assertRaises(Exception) as ctx:
            self.parser.unregister(parser1)

        self.assertIsInstance(ctx.exception, RegistrationError)
        self.assertEqual(
            ctx.exception.message,
            "Parser is not registered yet: {parser}".format(parser=parser1))
        self.assertFalse(self.parser.is_registered(parser2))

        self.parser.register(parser2)
        self.assertTrue(self.parser.is_registered(parser2))

    def test_call(self):
        self.parser.register(self._build_parser())
        result = self.parser("Hello, username!")
        self.assertIsNone(result)

        result = self.parser("[1:00:00 AM] Hello, username!")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), "01:00:00")
        self.assertEqual(result.get('name'), "username")

    def test_callback(self):
        result = {}

        def callback(data):
            self.assertIsInstance(data, dict)
            result.update(data)

        self.parser.register(self._build_parser(), callback)
        self.parser("[1:00:00 AM] Hello, username!")
        self.assertEqual(result.get('time'), "01:00:00")
        self.assertEqual(result.get('name'), "username")


class GameFlowTestCase(unittest.TestCase):

    def test_parse_mission_playing(self):
        result = parse_evt("[Sep 15, 2013 8:33:08 PM] Mission: Helsinky.mis is Playing")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_MISSION_PLAYING)
        self.assertEqual(result.get('date'), "2013-09-15")
        self.assertEqual(result.get('time'), "20:33:08")
        self.assertEqual(result.get('mission'), "Helsinky.mis")

    def test_parse_mission_begin(self):
        result = parse_evt("[8:33:08 PM] Mission BEGIN")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_MISSION_BEGIN)
        self.assertEqual(result.get('time'), "20:33:08")

    def test_parse_mission_end(self):
        result = parse_evt("[8:33:08 PM] Mission END")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_MISSION_END)
        self.assertEqual(result.get('time'), "20:33:08")
