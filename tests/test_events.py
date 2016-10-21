# coding: utf-8

import datetime
import unittest

from il2fb.commons.organization import Belligerents
from il2fb.commons.spatial import Point2D

from il2fb.parsers.events import actors, events


class MissionIsPlayingTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MissionIsPlaying.from_s(
            "[Sep 15, 2013 8:33:05 PM] Mission: path/PH.mis is Playing"
        )
        self.assertIsInstance(event, events.MissionIsPlaying)
        self.assertEqual(event.date, datetime.date(2013, 9, 15))
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.mission, "path/PH.mis")

    def test_to_primitive(self):
        event = events.MissionIsPlaying(
            date=datetime.date(2013, 9, 15),
            time=datetime.time(20, 33, 5),
            mission="path/PH.mis",
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'date': "2013-09-15",
                'time': "20:33:05",
                'mission': "path/PH.mis",
                'name': "MissionIsPlaying",
                'verbose_name': "Mission is playing",
            }
        )


class MissionHasBegunTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MissionHasBegun.from_s("[8:33:05 PM] Mission BEGIN")
        self.assertIsInstance(event, events.MissionHasBegun)
        self.assertEqual(event.time, datetime.time(20, 33, 5))

    def test_to_primitive(self):
        event = events.MissionHasBegun(
            time=datetime.time(20, 33, 5),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'name': "MissionHasBegun",
                'verbose_name': "Mission has begun",
            }
        )


class MissionHasEndedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MissionHasEnded.from_s("[8:33:05 PM] Mission END")
        self.assertIsInstance(event, events.MissionHasEnded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))

    def test_to_primitive(self):
        event = events.MissionHasEnded(
            time=datetime.time(20, 33, 5),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'name': "MissionHasEnded",
                'verbose_name': "Mission has ended",
            }
        )


class MissionWasWonTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MissionWasWon.from_s(
            "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"
        )
        self.assertIsInstance(event, events.MissionWasWon)
        self.assertEqual(event.date, datetime.date(2013, 9, 15))
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.belligerent, Belligerents.red)

    def test_to_primitive(self):
        event = events.MissionWasWon(
            date=datetime.date(2013, 9, 15),
            time=datetime.time(20, 33, 5),
            belligerent=Belligerents.red,
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'date': "2013-09-15",
                'time': "20:33:05",
                'belligerent': {
                    'value': 1,
                    'name': 'red',
                    'verbose_name': "allies",
                    'help_text': None,
                },
                'name': "MissionWasWon",
                'verbose_name': "Mission was won",
            }
        )


class TargetStateWasChangedTestCase(unittest.TestCase):

    def test_from_s_complete(self):
        event = events.TargetStateWasChanged.from_s(
            "[8:33:05 PM] Target 3 Complete"
        )
        self.assertIsInstance(event, events.TargetStateWasChanged)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.target_index, 3)
        self.assertEqual(
            event.state,
            events.TargetStateWasChanged.STATES.COMPLETE,
        )

    def test_from_s_failed(self):
        event = events.TargetStateWasChanged.from_s(
            "[8:33:05 PM] Target 3 Failed"
        )
        self.assertIsInstance(event, events.TargetStateWasChanged)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.target_index, 3)
        self.assertEqual(
            event.state,
            events.TargetStateWasChanged.STATES.FAILED,
        )

    def test_to_primitive_complete(self):
        event = events.TargetStateWasChanged(
            time=datetime.time(20, 33, 5),
            target_index=3,
            state=events.TargetStateWasChanged.STATES.COMPLETE,
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'target_index': 3,
                'state': 'Complete',
                'name': "TargetStateWasChanged",
                'verbose_name': "Target state was changed",
            }
        )

    def test_to_primitive_failed(self):
        event = events.TargetStateWasChanged(
            time=datetime.time(20, 33, 5),
            target_index=3,
            state=events.TargetStateWasChanged.STATES.FAILED,
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'target_index': 3,
                'state': 'Failed',
                'name': "TargetStateWasChanged",
                'verbose_name': "Target state was changed",
            }
        )


class HumanHasConnectedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanHasConnected.from_s(
            "[8:33:05 PM] User0 has connected"
        )
        self.assertIsInstance(event, events.HumanHasConnected)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")

    def test_to_primitive(self):
        event = events.HumanHasConnected(
            time=datetime.time(20, 33, 5),
            callsign="User0",
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'callsign': "User0",
                'name': "HumanHasConnected",
                'verbose_name': "Human has connected",
            }
        )


class HumanHasDisconnectedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanHasDisconnected.from_s(
            "[8:33:05 PM] User0 has disconnected"
        )
        self.assertIsInstance(event, events.HumanHasDisconnected)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")

    def test_to_primitive(self):
        event = events.HumanHasDisconnected(
            time=datetime.time(20, 33, 5),
            callsign="User0",
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'callsign': "User0",
                'name': "HumanHasDisconnected",
                'verbose_name': "Human has disconnected",
            }
        )


class HumanHasSelectedAirfieldTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanHasSelectedAirfield.from_s(
            "[8:33:05 PM] User0 selected army Red at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanHasSelectedAirfield)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.belligerent, Belligerents.red)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanHasSelectedAirfield(
            time=datetime.time(20, 33, 5),
            callsign="User0",
            belligerent=Belligerents.red,
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'callsign': "User0",
                'belligerent': {
                    'value': 1,
                    'name': 'red',
                    'verbose_name': "allies",
                    'help_text': None,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanHasSelectedAirfield",
                'verbose_name': "Human has selected airfield",
            }
        )


class HumanAircraftHasSpawnedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftHasSpawned.from_s(
            "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"
        )
        self.assertIsInstance(event, events.HumanAircraftHasSpawned)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.weapons, "40fab100")
        self.assertEqual(event.fuel, 40)

    def test_to_primitive(self):
        event = events.HumanAircraftHasSpawned(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            weapons="40fab100",
            fuel=40,
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'weapons': "40fab100",
                'fuel': 40,
                'name': "HumanAircraftHasSpawned",
                'verbose_name': "Human aircraft has spawned",
            }
        )


class HumanHasWentToBriefingTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanHasWentToBriefing.from_s(
            "[8:33:05 PM] User0 entered refly menu"
        )
        self.assertIsInstance(event, events.HumanHasWentToBriefing)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")

    def test_to_primitive(self):
        event = events.HumanHasWentToBriefing(
            time=datetime.time(20, 33, 5),
            callsign="User0",
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'callsign': "User0",
                'name': "HumanHasWentToBriefing",
                'verbose_name': "Human has went to briefing",
            }
        )


class HumanHasToggledLandingLightsTestCase(unittest.TestCase):

    def test_from_s_value_off(self):
        event = events.HumanHasToggledLandingLights.from_s(
            "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanHasToggledLandingLights)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.value, 'off')
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_from_s_value_on(self):
        event = events.HumanHasToggledLandingLights.from_s(
            "[8:33:05 PM] User0:Pe-8 turned landing lights on at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanHasToggledLandingLights)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.value, 'on')
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive_value_off(self):
        event = events.HumanHasToggledLandingLights(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            value='off',
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'value': 'off',
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanHasToggledLandingLights",
                'verbose_name': "Human has toggled landing lights",
            }
        )

    def test_to_primitive_value_on(self):
        event = events.HumanHasToggledLandingLights(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            value='on',
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'value': 'on',
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanHasToggledLandingLights",
                'verbose_name': "Human has toggled landing lights",
            }
        )


class HumanHasToggledWingtipSmokesTestCase(unittest.TestCase):

    def test_from_s_value_off(self):
        event = events.HumanHasToggledWingtipSmokes.from_s(
            "[8:33:05 PM] User0:Pe-8 turned wingtip smokes off at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanHasToggledWingtipSmokes)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.value, 'off')
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_from_s_value_on(self):
        event = events.HumanHasToggledWingtipSmokes.from_s(
            "[8:33:05 PM] User0:Pe-8 turned wingtip smokes on at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanHasToggledWingtipSmokes)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.value, 'on')
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive_value_off(self):
        event = events.HumanHasToggledWingtipSmokes(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            value='off',
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'value': 'off',
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanHasToggledWingtipSmokes",
                'verbose_name': "Human has toggled wingtip smokes",
            }
        )

    def test_to_primitive_value_on(self):
        event = events.HumanHasToggledWingtipSmokes(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            value='on',
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'value': 'on',
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanHasToggledWingtipSmokes",
                'verbose_name': "Human has toggled wingtip smokes",
            }
        )


class HumanHasChangedSeatTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanHasChangedSeat.from_s(
            "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanHasChangedSeat)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.actor,
            actors.HumanAircraftCrewMember("User0", "Pe-8", 0)
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanHasChangedSeat(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanHasChangedSeat",
                'verbose_name': "Human has changed seat",
            }
        )


class HumanAircraftHasTookOffTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftHasTookOff.from_s(
            "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftHasTookOff)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftHasTookOff(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftHasTookOff",
                'verbose_name': "Human aircraft has took off",
            }
        )


class HumanAircraftHasLandedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftHasLanded.from_s(
            "[8:33:05 PM] User0:Pe-8 landed at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftHasLanded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftHasLanded(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftHasLanded",
                'verbose_name': "Human aircraft has landed",
            }
        )


class HumanHasDamagedOwnAircraftTestCase(unittest.TestCase):

    def test_from_s_by_landscape(self):
        event = events.HumanHasDamagedOwnAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 damaged by landscape at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanHasDamagedOwnAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_from_s_by_noname(self):
        event = events.HumanHasDamagedOwnAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 damaged by NONAME at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanHasDamagedOwnAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanHasDamagedOwnAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanHasDamagedOwnAircraft",
                'verbose_name': "Human has damaged own aircraft",
            }
        )
