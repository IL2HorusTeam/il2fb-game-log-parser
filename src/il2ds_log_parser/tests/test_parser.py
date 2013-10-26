# -*- coding: utf-8 -*-

import unittest

from il2ds_log_parser import parse_evt
from il2ds_log_parser.events import *
from il2ds_log_parser.parser import *
from il2ds_log_parser.parser import parse_time, parse_date
from il2ds_log_parser.regex import *
from il2ds_log_parser.regex import (RX_TIME_BASE, RX_TIME, RX_DATE_TIME,
    RX_POS, RX_TOGGLE_VALUE, RX_SEAT, RX_STATIC, RX_ENEMY_CALLSIGN_AIRCRAFT,
    RX_TIME_CALLSIGN, RX_TIME_AIRCRAFT, RX_TIME_SEAT, RX_DESTROYED_BY, )


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
        parser = TimeStampedRegexParser(
            "{time}Hello,\s\S+!$".format(time=RX_TIME))

        result = parser("Hello, user!")
        self.assertIsNone(result)

        result = parser("[1:00:00 AM] Hello, user!")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), "01:00:00")
        self.assertIsNone(result.get('type'))

    def test_call_with_type(self):
        parser = TimeStampedRegexParser(
            "{time}Hello,\s\S+!$".format(time=RX_TIME), 'TYPE')

        result = parser("Hello, user!")
        self.assertIsNone(result)

        result = parser("[1:00:00 AM] Hello, user!")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), "01:00:00")
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


class NumeratedRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = NumeratedRegexParser(
            "{time}Hello,\s(?P<number>\d+)!$".format(time=RX_TIME))
        result = parser("[1:00:00 AM] Hello, 1!")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), "01:00:00")
        self.assertEqual(result.get('number'), 1)


class FuelRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = FuelRegexParser(
            "{time}Fuel\sis\sat\s(?P<fuel>\d+)%$".format(time=RX_TIME))
        result = parser("[1:00:00 AM] Fuel is at 100%")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), "01:00:00")
        self.assertEqual(result.get('fuel'), 100)


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


class DefaultEventParserTestCase(unittest.TestCase):

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

    def test_parse_mission_won(self):
        result = parse_evt("[Dec 29, 2012 5:19:49 PM] Mission: RED WON")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_MISSION_WON)
        self.assertEqual(result.get('date'), "2012-12-29")
        self.assertEqual(result.get('time'), "17:19:49")
        self.assertEqual(result.get('army'), "RED")

    def test_target_complete(self):
        result = parse_evt("[5:15:22 PM] Target 3 Complete")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_TARGET_END)
        self.assertEqual(result.get('time'), "17:15:22")
        self.assertEqual(result.get('number'), 3)
        self.assertEqual(result.get('result'), "Complete")

        result = parse_evt("[5:19:49 PM] Target 5 Failed")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_TARGET_END)
        self.assertEqual(result.get('time'), "17:19:49")
        self.assertEqual(result.get('number'), 5)
        self.assertEqual(result.get('result'), "Failed")

    def test_connected(self):
        result = parse_evt("[8:33:16 PM] User has connected")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_CONNECTED)
        self.assertEqual(result.get('time'), "20:33:16")
        self.assertEqual(result.get('callsign'), "User")

    def test_disconnected(self):
        result = parse_evt("[8:49:28 PM] User has disconnected")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_DISCONNECTED)
        self.assertEqual(result.get('time'), "20:49:28")
        self.assertEqual(result.get('callsign'), "User")

    def test_went_to_menu(self):
        result = parse_evt("[8:49:20 PM] User entered refly menu")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_WENT_TO_MENU)
        self.assertEqual(result.get('time'), "20:49:20")
        self.assertEqual(result.get('callsign'), "User")

    def test_weapons_loaded(self):
        result = parse_evt("[8:47:27 PM] User:Pe-8 loaded weapons '40fab100' fuel 40%")
        self.assertIsNotNone(result)

        self.assertEqual(result.get('type'), EVT_WEAPONS_LOADED)
        self.assertEqual(result.get('time'), "20:47:27")
        self.assertEqual(result.get('callsign'), "User")
        self.assertEqual(result.get('loadout'), "40fab100")
        self.assertEqual(result.get('fuel'), 40)
