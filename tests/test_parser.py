# -*- coding: utf-8 -*-
import datetime
import unittest

from il2fb.parsers.events import parse_evt
from il2fb.parsers.events.content_processor import process_time
from il2fb.parsers.events.event_types import *
from il2fb.parsers.events.parser import *

from il2fb.parsers.events.regex import *
from il2fb.parsers.events.regex import RX_TIME


class MultipleParserTestCase(unittest.TestCase):

    def setUp(self):
        self.parser = MultipleParser()

    def _build_parser(self):
        rx = "{time}Hello,\s(?P<name>\S+)!$".format(time=RX_TIME)
        return RegexParser(rx, process_time)

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
        self.assertEqual(result['time'], datetime.time(1, 0))
        self.assertEqual(result['name'], "username")

    def test_callback(self):
        result = {}

        def callback(data):
            self.assertIsInstance(data, dict)
            result.update(data)

        self.parser.register(self._build_parser(), callback)
        self.parser("[1:00:00 AM] Hello, username!")
        self.assertEqual(result['time'], datetime.time(1, 0))
        self.assertEqual(result['name'], "username")


class DefaultEventParserTestCase(unittest.TestCase):

    def assertPos(self, data, x, y):
        pos = data['pos']
        self.assertIsNotNone(pos)
        self.assertEqual(pos['x'], x)
        self.assertEqual(pos['y'], y)

    def assertCalsignAircraft(self, data, callsign, aircraft):
        self.assertEqual(data['callsign'], callsign)
        self.assertEqual(data['aircraft'], aircraft)

    def assertAttackingUser(self, data, callsign, aircraft):
        attacker = data['attacker']
        self.assertIsNotNone(attacker)
        self.assertCalsignAircraft(attacker, callsign, aircraft)

    def test_parse_mission_playing(self):
        evt = parse_evt("[Sep 15, 2013 8:33:08 PM] Mission: Helsinky.mis is Playing")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_MISSION_PLAYING)
        self.assertEqual(evt['date'], datetime.date(2013, 9, 15))
        self.assertEqual(evt['time'], datetime.time(20, 33, 8))
        self.assertEqual(evt['mission'], "Helsinky.mis")

    def test_parse_mission_begin(self):
        evt = parse_evt("[8:33:08 PM] Mission BEGIN")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_MISSION_BEGIN)
        self.assertEqual(evt['time'], datetime.time(20, 33, 8))

    def test_parse_mission_end(self):
        evt = parse_evt("[8:33:08 PM] Mission END")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_MISSION_END)
        self.assertEqual(evt['time'], datetime.time(20, 33, 8))

    def test_parse_mission_won(self):
        evt = parse_evt("[Dec 29, 2012 5:19:49 PM] Mission: RED WON")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_MISSION_WON)
        self.assertEqual(evt['date'], datetime.date(2012, 12, 29))
        self.assertEqual(evt['time'], datetime.time(17, 19, 49))
        self.assertEqual(evt['army'], "Red")

    def test_target_result(self):
        evt = parse_evt("[5:15:22 PM] Target 3 Complete")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_TARGET_RESULT)
        self.assertEqual(evt['time'], datetime.time(17, 15, 22))
        self.assertEqual(evt['number'], 3)
        self.assertEqual(evt['result'], True)

        evt = parse_evt("[5:19:49 PM] Target 5 Failed")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_TARGET_RESULT)
        self.assertEqual(evt['time'], datetime.time(17, 19, 49))
        self.assertEqual(evt['number'], 5)
        self.assertEqual(evt['result'], False)

    def test_connected(self):
        evt = parse_evt("[8:33:16 PM] User has connected")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_CONNECTED)
        self.assertEqual(evt['time'], datetime.time(20, 33, 16))
        self.assertEqual(evt['callsign'], "User")

    def test_disconnected(self):
        evt = parse_evt("[8:49:28 PM] User has disconnected")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_DISCONNECTED)
        self.assertEqual(evt['time'], datetime.time(20, 49, 28))
        self.assertEqual(evt['callsign'], "User")

    def test_went_to_menu(self):
        evt = parse_evt("[8:49:20 PM] User entered refly menu")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_WENT_TO_MENU)
        self.assertEqual(evt['time'], datetime.time(20, 49, 20))
        self.assertEqual(evt['callsign'], "User")

    def test_army_selected(self):
        evt = parse_evt("[8:46:57 PM] User selected army Red at 238667.0 104506.0")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_SELECTED_ARMY)
        self.assertEqual(evt['time'], datetime.time(20, 46, 57))
        self.assertEqual(evt['callsign'], "User")
        self.assertEqual(evt['army'], "Red")
        self.assertPos(evt, 238667.0, 104506.0)

    def test_weapons_loaded(self):
        evt = parse_evt("[8:47:27 PM] User:Pe-8 loaded weapons '40fab100' fuel 40%")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_WEAPONS_LOADED)
        self.assertEqual(evt['time'], datetime.time(20, 47, 27))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['loadout'], "40fab100")
        self.assertEqual(evt['fuel'], 40)

    def test_seat_selected(self):
        evt = parse_evt("[8:47:27 PM] User:Pe-8(0) seat occupied by User at 238667.5 104125.0")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_SEAT_OCCUPIED)
        self.assertEqual(evt['time'], datetime.time(20, 47, 27))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['seat'], 0)
        self.assertPos(evt, 238667.5, 104125.0)

    def test_bailed_out(self):
        evt = parse_evt("[9:31:20 PM] User:Pe-8(0) bailed out at 149880.23 105703.76")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_BAILED_OUT)
        self.assertEqual(evt['time'], datetime.time(21, 31, 20))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['seat'], 0)
        self.assertPos(evt, 149880.23, 105703.76)

    def test_successfully_bailed_out(self):
        evt = parse_evt("[9:33:20 PM] User:Pe-8(0) successfully bailed out at 148534.2 105877.93")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_SUCCESSFULLY_BAILED_OUT)
        self.assertEqual(evt['time'], datetime.time(21, 33, 20))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['seat'], 0)
        self.assertPos(evt, 148534.2, 105877.93)

    def test_toggle_landing_lights(self):
        evt = parse_evt("[8:47:45 PM] User:Pe-8 turned landing lights on at 238667.52 104125.04")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_TOGGLE_LANDING_LIGHTS)
        self.assertEqual(evt['time'], datetime.time(20, 47, 45))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['value'], True)
        self.assertPos(evt, 238667.52, 104125.04)

        evt = parse_evt("[8:47:47 PM] User:Pe-8 turned landing lights off at 238667.52 104125.04")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_TOGGLE_LANDING_LIGHTS)
        self.assertEqual(evt['time'], datetime.time(20, 47, 47))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['value'], False)
        self.assertPos(evt, 238667.52, 104125.04)

    def test_toggle_wingtip_smokes(self):
        evt = parse_evt("[9:09:39 PM] User:Pe-8 turned wingtip smokes on at 208420.42 103602.61")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_TOGGLE_WINGTIP_SMOKES)
        self.assertEqual(evt['time'], datetime.time(21, 9, 39))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['value'], True)
        self.assertPos(evt, 208420.42, 103602.61)

        evt = parse_evt("[9:09:42 PM] User:Pe-8 turned wingtip smokes off at 208370.92 103669.64")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_TOGGLE_WINGTIP_SMOKES)
        self.assertEqual(evt['time'], datetime.time(21, 9, 42))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['value'], False)
        self.assertPos(evt, 208370.92, 103669.64)

    def test_took_off(self):
        evt = parse_evt("[9:09:56 PM] User:Pe-8 in flight at 207635.0 104367.586")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_TOOK_OFF)
        self.assertEqual(evt['time'], datetime.time(21, 9, 56))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 207635.0, 104367.586)

    def test_wounded(self):
        evt = parse_evt("[9:49:14 PM] User:Bf-109G-6_Late(0) was wounded at 89172.44 123074.15")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_WOUNDED)
        self.assertEqual(evt['time'], datetime.time(21, 49, 14))
        self.assertCalsignAircraft(evt, "User", "Bf-109G-6_Late")
        self.assertEqual(evt['seat'], 0)
        self.assertPos(evt, 89172.44, 123074.15)

    def test_heavily_wounded(self):
        evt = parse_evt("[9:50:24 PM] User:Pe-8(7) was heavily wounded at 84521.69 123442.84")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_HEAVILY_WOUNDED)
        self.assertEqual(evt['time'], datetime.time(21, 50, 24))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['seat'], 7)
        self.assertPos(evt, 84521.69, 123442.84)

    def test_killed(self):
        evt = parse_evt("[9:54:03 PM] User:Pe-8(0) was killed at 209064.98 102002.914")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_KILLED)
        self.assertEqual(evt['time'], datetime.time(21, 54, 3))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['seat'], 0)
        self.assertPos(evt, 209064.98, 102002.914)

    def test_killed_by_user(self):
        evt = parse_evt("[9:48:18 PM] User1:Bf-109G-6_Late(0) was killed by User2:Pe-8 at 53694.484 140936.42")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_KILLED_BY_USER)
        self.assertEqual(evt['time'], datetime.time(21, 48, 18))
        self.assertCalsignAircraft(evt, "User1", "Bf-109G-6_Late")
        self.assertEqual(evt['seat'], 0)
        self.assertAttackingUser(evt, "User2", "Pe-8")
        self.assertPos(evt, 53694.484, 140936.42)

    def test_captured(self):
        evt = parse_evt("[9:53:17 PM] User:Pe-8(2) was captured at 48024.66 126228.92")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_CAPTURED)
        self.assertEqual(evt['time'], datetime.time(21, 53, 17))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['seat'], 2)
        self.assertPos(evt, 48024.66, 126228.92)

    def test_crashed(self):
        evt = parse_evt("[9:53:59 PM] User:Pe-8 crashed at 90787.76 119865.445")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_CRASHED)
        self.assertEqual(evt['time'], datetime.time(21, 53, 59))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 90787.76, 119865.445)

    def test_landed(self):
        evt = parse_evt("[10:22:57 PM] User:Pe-8 landed at 209123.62 102794.375")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_LANDED)
        self.assertEqual(evt['time'], datetime.time(22, 22, 57))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 209123.62, 102794.375)

    def test_destroyed_building(self):
        evt = parse_evt("[9:41:39 PM] 3do/Buildings/Industrial/FactoryHouse1_W/live.sim destroyed by User:Pe-8 at 48734.32 131787.66")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_DESTROYED_BLD)
        self.assertEqual(evt['time'], datetime.time(21, 41, 39))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['building'], "FactoryHouse1_W")
        self.assertPos(evt, 48734.32, 131787.66)

    def test_destroyed_tree(self):
        evt = parse_evt("[9:41:56 PM] 3do/Tree/Line_W/live.sim destroyed by User:Pe-8 at 47617.54 131795.72")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_DESTROYED_TREE)
        self.assertEqual(evt['time'], datetime.time(21, 41, 56))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['tree'], "Line_W")
        self.assertPos(evt, 47617.54, 131795.72)

    def test_destroyed_static(self):
        evt = parse_evt("[9:42:27 PM] 200_Static destroyed by User:Pe-8 at 46240.0 132810.0")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_DESTROYED_STATIC)
        self.assertEqual(evt['time'], datetime.time(21, 42, 27))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['static'], "200_Static")
        self.assertPos(evt, 46240.0, 132810.0)

    def test_destroyed_bridge(self):
        evt = parse_evt("[5:17:41 PM]  Bridge0 destroyed by User:Bf-110G-2 at 11108.0 47692.0")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_DESTROYED_BRIDGE)
        self.assertEqual(evt['time'], datetime.time(17, 17, 41))
        self.assertCalsignAircraft(evt, "User", "Bf-110G-2")
        self.assertEqual(evt['bridge'], "Bridge0")
        self.assertPos(evt, 11108.0, 47692.0)

    def test_damaged_on_the_ground(self):
        evt = parse_evt("[10:25:54 PM] User:Pe-8 damaged on the ground at 208571.47 103295.33")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_DAMAGED_ON_GROUND)
        self.assertEqual(evt['time'], datetime.time(22, 25, 54))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 208571.47, 103295.33)

    def test_damaged_by_user(self):
        evt = parse_evt("[10:25:32 PM] User1:Pe-8 damaged by User2:Bf-109G-6_Late at 208901.16 102836.57")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_DAMAGED_BY_USER)
        self.assertEqual(evt['time'], datetime.time(22, 25, 32))
        self.assertCalsignAircraft(evt, "User1", "Pe-8")
        self.assertAttackingUser(evt, "User2", "Bf-109G-6_Late")
        self.assertPos(evt, 208901.16, 102836.57)

    def test_damaged_self(self):
        evt = parse_evt("[10:26:24 PM] User:Pe-8 damaged by landscape at 207773.69 104716.07")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_DAMAGED_SELF)
        self.assertEqual(evt['time'], datetime.time(22, 26, 24))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 207773.69, 104716.07)

    def test_shot_down_by_user(self):
        evt = parse_evt("[9:31:51 PM] User1:Pe-8 shot down by User2:Pe-8 at 148687.02 105729.086")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_SHOT_DOWN_BY_USER)
        self.assertEqual(evt['time'], datetime.time(21, 31, 51))
        self.assertCalsignAircraft(evt, "User1", "Pe-8")
        self.assertAttackingUser(evt, "User2", "Pe-8")
        self.assertPos(evt, 148687.02, 105729.086)

    def test_shot_down_self(self):
        evt = parse_evt("[8:52:43 PM] User:Pe-8 shot down by landscape at 208531.81 103386.945")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_SHOT_DOWN_SELF)
        self.assertEqual(evt['time'], datetime.time(20, 52, 43))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertPos(evt, 208531.81, 103386.945)

    def test_shot_down_by_static(self):
        evt = parse_evt("[9:45:16 PM] User:Pe-8 shot down by 85_Static at 47626.78 126637.38")
        self.assertIsNotNone(evt)
        self.assertEqual(evt['type'], EVT_SHOT_DOWN_BY_STATIC)
        self.assertEqual(evt['time'], datetime.time(21, 45, 16))
        self.assertCalsignAircraft(evt, "User", "Pe-8")
        self.assertEqual(evt['static'], "85_Static")
        self.assertPos(evt, 47626.78, 126637.38)
