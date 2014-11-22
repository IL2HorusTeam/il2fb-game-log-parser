# -*- coding: utf-8 -*-
import re
import unittest

from il2fb.parsers.events.regex import *
from il2fb.parsers.events.regex import (
    RX_TIME_BASE, RX_TIME, RX_DATE_TIME,
    RX_CALLSIGN, RX_SEAT, RX_BRIDGE, RX_ARMY, RX_AIRCRAFT,
    RX_POS, RX_TOGGLE_VALUE, RX_STATIC, RX_ENEMY_CALLSIGN_AIRCRAFT,
    RX_TIME_CALLSIGN, RX_TIME_AIRCRAFT, RX_DESTROYED_BY,
)


class BaseTestCase(unittest.TestCase):

    def _compile_re(self, regex):
        return re.compile(regex, RX_FLAGS)

    def _assert_time_only(self, groupdict, expected_time):
        self.assertTrue(groupdict)
        self.assertEqual(groupdict['time'], expected_time)

    def _assert_datetime_only(self, groupdict, expected_data):
        self.assertTrue(groupdict)
        self.assertEqual(groupdict['date'], expected_data['date'])
        self.assertEqual(groupdict['time'], expected_data['time'])


class CommonsTestCase(BaseTestCase):

    def test_RX_TIME_BASE(self):
        rx = self._compile_re(RX_TIME_BASE)
        m = rx.search("[8:33:05 AM]")
        self.assertIsNotNone(m)
        self._assert_time_only(m.groupdict(), "8:33:05 AM")

    def test_time(self):
        rx = self._compile_re(RX_TIME)

        m = rx.match("[8:33:05 AM] ")
        self.assertIsNotNone(m)
        self._assert_time_only(m.groupdict(), "8:33:05 AM")

        m = rx.match("[8:33:05 AM] foo")
        self.assertIsNotNone(m)
        self._assert_time_only(m.groupdict(), "8:33:05 AM")

        m = rx.match("[8:33:05 PM] ")
        self.assertIsNotNone(m)
        self._assert_time_only(m.groupdict(), "8:33:05 PM")

        m = rx.match("[10:33:05 PM] ")
        self.assertIsNotNone(m)
        self._assert_time_only(m.groupdict(), "10:33:05 PM")

    def test_date_time(self):
        rx = self._compile_re(RX_DATE_TIME)

        m = rx.match("[Sep 15, 2013 8:33:05 PM] ")
        self.assertIsNotNone(m)
        self._assert_datetime_only(m.groupdict(), {
            'date': "Sep 15, 2013",
            'time': "8:33:05 PM",
        })

        m = rx.match("[Sep 7, 2013 10:33:05 AM] ")
        self.assertIsNotNone(m)
        self._assert_datetime_only(m.groupdict(), {
            'date': "Sep 7, 2013",
            'time': "10:33:05 AM",
        })

    def test_pos(self):
        rx = self._compile_re(RX_POS)
        m = rx.search("foo bar started buzzing at 100.0 200.99")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'pos_x': "100.0",
            'pos_y': "200.99"
        })

    def test_callsign(self):
        rx = self._compile_re(RX_CALLSIGN)
        m = rx.search("    User   ")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['callsign'], "User")

    def test_time_callsign(self):
        rx = self._compile_re(RX_TIME_CALLSIGN)
        m = rx.search("[8:33:05 AM] User ")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'time': "8:33:05 AM",
            'callsign': "User"
        })

    def test_time_aircraft(self):
        rx = self._compile_re(RX_TIME_AIRCRAFT)
        m = rx.search("[8:33:05 AM] User:Pe-8  ")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'time': "8:33:05 AM",
            'callsign': "User",
            'aircraft': "Pe-8",
        })

    def test_seat(self):
        rx = self._compile_re(RX_SEAT)
        m = rx.search("User(0) bailed out")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['seat'], "0")

    def test_aircraft(self):
        rx = self._compile_re(RX_AIRCRAFT)
        m = rx.search("User:Pe-8")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['aircraft'], "Pe-8")

    def test_enemy_callsign_aircraft(self):
        rx = self._compile_re(RX_ENEMY_CALLSIGN_AIRCRAFT)
        m = rx.search("  User:Pe-8  ")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'e_callsign': "User",
            'e_aircraft': "Pe-8",
        })

    def test_static(self):
        rx = self._compile_re(RX_STATIC)
        m = rx.search(" 200_Static destroyed")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['static'], "200_Static")

    def test_bridge(self):
        rx = self._compile_re(RX_BRIDGE)
        m = rx.search(" Bridge0 destroyed")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['bridge'], "Bridge0")

    def test_army(self):
        rx = self._compile_re(RX_ARMY)

        m = rx.search(" Red ")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['army'], "Red")

        m = rx.search(" RED ")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['army'], "RED")

        m = rx.search(" Blue ")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['army'], "Blue")

        m = rx.search(" BLUE ")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['army'], "BLUE")

    def test_toggle_value(self):
        rx = self._compile_re(RX_TOGGLE_VALUE)

        m = rx.search("turned landing lights on at ")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['value'], "on")

        m = rx.search("turned landing lights off at ")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['value'], "off")

    def test_destroyed_by(self):
        rx = self._compile_re(RX_DESTROYED_BY)
        m = rx.search("something destroyed by User:Pe-8 at 100.0 200.99")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'callsign': "User",
            'aircraft': "Pe-8",
            'pos_x': "100.0",
            'pos_y': "200.99",
        })


