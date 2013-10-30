# -*- coding: utf-8 -*-

import datetime
import unittest

from il2ds_log_parser.content_processor import *


class EventProcessorTestCase(unittest.TestCase):

    def test_process_time(self):
        data = {'time': "8:10:12 PM", }
        process_time(data)
        self.assertEqual(data['time'], datetime.time(20, 10, 12))

    def test_process_date(self):
        data = {'date': "Oct 30, 2013", }
        process_date(data)
        self.assertEqual(data['date'], datetime.date(2013, 10, 30))

    def test_process_number(self):
        data = {'number': "1", }
        process_number(data)
        self.assertEqual(data['number'], 1)

    def test_process_target_result(self):
        data = {'result': "Complete", }
        process_target_result(data)
        self.assertTrue(data['result'])

        data = {'result': "Failed", }
        process_target_result(data)
        self.assertFalse(data['result'])

        data = {'result': "fake", }
        with self.assertRaises(ValueError) as ctx:
            process_target_result(data)

        self.assertEqual(
            ctx.exception.message,
            "Target result value 'fake' is invalid. "
            "Valid values: Complete, Failed.")

    def test_process_fuel(self):
        data = {'fuel': "50", }
        process_fuel(data)
        self.assertEqual(data['fuel'], 50)

    def test_process_position(self):
        data = {
            'pos_x': "50.0",
            'pos_y': "-0.99999",
        }
        process_position(data)
        pos = data.get('pos')
        self.assertIsInstance(pos, dict)
        self.assertEqual(pos.get('x'), 50)
        self.assertEqual(pos.get('y'), -0.99999)

    def test_process_toggle_value(self):
        data = {'value': "on", }
        process_toggle_value(data)
        self.assertTrue(data['value'])

        data = {'value': "off", }
        process_toggle_value(data)
        self.assertFalse(data['value'])

        data = {'value': "fake", }
        with self.assertRaises(ValueError) as ctx:
            process_toggle_value(data)

        self.assertEqual(
            ctx.exception.message,
            "Toggle value 'fake' is invalid. Valid values: on, off.")

    def test_process_seat(self):
        data = {'seat': "0", }
        process_seat(data)
        self.assertEqual(data['seat'], 0)

    def test_process_attacking_user(self):
        data = {
            'e_callsign': "User",
            'e_aircraft': "Ubercraft",
        }
        process_attacking_user(data)
        attacker = data.get('attacker')
        self.assertIsInstance(attacker, dict)
        self.assertEqual(attacker.get('callsign'), "User")
        self.assertEqual(attacker.get('aircraft'), "Ubercraft")

    def test_process_army(self):
        datas = [
            {'army': "Red", },
            {'army': "RED", },
            {'army': "red", },
            {'army': "rEd", },
        ]
        for data in datas:
            process_army(data)
            self.assertEqual(data['army'], "Red")
