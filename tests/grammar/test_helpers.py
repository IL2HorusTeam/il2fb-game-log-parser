# -*- coding: utf-8 -*-

import datetime

from il2fb.commons.organization import Belligerents
from pyparsing import ParseException

from il2fb.parsers.events.constants import TargetEndStates
from il2fb.parsers.events.grammar.helpers import (
    aircraft, ai_aircraft_crew_member, belligerent, bridge, building, callsign,
    event_date_time, event_pos, event_time, human_aircraft,
    human_aircraft_actor, human_aircraft_aggressor, human_crew_member,
    seat_number, static, target_end_state, toggle_value, tree, by_himself,
)
from il2fb.parsers.events.grammar.primitives import space
from il2fb.parsers.events.structures import (
    Point2D, HumanAircraft, HumanCrewMember, AIAircraftCrewMember,
)

from ..base import BaseTestCase


class CommonGrammarTestCase(BaseTestCase):

    def test_event_time(self):
        result = event_time.parseString("[08:33:05 PM] ").time
        self.assertEqual(result, datetime.time(20, 33, 5))

    def test_event_date_time(self):
        result = event_date_time.parseString("[Oct 30, 2013 8:33:05 PM] ")

        self.assertEqual(result.date, datetime.date(2013, 10, 30))
        self.assertEqual(result.time, datetime.time(20, 33, 5))

    def test_event_pos(self):
        result = event_pos.parseString(" at 123.321 456.654").pos
        self.assertEqual(result, Point2D(123.321, 456.654))

    def test_callsign(self):
        for string in ["User0", " User0 ", ]:
            result = callsign.parseString(string).callsign
            self.assertEqual(result, "User0")

    def test_aircraft(self):
        result = aircraft.parseString("Pe-8").aircraft
        self.assertEqual(result, "Pe-8")

    def test_ai_aircraft_crew_member(self):
        result = ai_aircraft_crew_member.parseString("Pe-8(0)").actor
        self.assertEqual(result, AIAircraftCrewMember("Pe-8", 0))

    def test_human_aircraft(self):
        result = human_aircraft.parseString("User0:Pe-8")

        self.assertEqual(result.callsign, "User0")
        self.assertEqual(result.aircraft, "Pe-8")

    def test_human_aircraft_actor(self):
        result = human_aircraft_actor.parseString("User0:Pe-8").actor
        self.assertEqual(result, HumanAircraft("User0", "Pe-8"))

    def test_human_aircraft_aggressor(self):
        testee = human_aircraft_aggressor
        result = testee.parseString("User1:Bf-109G-6_Late").aggressor
        self.assertEqual(result, HumanAircraft("User1", "Bf-109G-6_Late"))

    def test_victim_and_aggressor(self):
        grammar = (
            human_aircraft_actor.setResultsName("victim")
            + space
            + human_aircraft_aggressor
        )
        result = grammar.parseString("User0:Pe-8 User1:Bf-109G-6_Late")

        self.assertEqual(result.victim,
                         HumanAircraft("User0", "Pe-8"))
        self.assertEqual(result.aggressor,
                         HumanAircraft("User1", "Bf-109G-6_Late"))

    def test_seat_number(self):
        result = seat_number.parseString("(0)").seat_number
        self.assertEqual(result, 0)

    def test_human_crew_member(self):
        result = human_crew_member.parseString("User:Pe-8(0)").actor
        self.assertEqual(result, HumanCrewMember("User", "Pe-8", 0))

    def test_static(self):
        result = static.parseString("0_Static").static
        self.assertEqual(result, "0_Static")

    def test_bridge(self):
        result = bridge.parseString("Bridge0").bridge
        self.assertEqual(result, "Bridge0")

    def test_building(self):
        string = "3do/Buildings/Finland/CenterHouse1_w/live.sim"
        result = building.parseString(string).building
        self.assertEqual(result, "Finland/CenterHouse1_w")

        string = "3do/Buildings/Russia/Piter/House3_W/live.sim"
        result = building.parseString(string).building
        self.assertEqual(result, "Russia/Piter/House3_W")

    def test_tree(self):
        try:
            tree.parseString("3do/Tree/Line_W/live.sim")
        except Exception as e:
            message = e.args[0] if e.args else ""
            self.fail("'tree' grammar raised a {0} unexpectedly: {1}"
                      .format(e.__class__.__name__, message))

    def test_by_himself(self):
        try:
            by_himself.parseString(" by landscape")
            by_himself.parseString(" by NONAME")
        except Exception as e:
            message = e.args[0] if e.args else ""
            self.fail("'by_himself' grammar raised a {0} unexpectedly: {1}"
                      .format(e.__class__.__name__, message))


class ToggleValueTestCase(BaseTestCase):

    def test_toggle_value_is_on(self):
        result = toggle_value.parseString("on").toggle_value
        self.assertEqual(result.value, True)

    def test_toggle_value_is_off(self):
        result = toggle_value.parseString("off").toggle_value
        self.assertEqual(result.value, False)

    def test_toggle_value_is_invalid(self):
        with self.assertRaises(ParseException):
            toggle_value.parseString("XXX")


class BelligerentTestCase(BaseTestCase):

    def test_belligerent_in_title_case(self):
        result = belligerent.parseString("Red").belligerent
        self.assertEqual(result, Belligerents.red)

    def test_belligerent_in_lower_case(self):
        result = belligerent.parseString("red").belligerent
        self.assertEqual(result, Belligerents.red)

    def test_belligerent_in_upper_case(self):
        result = belligerent.parseString("RED").belligerent
        self.assertEqual(result, Belligerents.red)


class TargetEndStateTestCase(BaseTestCase):

    def test_target_end_state_is_complete(self):
        result = target_end_state.parseString("Complete").target_end_state
        self.assertEqual(result, TargetEndStates.COMPLETE)

    def test_target_end_state_is_failed(self):
        result = target_end_state.parseString("Failed").target_end_state
        self.assertEqual(result, TargetEndStates.FAILED)

    def test_target_end_state_is_invalid(self):
        with self.assertRaises(ParseException):
            target_end_state.parseString("XXX")