class MissionFlowTestCase(BaseTestCase):

    def test_mission_playing(self):
        rx = self._compile_re(RX_MISSION_PLAYING)

        m = rx.match("[Sep 15, 2013 8:33:08 PM] Mission: Helsinky.mis is Playing")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'date': "Sep 15, 2013",
            'time': "8:33:08 PM",
            'mission': "Helsinky.mis",
        })

        m = rx.match("[Sep 15, 2013 8:33:08 PM] Mission: test\Helsinky.mis is Playing")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict()['mission'], "test\Helsinky.mis")

    def test_mission_begin(self):
        rx = self._compile_re(RX_MISSION_BEGIN)
        m = rx.match("[8:33:05 AM] Mission BEGIN")
        self.assertIsNotNone(m)
        self._assert_time_only(m.groupdict(), "8:33:05 AM")

    def test_mission_end(self):
        rx = self._compile_re(RX_MISSION_END)
        m = rx.match("[8:33:05 AM] Mission END")
        self.assertIsNotNone(m)
        self._assert_time_only(m.groupdict(), "8:33:05 AM")

    def test_mission_won(self):
        rx = self._compile_re(RX_MISSION_WON)
        m = rx.match("[Dec 29, 2012 5:19:49 PM] Mission: RED WON")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'date': "Dec 29, 2012",
            'time': "5:19:49 PM",
            'army': "RED",
        })

    def test_target_result(self):
        rx = self._compile_re(RX_TARGET_RESULT)

        m = rx.match("[5:15:22 PM] Target 3 Complete")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'time': "5:15:22 PM",
            'number': "3",
            'result': "Complete",
        })

        m = rx.match("[5:19:49 PM] Target 5 Failed")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'time': "5:19:49 PM",
            'number': "5",
            'result': "Failed",
        })


