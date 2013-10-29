# -*- coding: utf-8 -*-

import datetime
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
        self.assertEqual(result, datetime.time(8, 33, 5))

        result = parse_time("8:33:05 PM")
        self.assertEqual(result, datetime.time(20, 33, 5))

    def test_parse_date(self):
        result = parse_date("Sep 1, 2013")
        self.assertEqual(result, datetime.date(2013, 9, 1))

        result = parse_date("Feb 15, 2013")
        self.assertEqual(result, datetime.date(2013, 2, 15))


class TimeStampedRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = TimeStampedRegexParser(
            "{time}Hello,\s\S+!$".format(time=RX_TIME))

        result = parser("Hello, user!")
        self.assertIsNone(result)

        result = parser("[1:00:00 AM] Hello, user!")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), datetime.time(1, 0))
        self.assertIsNone(result.get('type'))

    def test_call_with_type(self):
        parser = TimeStampedRegexParser(
            "{time}Hello,\s\S+!$".format(time=RX_TIME), 'TYPE')

        result = parser("Hello, user!")
        self.assertIsNone(result)

        result = parser("[1:00:00 AM] Hello, user!")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), datetime.time(1, 0))
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
        self.assertEqual(result.get('date'), datetime.date(2013, 9, 1))
        self.assertEqual(result.get('time'), datetime.time(1, 0))


class NumeratedRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = NumeratedRegexParser(
            "{time}Hello,\s(?P<number>\d+)!$".format(time=RX_TIME))
        result = parser("[1:00:00 AM] Hello, 1!")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), datetime.time(1, 0))
        self.assertEqual(result.get('number'), 1)


class FuelRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = FuelRegexParser(
            "{time}Fuel\sis\sat\s(?P<fuel>\d+)%$".format(time=RX_TIME))
        result = parser("[1:00:00 AM] Fuel is at 100%")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), datetime.time(1, 0))
        self.assertEqual(result.get('fuel'), 100)


class PositionedRegexParserTestCase(unittest.TestCase):

    def test_call(self):
        parser = PositionedRegexParser(
            "{time}Hello{pos}".format(time=RX_TIME, pos=RX_POS))
        result = parser("[1:00:00 AM] Hello at 100.0 200.99")
        self.assertIsNotNone(result)
        self.assertEqual(result.get('time'), datetime.time(1, 0))
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
        self.assertEqual(result.get('time'), datetime.time(1, 0))
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
        self.assertEqual(result.get('time'), datetime.time(1, 0))
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
        self.assertEqual(result.get('time'), datetime.time(1, 0))
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
        self.assertEqual(result.get('time'), datetime.time(1, 0))
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
        self.assertEqual(result.get('time'), datetime.time(1, 0))
        self.assertEqual(result.get('name'), "username")

    def test_callback(self):
        result = {}

        def callback(data):
            self.assertIsInstance(data, dict)
            result.update(data)

        self.parser.register(self._build_parser(), callback)
        self.parser("[1:00:00 AM] Hello, username!")
        self.assertEqual(result.get('time'), datetime.time(1, 0))
        self.assertEqual(result.get('name'), "username")


