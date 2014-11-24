# -*- coding: utf-8 -*-

import datetime

from pyparsing import ParseException

from il2fb.commons.organization import Belligerents

from il2fb.parsers.events.constants import TOGGLE_VALUES, EVENT_TYPES
from il2fb.parsers.events.grammar import (
    space, day_period, time, event_time, date, date_time, event_date_time,
    float_number, event_pos, toggle_value, callsign, aircraft, pilot, enemy,
    seat_number, crew_member, static, bridge, belligerent, destroyed_by,
    mission_playing, mission_begin, mission_end,
)
from il2fb.parsers.events.structures import Point2D

from .base import BaseTestCase


class CommonGrammarTestCase(BaseTestCase):

    def test_day_period(self):
        self.assertEqual(day_period.parseString("AM").day_period, "AM")
        self.assertEqual(day_period.parseString("PM").day_period, "PM")

        with self.assertRaises(ParseException):
            day_period.parseString("ZZ")

    def test_time(self):
        expected = datetime.time(20, 33, 5)

        self.assertEqual(time.parseString("8:33:05 PM").time, expected)
        self.assertEqual(time.parseString("08:33:05 PM").time, expected)

    def test_event_time(self):
        result = event_time.parseString("[08:33:05 PM] ").time
        self.assertEqual(result, datetime.time(20, 33, 5))

    def test_date(self):
        result = date.parseString("Oct 30, 2013").date
        self.assertEqual(result, datetime.date(2013, 10, 30))

    def test_date_time(self):
        result = date_time.parseString("Oct 30, 2013 8:33:05 PM")

        self.assertEqual(result.date, datetime.date(2013, 10, 30))
        self.assertEqual(result.time, datetime.time(20, 33, 5))

    def test_event_date_time(self):
        result = event_date_time.parseString("[Oct 30, 2013 8:33:05 PM] ")

        self.assertEqual(result.date, datetime.date(2013, 10, 30))
        self.assertEqual(result.time, datetime.time(20, 33, 5))

    def test_float_number(self):
        result = float_number.parseString("123.321")
        self.assertEqual(result[0], 123.321)

        result = float_number.parseString("-456.654")
        self.assertEqual(result[0], -456.654)

    def test_event_pos(self):
        result = event_pos.parseString(" at 123.321 456.654").pos
        self.assertEqual(result, Point2D(123.321, 456.654))

    def test_toggle_value(self):
        self.assertEqual(
            toggle_value.parseString("on").toggle_value,
            TOGGLE_VALUES.ON)
        self.assertEqual(
            toggle_value.parseString("off").toggle_value,
            TOGGLE_VALUES.OFF)

        with self.assertRaises(ParseException):
            toggle_value.parseString("XXX")

    def test_callsign(self):
        for string in ["User0", " User0 ", ]:
            result = callsign.parseString(string).callsign
            self.assertEqual(result, "User0")

    def test_aircraft(self):
        result = aircraft.parseString("Pe-8").aircraft
        self.assertEqual(result, "Pe-8")

    def test_pilot(self):
        result = pilot.parseString("User0:Pe-8").pilot

        self.assertEqual(result.callsign, "User0")
        self.assertEqual(result.aircraft, "Pe-8")

    def test_enemy(self):
        result = enemy.parseString("User1:Bf-109G-6_Late").enemy

        self.assertEqual(result.callsign, "User1")
        self.assertEqual(result.aircraft, "Bf-109G-6_Late")

    def test_victim_and_offender(self):
        grammar = pilot + space + enemy
        result = grammar.parseString("User0:Pe-8 User1:Bf-109G-6_Late")

        victim = result.pilot
        self.assertEqual(victim.callsign, "User0")
        self.assertEqual(victim.aircraft, "Pe-8")

        offender = result.enemy
        self.assertEqual(offender.callsign, "User1")
        self.assertEqual(offender.aircraft, "Bf-109G-6_Late")

    def test_seat_number(self):
        result = seat_number.parseString("(0)").seat_number
        self.assertEqual(result, 0)

    def test_crew_member(self):
        result = crew_member.parseString("User:Pe-8(0)")

        self.assertEqual(result.callsign, "User")
        self.assertEqual(result.aircraft, "Pe-8")
        self.assertEqual(result.seat_number, 0)

    def test_static(self):
        result = static.parseString("0_Static").static
        self.assertEqual(result, "0_Static")

    def test_bridge(self):
        result = bridge.parseString("Bridge0").bridge
        self.assertEqual(result, "Bridge0")

    def test_belligerent(self):
        result = belligerent.parseString("Red").belligerent
        self.assertEqual(result, Belligerents.red)

    def test_destroyed_by(self):
        string = " destroyed by User:Pe-8 at 100.0 200.99"
        result = destroyed_by.parseString(string)

        self.assertEqual(result.callsign, "User")
        self.assertEqual(result.aircraft, "Pe-8")
        self.assertEqual(result.pos, Point2D(100.0, 200.99))


class EventsGrammarTestCase(BaseTestCase):

    def test_mission_playing(self):
        string = "[Sep 15, 2013 8:33:05 PM] Mission: path/PH.mis is Playing"
        result = mission_playing.parseString(string).event

        self.assertEqual(result.type, EVENT_TYPES.MISSION_PLAYING)
        self.assertEqual(result.date, datetime.date(2013, 9, 15))
        self.assertEqual(result.time, datetime.time(20, 33, 5))
        self.assertEqual(result.mission, "path/PH.mis")

    def test_mission_begin(self):
        string = "[8:33:05 PM] Mission BEGIN"
        result = mission_begin.parseString(string).event

        self.assertEqual(result.type, EVENT_TYPES.MISSION_BEGIN)
        self.assertEqual(result.time, datetime.time(20, 33, 5))

    def test_mission_end(self):
        string = "[8:33:05 PM] Mission END"
        result = mission_end.parseString(string).event

        self.assertEqual(result.type, EVENT_TYPES.MISSION_END)
        self.assertEqual(result.time, datetime.time(20, 33, 5))