class ActionsTestCase(BaseTestCase):

    def _assert_toggle_value(self, groupdict, value, expected_data={}):
        self._assert_time_aircraft_pos(groupdict, expected_data)
        self.assertEqual(groupdict['value'], value)

    def _assert_time_seat_pos(self, groupdict, expected_data={}):
        self._assert_time_aircraft_pos(groupdict, expected_data)
        self.assertEqual(groupdict['seat'], expected_data.get('seat', "0"))

    def _assert_time_aircraft_under_eair_attack_pos(self, groupdict, expected_data={}):
        expected_data = expected_data or {
            'time': "8:49:39 PM",
            'callsign': "User1",
            'aircraft': "Pe-8",
            'e_callsign': "User2",
            'e_aircraft': "Bf-109G-6_Late",
            'pos_x': "100.0",
            'pos_y': "200.99",
        }
        self._assert_time_aircraft_pos(groupdict, expected_data)
        self.assertEqual(
            groupdict['e_callsign'], expected_data['e_callsign'])
        self.assertEqual(
            groupdict['e_aircraft'], expected_data['e_aircraft'])

    def _assert_time_aircraft_under_static_attack_pos(self, groupdict, expected_data={}):
        self._assert_time_aircraft_pos(groupdict, expected_data)
        self.assertEqual(
            groupdict['static'], expected_data.get('static', "0_Static"))

    def _assert_time_aircraft_pos(self, groupdict, expected_data={}):
        self.assertTrue(groupdict)
        expected_data = expected_data or {
            'time': "8:49:39 PM",
            'callsign': "User",
            'aircraft': "Pe-8",
            'pos_x': "100.0",
            'pos_y': "200.99",
        }
        self.assertEqual(groupdict['time'], expected_data['time'])
        self.assertEqual(groupdict['callsign'], expected_data['callsign'])
        self.assertEqual(groupdict['aircraft'], expected_data['aircraft'])
        self.assertEqual(groupdict['pos_x'], expected_data['pos_x'])
        self.assertEqual(groupdict['pos_y'], expected_data['pos_y'])

    def test_connected(self):
        rx = self._compile_re(RX_CONNECTED)
        m = rx.match("[8:45:57 PM] User has connected")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'time': "8:45:57 PM",
            'callsign': "User",
        })

    def test_disconnected(self):
        rx = self._compile_re(RX_DISCONNECTED)
        m = rx.match("[8:46:37 PM] User has disconnected")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'time': "8:46:37 PM",
            'callsign': "User",
        })

    def test_went_to_menu(self):
        rx = self._compile_re(RX_WENT_TO_MENU)
        m = rx.match("[8:49:20 PM] User entered refly menu")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'time': "8:49:20 PM",
            'callsign': "User",
        })

    def test_selected_army(self):
        rx = self._compile_re(RX_SELECTED_ARMY)
        m = rx.match("[8:46:55 PM] User selected army Red at 100.0 200.99")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'time': "8:46:55 PM",
            'callsign': "User",
            'army': "Red",
            'pos_x': "100.0",
            'pos_y': "200.99",
        })

    def test_took_off(self):
        rx = self._compile_re(RX_TOOK_OFF)
        m = rx.match("[8:49:32 PM] User:Pe-8 in flight at 100.0 200.99")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'time': "8:49:32 PM",
            'callsign': "User",
            'aircraft': "Pe-8",
            'pos_x': "100.0",
            'pos_y': "200.99",
        })

    def test_weapons_loaded(self):
        rx = self._compile_re(RX_WEAPONS_LOADED)
        m = rx.match("[8:49:35 PM] User:Pe-8 loaded weapons '40fab100' fuel 40%")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'time': "8:49:35 PM",
            'callsign': "User",
            'aircraft': "Pe-8",
            'loadout': "40fab100",
            'fuel': "40",
        })

    def test_seat_occupied(self):
        rx = self._compile_re(RX_SEAT_OCCUPIED)
        m = rx.match("[8:49:39 PM] User:Pe-8(0) seat occupied by User at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_seat_pos(m.groupdict())

    def test_bailed_out(self):
        rx = self._compile_re(RX_BAILED_OUT)
        m = rx.match("[8:49:39 PM] User:Pe-8(0) bailed out at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_seat_pos(m.groupdict())

    def test_successfully_bailed_out(self):
        rx = self._compile_re(RX_SUCCESSFULLY_BAILED_OUT)
        m = rx.match("[8:49:39 PM] User:Pe-8(0) successfully bailed out at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_seat_pos(m.groupdict())

    def test_toggle_landing_lights(self):
        rx = self._compile_re(RX_TOGGLE_LANDING_LIGHTS)

        m = rx.match("[8:49:39 PM] User:Pe-8 turned landing lights on at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_toggle_value(m.groupdict(), "on")

        m = rx.match("[8:49:39 PM] User:Pe-8 turned landing lights off at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_toggle_value(m.groupdict(), "off")

    def test_toggle_wingtip_smokes(self):
        rx = self._compile_re(RX_TOGGLE_WINGTIP_SMOKES)

        m = rx.match("[8:49:39 PM] User:Pe-8 turned wingtip smokes on at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_toggle_value(m.groupdict(), "on")

        m = rx.match("[8:49:39 PM] User:Pe-8 turned wingtip smokes off at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_toggle_value(m.groupdict(), "off")

    def test_wounded(self):
        rx = self._compile_re(RX_WOUNDED)
        m = rx.match("[8:49:39 PM] User:Pe-8(0) was wounded at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_seat_pos(m.groupdict())

    def test_heavily_wounded(self):
        rx = self._compile_re(RX_HEAVILY_WOUNDED)
        m = rx.match("[8:49:39 PM] User:Pe-8(0) was heavily wounded at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_seat_pos(m.groupdict())

    def test_killed(self):
        rx = self._compile_re(RX_KILLED)
        m = rx.match("[8:49:39 PM] User:Pe-8(0) was killed at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_seat_pos(m.groupdict())

    def test_killed_by_user(self):
        rx = self._compile_re(RX_KILLED_BY_USER)
        m = rx.match("[8:49:39 PM] User1:Pe-8(0) was killed by User2:Bf-109G-6_Late at 100.0 200.99")
        self.assertIsNotNone(m)
        self.assertEqual(m.groupdict(), {
            'time': "8:49:39 PM",
            'callsign': "User1",
            'aircraft': "Pe-8",
            'seat': "0",
            'e_callsign': "User2",
            'e_aircraft': "Bf-109G-6_Late",
            'pos_x': "100.0",
            'pos_y': "200.99",
        })

    def test_captured(self):
        rx = self._compile_re(RX_CAPTURED)
        m = rx.match("[8:49:39 PM] User:Pe-8(0) was captured at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_seat_pos(m.groupdict())

    def test_crashed(self):
        rx = self._compile_re(RX_CRASHED)
        m = rx.match("[8:49:39 PM] User:Pe-8 crashed at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_aircraft_pos(m.groupdict())

    def test_landed(self):
        rx = self._compile_re(RX_LANDED)
        m = rx.match("[8:49:39 PM] User:Pe-8 landed at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_aircraft_pos(m.groupdict())

    def test_damaged_on_the_ground(self):
        rx = self._compile_re(RX_DAMAGED_ON_GROUND)
        m = rx.match("[8:49:39 PM] User:Pe-8 damaged on the ground at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_aircraft_pos(m.groupdict())

    def test_damaged_self(self):
        rx = self._compile_re(RX_DAMAGED_SELF)
        m = rx.match("[8:49:39 PM] User:Pe-8 damaged by landscape at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_aircraft_pos(m.groupdict())

    def test_damaged_by_user(self):
        rx = self._compile_re(RX_DAMAGED_BY_USER)
        m = rx.match("[8:49:39 PM] User1:Pe-8 damaged by User2:Bf-109G-6_Late at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_aircraft_under_eair_attack_pos(m.groupdict())

    def test_shot_down_self(self):
        rx = self._compile_re(RX_SHOT_DOWN_SELF)
        m = rx.match("[8:49:39 PM] User:Pe-8 shot down by landscape at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_aircraft_pos(m.groupdict())

    def test_shot_down_by_user(self):
        rx = self._compile_re(RX_SHOT_DOWN_BY_USER)
        m = rx.match("[8:49:39 PM] User1:Pe-8 shot down by User2:Bf-109G-6_Late at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_aircraft_under_eair_attack_pos(m.groupdict())

    def test_shot_down_by_static(self):
        rx = self._compile_re(RX_SHOT_DOWN_BY_STATIC)
        m = rx.match("[8:49:39 PM] User:Pe-8 shot down by 0_Static at 100.0 200.99")
        self.assertIsNotNone(m)
        self._assert_time_aircraft_under_static_attack_pos(m.groupdict())

    def test_destroyed_building(self):
        rx = self._compile_re(RX_DESTROYED_BLD)
        m = rx.match("[8:49:39 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by User:Pe-8 at 100.0 200.99")
        self.assertIsNotNone(m)
        d = m.groupdict()
        self._assert_time_aircraft_pos(d)
        self.assertEqual(d['building'], "CenterHouse1_w")

    def test_destroyed_tree(self):
        rx = self._compile_re(RX_DESTROYED_TREE)
        m = rx.match("[8:49:39 PM] 3do/Tree/Line_W/live.sim destroyed by User:Pe-8 at 100.0 200.99")
        self.assertIsNotNone(m)
        d = m.groupdict()
        self._assert_time_aircraft_pos(d)
        self.assertEqual(d['tree'], "Line_W")

    def test_destroyed_static(self):
        rx = self._compile_re(RX_DESTROYED_STATIC)
        m = rx.match("[8:49:39 PM] 0_Static destroyed by User:Pe-8 at 100.0 200.99")
        self.assertIsNotNone(m)
        d = m.groupdict()
        self._assert_time_aircraft_pos(d)
        self.assertEqual(d['static'], "0_Static")

    def test_destroyed_bridge(self):
        rx = self._compile_re(RX_DESTROYED_BRIDGE)
        m = rx.match("[8:49:39 PM]  Bridge0 destroyed by User:Pe-8 at 100.0 200.99")
        self.assertIsNotNone(m)
        d = m.groupdict()
        self._assert_time_aircraft_pos(d)
        self.assertEqual(d['bridge'], "Bridge0")