class DefaultEventParserTestCase(unittest.TestCase):

    def assertPos(self, data, x, y):
        pos = data.get('pos')
        self.assertIsNotNone(pos)
        self.assertEqual(pos.get('x'), x)
        self.assertEqual(pos.get('y'), y)

    def assertCalsignAircraft(self, data, callsign, aircraft):
        self.assertEqual(data.get('callsign'), callsign)
        self.assertEqual(data.get('aircraft'), aircraft)

    def assertAttackingUser(self, data, callsign, aircraft):
        attacker = data.get('attacker')
        self.assertIsNotNone(attacker)
        self.assertCalsignAircraft(attacker, callsign, aircraft)

    def test_parse_mission_playing(self):
        evt = parse_evt("[Sep 15, 2013 8:33:08 PM] Mission: Helsinky.mis is Playing")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_MISSION_PLAYING)
        self.assertEqual(evt.get('date'), datetime.date(2013, 9, 15))
        self.assertEqual(evt.get('time'), datetime.time(20, 33, 8))
        self.assertEqual(evt.get('mission'), "Helsinky.mis")

    def test_parse_mission_begin(self):
        evt = parse_evt("[8:33:08 PM] Mission BEGIN")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_MISSION_BEGIN)
        self.assertEqual(evt.get('time'), datetime.time(20, 33, 8))

    def test_parse_mission_end(self):
        evt = parse_evt("[8:33:08 PM] Mission END")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_MISSION_END)
        self.assertEqual(evt.get('time'), datetime.time(20, 33, 8))

    def test_parse_mission_won(self):
        evt = parse_evt("[Dec 29, 2012 5:19:49 PM] Mission: RED WON")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_MISSION_WON)
        self.assertEqual(evt.get('date'), datetime.date(2012, 12, 29))
        self.assertEqual(evt.get('time'), datetime.time(17, 19, 49))
        self.assertEqual(evt.get('army'), "RED")

    def test_target_complete(self):
        evt = parse_evt("[5:15:22 PM] Target 3 Complete")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_TARGET_END)
        self.assertEqual(evt.get('time'), datetime.time(17, 15, 22))
        self.assertEqual(evt.get('number'), 3)
        self.assertEqual(evt.get('result'), "Complete")

        evt = parse_evt("[5:19:49 PM] Target 5 Failed")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_TARGET_END)
        self.assertEqual(evt.get('time'), datetime.time(17, 19, 49))
        self.assertEqual(evt.get('number'), 5)
        self.assertEqual(evt.get('result'), "Failed")

    def test_connected(self):
        evt = parse_evt("[8:33:16 PM] User has connected")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_CONNECTED)
        self.assertEqual(evt.get('time'), datetime.time(20, 33, 16))
        self.assertEqual(evt.get('callsign'), "User")

    def test_disconnected(self):
        evt = parse_evt("[8:49:28 PM] User has disconnected")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_DISCONNECTED)
        self.assertEqual(evt.get('time'), datetime.time(20, 49, 28))
        self.assertEqual(evt.get('callsign'), "User")

    def test_went_to_menu(self):
        evt = parse_evt("[8:49:20 PM] User entered refly menu")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_WENT_TO_MENU)
        self.assertEqual(evt.get('time'), datetime.time(20, 49, 20))
        self.assertEqual(evt.get('callsign'), "User")

    def test_army_selected(self):
        evt = parse_evt("[8:46:57 PM] User selected army Red at 238667.0 104506.0")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_SELECTED_ARMY)
        self.assertEqual(evt.get('time'), datetime.time(20, 46, 57))
        self.assertEqual(evt.get('callsign'), "User")
        self.assertEqual(evt.get('army'), "Red")
        self.assertPos(evt, 238667.0, 104506.0)

    def test_weapons_loaded(self):
        evt = parse_evt("[8:47:27 PM] User:Pe-8 loaded weapons '40fab100' fuel 40%")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_WEAPONS_LOADED)
        self.assertEqual(evt.get('time'), datetime.time(20, 47, 27))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('loadout'), "40fab100")
        self.assertEqual(evt.get('fuel'), 40)

    def test_seat_selected(self):
        evt = parse_evt("[8:47:27 PM] User:Pe-8(0) seat occupied by User at 238667.5 104125.0")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_SEAT_OCCUPIED)
        self.assertEqual(evt.get('time'), datetime.time(20, 47, 27))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('seat'), 0)
        self.assertPos(evt, 238667.5, 104125.0)

    def test_bailed_out(self):
        evt = parse_evt("[9:31:20 PM] User:Pe-8(0) bailed out at 149880.23 105703.76")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_BAILED_OUT)
        self.assertEqual(evt.get('time'), datetime.time(21, 31, 20))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('seat'), 0)
        self.assertPos(evt, 149880.23, 105703.76)

    def test_parachute_opened(self):
        evt = parse_evt("[9:33:20 PM] User:Pe-8(0) successfully bailed out at 148534.2 105877.93")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_PARACHUTE_OPENED)
        self.assertEqual(evt.get('time'), datetime.time(21, 33, 20))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('seat'), 0)
        self.assertPos(evt, 148534.2, 105877.93)

    def test_toggle_landing_lights(self):
        evt = parse_evt("[8:47:45 PM] User:Pe-8 turned landing lights on at 238667.52 104125.04")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_TOGGLE_LANDING_LIGHTS)
        self.assertEqual(evt.get('time'), datetime.time(20, 47, 45))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('value'), True)
        self.assertPos(evt, 238667.52, 104125.04)

        evt = parse_evt("[8:47:47 PM] User:Pe-8 turned landing lights off at 238667.52 104125.04")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_TOGGLE_LANDING_LIGHTS)
        self.assertEqual(evt.get('time'), datetime.time(20, 47, 47))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('value'), False)
        self.assertPos(evt, 238667.52, 104125.04)

    def test_toggle_wingtip_smokes(self):
        evt = parse_evt("[9:09:39 PM] User:Pe-8 turned wingtip smokes on at 208420.42 103602.61")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_TOGGLE_WINGTIP_SMOKES)
        self.assertEqual(evt.get('time'), datetime.time(21, 9, 39))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('value'), True)
        self.assertPos(evt, 208420.42, 103602.61)

        evt = parse_evt("[9:09:42 PM] User:Pe-8 turned wingtip smokes off at 208370.92 103669.64")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_TOGGLE_WINGTIP_SMOKES)
        self.assertEqual(evt.get('time'), datetime.time(21, 9, 42))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('value'), False)
        self.assertPos(evt, 208370.92, 103669.64)

    def test_took_off(self):
        evt = parse_evt("[9:09:56 PM] User:Pe-8 in flight at 207635.0 104367.586")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_TOOK_OFF)
        self.assertEqual(evt.get('time'), datetime.time(21, 9, 56))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 207635.0, 104367.586)

    def test_wounded(self):
        evt = parse_evt("[9:49:14 PM] User:Bf-109G-6_Late(0) was wounded at 89172.44 123074.15")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_WOUNDED)
        self.assertEqual(evt.get('time'), datetime.time(21, 49, 14))
        self.assertCalsignAircraft(evt, "User", "Bf-109G-6_Late")
        self.assertEqual(evt.get('seat'), 0)
        self.assertPos(evt, 89172.44, 123074.15)

    def test_heavily_wounded(self):
        evt = parse_evt("[9:50:24 PM] User:Pe-8(7) was heavily wounded at 84521.69 123442.84")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_HEAVILY_WOUNDED)
        self.assertEqual(evt.get('time'), datetime.time(21, 50, 24))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('seat'), 7)
        self.assertPos(evt, 84521.69, 123442.84)

    def test_killed(self):
        evt = parse_evt("[9:54:03 PM] User:Pe-8(0) was killed at 209064.98 102002.914")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_KILLED)
        self.assertEqual(evt.get('time'), datetime.time(21, 54, 3))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('seat'), 0)
        self.assertPos(evt, 209064.98, 102002.914)

    def test_killed_by_user(self):
        evt = parse_evt("[9:48:18 PM] User1:Bf-109G-6_Late(0) was killed by User2:Pe-8 at 53694.484 140936.42")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_KILLED_BY_USER)
        self.assertEqual(evt.get('time'), datetime.time(21, 48, 18))
        self.assertCalsignAircraft(evt, "User1", "Bf-109G-6_Late")
        self.assertEqual(evt.get('seat'), 0)
        self.assertAttackingUser(evt, "User2", "Pe-8")
        self.assertPos(evt, 53694.484, 140936.42)

    def test_captured(self):
        evt = parse_evt("[9:53:17 PM] User:Pe-8(2) was captured at 48024.66 126228.92")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_CAPTURED)
        self.assertEqual(evt.get('time'), datetime.time(21, 53, 17))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('seat'), 2)
        self.assertPos(evt, 48024.66, 126228.92)

    def test_crashed(self):
        evt = parse_evt("[9:53:59 PM] User:Pe-8 crashed at 90787.76 119865.445")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_CRASHED)
        self.assertEqual(evt.get('time'), datetime.time(21, 53, 59))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 90787.76, 119865.445)

    def test_landed(self):
        evt = parse_evt("[10:22:57 PM] User:Pe-8 landed at 209123.62 102794.375")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_LANDED)
        self.assertEqual(evt.get('time'), datetime.time(22, 22, 57))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 209123.62, 102794.375)

    def test_destroyed_building(self):
        evt = parse_evt("[9:41:39 PM] 3do/Buildings/Industrial/FactoryHouse1_W/live.sim destroyed by User:Pe-8 at 48734.32 131787.66")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_DESTROYED_BLD)
        self.assertEqual(evt.get('time'), datetime.time(21, 41, 39))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('building'), "FactoryHouse1_W")
        self.assertPos(evt, 48734.32, 131787.66)

    def test_destroyed_tree(self):
        evt = parse_evt("[9:41:56 PM] 3do/Tree/Line_W/live.sim destroyed by User:Pe-8 at 47617.54 131795.72")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_DESTROYED_TREE)
        self.assertEqual(evt.get('time'), datetime.time(21, 41, 56))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('tree'), "Line_W")
        self.assertPos(evt, 47617.54, 131795.72)

    def test_destroyed_static(self):
        evt = parse_evt("[9:42:27 PM] 200_Static destroyed by User:Pe-8 at 46240.0 132810.0")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_DESTROYED_STATIC)
        self.assertEqual(evt.get('time'), datetime.time(21, 42, 27))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('static'), "200_Static")
        self.assertPos(evt, 46240.0, 132810.0)

    def test_destroyed_bridge(self):
        evt = parse_evt("[5:17:41 PM]  Bridge0 destroyed by User:Bf-110G-2 at 11108.0 47692.0")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_DESTROYED_BRIDGE)
        self.assertEqual(evt.get('time'), datetime.time(17, 17, 41))
        self.assertCalsignAircraft(evt, "User", "Bf-110G-2")
        self.assertEqual(evt.get('bridge'), "Bridge0")
        self.assertPos(evt, 11108.0, 47692.0)

    def test_damaged_on_the_ground(self):
        evt = parse_evt("[10:25:54 PM] User:Pe-8 damaged on the ground at 208571.47 103295.33")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_DAMAGED_ON_GROUND)
        self.assertEqual(evt.get('time'), datetime.time(22, 25, 54))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 208571.47, 103295.33)

    def test_damaged_by_user(self):
        evt = parse_evt("[10:25:32 PM] User1:Pe-8 damaged by User2:Bf-109G-6_Late at 208901.16 102836.57")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_DAMAGED_BY_USER)
        self.assertEqual(evt.get('time'), datetime.time(22, 25, 32))
        self.assertCalsignAircraft(evt, "User1", "Pe-8")
        self.assertAttackingUser(evt, "User2", "Bf-109G-6_Late")
        self.assertPos(evt, 208901.16, 102836.57)

    def test_damaged_self(self):
        evt = parse_evt("[10:26:24 PM] User:Pe-8 damaged by landscape at 207773.69 104716.07")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_DAMAGED_SELF)
        self.assertEqual(evt.get('time'), datetime.time(22, 26, 24))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 207773.69, 104716.07)

    def test_shot_down_by_user(self):
        evt = parse_evt("[9:31:51 PM] User1:Pe-8 shot down by User2:Pe-8 at 148687.02 105729.086")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_SHOT_DOWN_BY_USER)
        self.assertEqual(evt.get('time'), datetime.time(21, 31, 51))
        self.assertCalsignAircraft(evt, "User1", "Pe-8")
        self.assertAttackingUser(evt, "User2", "Pe-8")
        self.assertPos(evt, 148687.02, 105729.086)

    def test_shot_down_self(self):
        evt = parse_evt("[8:52:43 PM] User:Pe-8 shot down by landscape at 208531.81 103386.945")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_SHOT_DOWN_SELF)
        self.assertEqual(evt.get('time'), datetime.time(20, 52, 43))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 208531.81, 103386.945)

    def test_shot_down_by_static(self):
        evt = parse_evt("[9:45:16 PM] User:Pe-8 shot down by 85_Static at 47626.78 126637.38")
        self.assertIsNotNone(evt)
        self.assertEqual(evt.get('type'), EVT_SHOT_DOWN_BY_STATIC)
        self.assertEqual(evt.get('time'), datetime.time(21, 45, 16))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt.get('attacker'), "85_Static")
        self.assertPos(evt, 47626.78, 126637.38)
