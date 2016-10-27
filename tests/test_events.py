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
        self.assertEqual(event.index, 3)
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
        self.assertEqual(event.index, 3)
        self.assertEqual(
            event.state,
            events.TargetStateWasChanged.STATES.FAILED,
        )

    def test_to_primitive_complete(self):
        event = events.TargetStateWasChanged(
            time=datetime.time(20, 33, 5),
            index=3,
            state=events.TargetStateWasChanged.STATES.COMPLETE,
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'index': 3,
                'state': 'Complete',
                'name': "TargetStateWasChanged",
                'verbose_name': "Target state was changed",
            }
        )

    def test_to_primitive_failed(self):
        event = events.TargetStateWasChanged(
            time=datetime.time(20, 33, 5),
            index=3,
            state=events.TargetStateWasChanged.STATES.FAILED,
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'index': 3,
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
        self.assertEqual(event.actor, actors.Human("User0"))

    def test_to_primitive(self):
        event = events.HumanHasConnected(
            time=datetime.time(20, 33, 5),
            actor=actors.Human("User0"),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                },
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
        self.assertEqual(event.actor, actors.Human("User0"))

    def test_to_primitive(self):
        event = events.HumanHasDisconnected(
            time=datetime.time(20, 33, 5),
            actor=actors.Human("User0"),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                },
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
        self.assertEqual(event.actor, actors.Human("User0"))
        self.assertEqual(event.belligerent, Belligerents.red)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanHasSelectedAirfield(
            time=datetime.time(20, 33, 5),
            actor=actors.Human("User0"),
            belligerent=Belligerents.red,
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                },
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
        self.assertEqual(event.actor, actors.Human("User0"))

    def test_to_primitive(self):
        event = events.HumanHasWentToBriefing(
            time=datetime.time(20, 33, 5),
            actor=actors.Human("User0"),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                },
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
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanHasChangedSeat",
                'verbose_name': "Human has changed seat",
            }
        )


class HumanIsTryingToTakeSeatTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanIsTryingToTakeSeat.from_s(
            "[8:33:05 PM] User0 is trying to occupy seat USN_VF_51A020(0)"
        )
        self.assertIsInstance(event, events.HumanIsTryingToTakeSeat)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.Human("User0"))
        self.assertEqual(event.seat, actors.AIAircraftCrewMember("USN_VF_51A02", 0, 0))

    def test_to_primitive(self):
        event = events.HumanIsTryingToTakeSeat(
            time=datetime.time(20, 33, 5),
            actor=actors.Human("User0"),
            seat=actors.AIAircraftCrewMember("USN_VF_51A02", 0, 0),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                },
                'seat': {
                    'flight': "USN_VF_51A02",
                    'aircraft': 0,
                    'index': 0,
                },
                'name': "HumanIsTryingToTakeSeat",
                'verbose_name': "Human is trying to take seat",
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


class HumanAircraftHasCrashedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftHasCrashed.from_s(
            "[8:33:05 PM] User0:Pe-8 crashed at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftHasCrashed)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftHasCrashed(
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
                'name': "HumanAircraftHasCrashed",
                'verbose_name': "Human aircraft has crashed",
            }
        )


class HumanHasDestroyedOwnAircraftTestCase(unittest.TestCase):

    def test_from_s_by_landscape(self):
        event = events.HumanHasDestroyedOwnAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 shot down by landscape at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanHasDestroyedOwnAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_from_s_by_noname(self):
        event = events.HumanHasDestroyedOwnAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 shot down by NONAME at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanHasDestroyedOwnAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanHasDestroyedOwnAircraft(
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
                'name': "HumanHasDestroyedOwnAircraft",
                'verbose_name': "Human has destroyed own aircraft",
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


class HumanAircraftWasDamagedOnGroundTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasDamagedOnGround.from_s(
            "[8:33:05 PM] User0:Pe-8 damaged on the ground at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasDamagedOnGround)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasDamagedOnGround(
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
                'name': "HumanAircraftWasDamagedOnGround",
                'verbose_name': "Human aircraft was damaged on the ground",
            }
        )


class HumanAircraftWasDamagedByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasDamagedByHumanAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 damaged by User1:Bf-109G-6_Late at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasDamagedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.actor,
            actors.HumanAircraft("User0", "Pe-8")
        )
        self.assertEqual(
            event.attacker,
            actors.HumanAircraft("User1", "Bf-109G-6_Late")
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasDamagedByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.HumanAircraft("User1", "Bf-109G-6_Late"),
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
                'attacker': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-6_Late",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasDamagedByHumanAircraft",
                'verbose_name': "Human aircraft was damaged by human aircraft",
            }
        )


class HumanAircraftWasDamagedByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasDamagedByStationaryUnit.from_s(
            "[8:33:05 PM] User0:Pe-8 damaged by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasDamagedByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasDamagedByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.StationaryUnit("0_Static"),
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
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasDamagedByStationaryUnit",
                'verbose_name': "Human aircraft was damaged by stationary unit",
            }
        )


class HumanAircraftWasDamagedByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasDamagedByMovingUnitMember.from_s(
            "[8:33:05 PM] User0:Pe-8 damaged by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasDamagedByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasDamagedByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.MovingUnitMember("0_Chief", 0),
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
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasDamagedByMovingUnitMember",
                'verbose_name': "Human aircraft was damaged by moving unit member",
            }
        )


class HumanAircraftWasDamagedByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasDamagedByMovingUnit.from_s(
            "[8:33:05 PM] User0:Pe-8 damaged by 0_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasDamagedByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasDamagedByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.MovingUnit("0_Chief"),
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
                'attacker': {
                    'id': "0_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasDamagedByMovingUnit",
                'verbose_name': "Human aircraft was damaged by moving unit",
            }
        )


class HumanAircraftWasDamagedByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasDamagedByAIAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 damaged by r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasDamagedByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasDamagedByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.AIAircraft("r0100", 0),
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
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasDamagedByAIAircraft",
                'verbose_name': "Human aircraft was damaged by AI aircraft",
            }
        )


class HumanAircraftWasShotDownByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasShotDownByHumanAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-6_Late at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasShotDownByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.actor,
            actors.HumanAircraft("User0", "Pe-8")
        )
        self.assertEqual(
            event.attacker,
            actors.HumanAircraft("User1", "Bf-109G-6_Late")
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasShotDownByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.HumanAircraft("User1", "Bf-109G-6_Late"),
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
                'attacker': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-6_Late",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasShotDownByHumanAircraft",
                'verbose_name': "Human aircraft was shot down by human aircraft",
            }
        )


class HumanAircraftWasShotDownByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasShotDownByStationaryUnit.from_s(
            "[8:33:05 PM] User0:Pe-8 shot down by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasShotDownByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasShotDownByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.StationaryUnit("0_Static"),
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
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasShotDownByStationaryUnit",
                'verbose_name': "Human aircraft was shot down by stationary unit",
            }
        )


class HumanAircraftWasShotDownByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasShotDownByMovingUnitMember.from_s(
            "[8:33:05 PM] User0:Pe-8 shot down by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasShotDownByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasShotDownByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.MovingUnitMember("0_Chief", 0),
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
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasShotDownByMovingUnitMember",
                'verbose_name': "Human aircraft was shot down by moving unit member",
            }
        )


class HumanAircraftWasShotDownByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasShotDownByMovingUnit.from_s(
            "[8:33:05 PM] User0:Pe-8 shot down by 0_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasShotDownByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasShotDownByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.MovingUnit("0_Chief"),
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
                'attacker': {
                    'id': "0_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasShotDownByMovingUnit",
                'verbose_name': "Human aircraft was shot down by moving unit",
            }
        )


class HumanAircraftWasShotDownByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasShotDownByAIAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 shot down by r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasShotDownByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasShotDownByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.AIAircraft("r0100", 0),
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
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasShotDownByAIAircraft",
                'verbose_name': "Human aircraft was shot down by AI aircraft",
            }
        )


class HumanAircraftWasShotDownByHumanAircraftAndHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasShotDownByHumanAircraftAndHumanAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-2 and User2:Bf-109G-2 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasShotDownByHumanAircraftAndHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.HumanAircraft("User1", "Bf-109G-2"))
        self.assertEqual(event.assistant, actors.HumanAircraft("User2", "Bf-109G-2"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasShotDownByHumanAircraftAndHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.HumanAircraft("User1", "Bf-109G-2"),
            assistant=actors.HumanAircraft("User2", "Bf-109G-2"),
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
                'attacker': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-2",
                },
                'assistant': {
                    'callsign': "User2",
                    'aircraft': "Bf-109G-2",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasShotDownByHumanAircraftAndHumanAircraft",
                'verbose_name': "Human aircraft was shot down by human aircraft and human aircraft",
            }
        )


class HumanAircraftWasShotDownByHumanAircraftAndAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasShotDownByHumanAircraftAndAIAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-2 and r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasShotDownByHumanAircraftAndAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.HumanAircraft("User1", "Bf-109G-2"))
        self.assertEqual(event.assistant, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasShotDownByHumanAircraftAndAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.HumanAircraft("User1", "Bf-109G-2"),
            assistant=actors.AIAircraft("r0100", 0),
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
                'attacker': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-2",
                },
                'assistant': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasShotDownByHumanAircraftAndAIAircraft",
                'verbose_name': "Human aircraft was shot down by human aircraft and AI aircraft",
            }
        )


class HumanAircraftWasShotDownByAIAircraftAndHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasShotDownByAIAircraftAndHumanAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 shot down by r01000 and User1:Bf-109G-2 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasShotDownByAIAircraftAndHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.assistant, actors.HumanAircraft("User1", "Bf-109G-2"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasShotDownByAIAircraftAndHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.AIAircraft("r0100", 0),
            assistant=actors.HumanAircraft("User1", "Bf-109G-2"),
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
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'assistant': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-2",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasShotDownByAIAircraftAndHumanAircraft",
                'verbose_name': "Human aircraft was shot down by AI aircraft and human aircraft",
            }
        )


class HumanAircraftWasShotDownByAIAircraftAndAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftWasShotDownByAIAircraftAndAIAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8 shot down by r01000 and r01001 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftWasShotDownByAIAircraftAndAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.assistant, actors.AIAircraft("r0100", 1))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftWasShotDownByAIAircraftAndAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraft("User0", "Pe-8"),
            attacker=actors.AIAircraft("r0100", 0),
            assistant=actors.AIAircraft("r0100", 1),
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
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'assistant': {
                    'flight': "r0100",
                    'aircraft': 1,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasShotDownByAIAircraftAndAIAircraft",
                'verbose_name': "Human aircraft was shot down by AI aircraft and AI aircraft",
            }
        )


class HumanAircraftCrewMemberHasBailedOutTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberHasBailedOut.from_s(
            "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberHasBailedOut)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberHasBailedOut(
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
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberHasBailedOut",
                'verbose_name': "Human aircraft crew member has bailed out",
            }
        )


class HumanAircraftCrewMemberHasLandedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberHasLanded.from_s(
            "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberHasLanded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberHasLanded(
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
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberHasLanded",
                'verbose_name': "Human aircraft crew member has landed",
            }
        )


class HumanAircraftCrewMemberWasCapturedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasCaptured.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was captured at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasCaptured)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasCaptured(
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
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasCaptured",
                'verbose_name': "Human aircraft crew member was captured",
            }
        )


class HumanAircraftCrewMemberWasWoundedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasWounded.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasWounded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasWounded(
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
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasWounded",
                'verbose_name': "Human aircraft crew member was wounded",
            }
        )


class HumanAircraftCrewMemberWasHeavilyWoundedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasHeavilyWounded.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasHeavilyWounded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasHeavilyWounded(
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
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasHeavilyWounded",
                'verbose_name': "Human aircraft crew member was heavily wounded",
            }
        )


class HumanAircraftCrewMemberWasKilledTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasKilled.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was killed at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasKilled)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasKilled(
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
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilled",
                'verbose_name': "Human aircraft crew member was killed",
            }
        )


class HumanAircraftCrewMemberWasKilledByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasKilledByHumanAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasKilledByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.HumanAircraft("User1", "Bf-109G-6_Late"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasKilledByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.HumanAircraft("User1", "Bf-109G-6_Late"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-6_Late",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilledByHumanAircraft",
                'verbose_name': "Human aircraft crew member was killed by human aircraft",
            }
        )


class HumanAircraftCrewMemberWasKilledByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasKilledByStationaryUnit.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was killed by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasKilledByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasKilledByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.HumanAircraft("User1", "Bf-109G-6_Late"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-6_Late",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilledByStationaryUnit",
                'verbose_name': "Human aircraft crew member was killed by stationary unit",
            }
        )


class HumanAircraftCrewMemberWasKilledByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasKilledByMovingUnitMember.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was killed by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasKilledByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasKilledByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.MovingUnitMember("0_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilledByMovingUnitMember",
                'verbose_name': "Human aircraft crew member was killed by moving unit member",
            }
        )


class HumanAircraftCrewMemberWasKilledByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasKilledByMovingUnit.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was killed by 0_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasKilledByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasKilledByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.MovingUnit("0_Chief"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'id': "0_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilledByMovingUnit",
                'verbose_name': "Human aircraft crew member was killed by moving unit",
            }
        )


class HumanAircraftCrewMemberWasKilledByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasKilledByAIAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was killed by r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasKilledByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasKilledByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilledByAIAircraft",
                'verbose_name': "Human aircraft crew member was killed by AI aircraft",
            }
        )


class HumanAircraftCrewMemberWasKilledInParachuteByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasKilledInParachuteByStationaryUnit.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was killed in his chute by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasKilledInParachuteByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasKilledInParachuteByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.StationaryUnit("0_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilledInParachuteByStationaryUnit",
                'verbose_name': "Human aircraft crew member was killed in parachute by stationary unit",
            }
        )


class HumanAircraftCrewMemberWasKilledInParachuteByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasKilledInParachuteByMovingUnitMember.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was killed in his chute by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasKilledInParachuteByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasKilledInParachuteByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.MovingUnitMember("0_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilledInParachuteByMovingUnitMember",
                'verbose_name': "Human aircraft crew member was killed in parachute by moving unit member",
            }
        )


class HumanAircraftCrewMemberWasKilledInParachuteByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasKilledInParachuteByMovingUnit.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was killed in his chute by 0_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasKilledInParachuteByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasKilledInParachuteByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.MovingUnit("0_Chief"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'id': "0_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilledInParachuteByMovingUnit",
                'verbose_name': "Human aircraft crew member was killed in parachute by moving unit",
            }
        )


class HumanAircraftCrewMemberWasKilledInParachuteByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasKilledInParachuteByHumanAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was killed in his chute by User1:Bf-109G-2 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasKilledInParachuteByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.HumanAircraft("User1", "Bf-109G-2"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasKilledInParachuteByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.HumanAircraft("User1", "Bf-109G-2"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-2",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilledInParachuteByHumanAircraft",
                'verbose_name': "Human aircraft crew member was killed in parachute by human aircraft",
            }
        )


class HumanAircraftCrewMemberWasKilledInParachuteByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberWasKilledInParachuteByAIAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8(0) was killed in his chute by r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberWasKilledInParachuteByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberWasKilledInParachuteByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilledInParachuteByAIAircraft",
                'verbose_name': "Human aircraft crew member was killed in parachute by AI aircraft",
            }
        )


class HumanAircraftCrewMemberParachuteWasDestroyedByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberParachuteWasDestroyedByStationaryUnit.from_s(
            "[8:33:05 PM] User0:Pe-8(0) has chute destroyed by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberParachuteWasDestroyedByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberParachuteWasDestroyedByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.StationaryUnit("0_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberParachuteWasDestroyedByStationaryUnit",
                'verbose_name': "Human aircraft crew member's parachute was destroyed by stationary unit",
            }
        )


class HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnitMember.from_s(
            "[8:33:05 PM] User0:Pe-8(0) has chute destroyed by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.MovingUnitMember("0_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnitMember",
                'verbose_name': "Human aircraft crew member's parachute was destroyed by moving unit member",
            }
        )


class HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnit.from_s(
            "[8:33:05 PM] User0:Pe-8(0) has chute destroyed by 0_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.MovingUnit("0_Chief"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'id': "0_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnit",
                'verbose_name': "Human aircraft crew member's parachute was destroyed by moving unit",
            }
        )


class HumanAircraftCrewMemberParachuteWasDestroyedByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberParachuteWasDestroyedByHumanAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8(0) has chute destroyed by User1:Bf-109G-2 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberParachuteWasDestroyedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.HumanAircraft("User1", "Bf-109G-2"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberParachuteWasDestroyedByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.HumanAircraft("User1", "Bf-109G-2"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-2",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberParachuteWasDestroyedByHumanAircraft",
                'verbose_name': "Human aircraft crew member's parachute was destroyed by human aircraft",
            }
        )


class HumanAircraftCrewMemberParachuteWasDestroyedByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.HumanAircraftCrewMemberParachuteWasDestroyedByAIAircraft.from_s(
            "[8:33:05 PM] User0:Pe-8(0) has chute destroyed by r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.HumanAircraftCrewMemberParachuteWasDestroyedByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.HumanAircraftCrewMember("User0", "Pe-8", 0))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.HumanAircraftCrewMemberParachuteWasDestroyedByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.HumanAircraftCrewMember("User0", "Pe-8", 0),
            attacker=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'index': 0,
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberParachuteWasDestroyedByAIAircraft",
                'verbose_name': "Human aircraft crew member's parachute was destroyed by AI aircraft",
            }
        )


class BuildingWasDestroyedByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.BuildingWasDestroyedByHumanAircraft.from_s(
            "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.BuildingWasDestroyedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.Building("Finland/CenterHouse1_w"))
        self.assertEqual(event.attacker, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.BuildingWasDestroyedByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.Building("Finland/CenterHouse1_w"),
            attacker=actors.HumanAircraft("User0", "Pe-8"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'name': "Finland/CenterHouse1_w",
                },
                'attacker': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BuildingWasDestroyedByHumanAircraft",
                'verbose_name': "Building was destroyed by human aircraft",
            }
        )


class BuildingWasDestroyedByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.BuildingWasDestroyedByStationaryUnit.from_s(
            "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.BuildingWasDestroyedByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.Building("Finland/CenterHouse1_w"))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.BuildingWasDestroyedByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.Building("Finland/CenterHouse1_w"),
            attacker=actors.StationaryUnit("0_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'name': "Finland/CenterHouse1_w",
                },
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BuildingWasDestroyedByStationaryUnit",
                'verbose_name': "Building was destroyed by stationary unit",
            }
        )


class BuildingWasDestroyedByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.BuildingWasDestroyedByMovingUnitMember.from_s(
            "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.BuildingWasDestroyedByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.Building("Finland/CenterHouse1_w"))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.BuildingWasDestroyedByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.Building("Finland/CenterHouse1_w"),
            attacker=actors.MovingUnitMember("0_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'name': "Finland/CenterHouse1_w",
                },
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BuildingWasDestroyedByMovingUnitMember",
                'verbose_name': "Building was destroyed by moving unit member",
            }
        )


class BuildingWasDestroyedByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.BuildingWasDestroyedByMovingUnit.from_s(
            "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by 0_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.BuildingWasDestroyedByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.Building("Finland/CenterHouse1_w"))
        self.assertEqual(event.attacker, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.BuildingWasDestroyedByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.Building("Finland/CenterHouse1_w"),
            attacker=actors.MovingUnit("0_Chief"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'name': "Finland/CenterHouse1_w",
                },
                'attacker': {
                    'id': "0_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BuildingWasDestroyedByMovingUnit",
                'verbose_name': "Building was destroyed by moving unit",
            }
        )


class BuildingWasDestroyedByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.BuildingWasDestroyedByAIAircraft.from_s(
            "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.BuildingWasDestroyedByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.Building("Finland/CenterHouse1_w"))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.BuildingWasDestroyedByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.Building("Finland/CenterHouse1_w"),
            attacker=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'name': "Finland/CenterHouse1_w",
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BuildingWasDestroyedByAIAircraft",
                'verbose_name': "Building was destroyed by AI aircraft",
            }
        )


class TreeWasDestroyedByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.TreeWasDestroyedByHumanAircraft.from_s(
            "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.TreeWasDestroyedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.attacker, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.TreeWasDestroyedByHumanAircraft(
            time=datetime.time(20, 33, 5),
            attacker=actors.HumanAircraft("User0", "Pe-8"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'attacker': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "TreeWasDestroyedByHumanAircraft",
                'verbose_name': "Tree was destroyed by human aircraft",
            }
        )


class TreeWasDestroyedByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.TreeWasDestroyedByStationaryUnit.from_s(
            "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.TreeWasDestroyedByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.TreeWasDestroyedByStationaryUnit(
            time=datetime.time(20, 33, 5),
            attacker=actors.StationaryUnit("0_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "TreeWasDestroyedByStationaryUnit",
                'verbose_name': "Tree was destroyed by stationary unit",
            }
        )


class TreeWasDestroyedByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.TreeWasDestroyedByAIAircraft.from_s(
            "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.TreeWasDestroyedByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.TreeWasDestroyedByAIAircraft(
            time=datetime.time(20, 33, 5),
            attacker=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "TreeWasDestroyedByAIAircraft",
                'verbose_name': "Tree was destroyed by AI aircraft",
            }
        )


class TreeWasDestroyedByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.TreeWasDestroyedByMovingUnitMember.from_s(
            "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.TreeWasDestroyedByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.TreeWasDestroyedByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            attacker=actors.MovingUnitMember("0_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "TreeWasDestroyedByMovingUnitMember",
                'verbose_name': "Tree was destroyed by moving unit member",
            }
        )


class TreeWasDestroyedByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.TreeWasDestroyedByMovingUnit.from_s(
            "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by 0_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.TreeWasDestroyedByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.attacker, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.TreeWasDestroyedByMovingUnit(
            time=datetime.time(20, 33, 5),
            attacker=actors.MovingUnit("0_Chief"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'attacker': {
                    'id': "0_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "TreeWasDestroyedByMovingUnit",
                'verbose_name': "Tree was destroyed by moving unit",
            }
        )


class TreeWasDestroyedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.TreeWasDestroyed.from_s(
            "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by at 100.0 200.99"
        )
        self.assertIsInstance(event, events.TreeWasDestroyed)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.TreeWasDestroyed(
            time=datetime.time(20, 33, 5),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "TreeWasDestroyed",
                'verbose_name': "Tree was destroyed",
            }
        )


class StationaryUnitWasDestroyedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.StationaryUnitWasDestroyed.from_s(
            "[8:33:05 PM] 0_Static crashed at 100.0 200.99"
        )
        self.assertIsInstance(event, events.StationaryUnitWasDestroyed)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.StationaryUnitWasDestroyed(
            time=datetime.time(20, 33, 5),
            actor=actors.StationaryUnit("0_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "StationaryUnitWasDestroyed",
                'verbose_name': "Stationary unit was destroyed",
            }
        )


class StationaryUnitWasDestroyedByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.StationaryUnitWasDestroyedByStationaryUnit.from_s(
            "[8:33:05 PM] 0_Static destroyed by 1_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.StationaryUnitWasDestroyedByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.attacker, actors.StationaryUnit("1_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.StationaryUnitWasDestroyedByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.StationaryUnit("0_Static"),
            attacker=actors.StationaryUnit("1_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Static",
                },
                'attacker': {
                    'id': "1_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "StationaryUnitWasDestroyedByStationaryUnit",
                'verbose_name': "Stationary unit was destroyed by stationary unit",
            }
        )


class StationaryUnitWasDestroyedByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.StationaryUnitWasDestroyedByMovingUnit.from_s(
            "[8:33:05 PM] 0_Static destroyed by 0_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.StationaryUnitWasDestroyedByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.attacker, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.StationaryUnitWasDestroyedByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.StationaryUnit("0_Static"),
            attacker=actors.MovingUnit("0_Chief"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Static",
                },
                'attacker': {
                    'id': "0_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "StationaryUnitWasDestroyedByMovingUnit",
                'verbose_name': "Stationary unit was destroyed by moving unit",
            }
        )


class StationaryUnitWasDestroyedByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.StationaryUnitWasDestroyedByMovingUnitMember.from_s(
            "[8:33:05 PM] 0_Static destroyed by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.StationaryUnitWasDestroyedByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.StationaryUnitWasDestroyedByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.StationaryUnit("0_Static"),
            attacker=actors.MovingUnitMember("0_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Static",
                },
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "StationaryUnitWasDestroyedByMovingUnitMember",
                'verbose_name': "Stationary unit was destroyed by moving unit member",
            }
        )


class StationaryUnitWasDestroyedByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.StationaryUnitWasDestroyedByHumanAircraft.from_s(
            "[8:33:05 PM] 0_Static destroyed by User0:Pe-8 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.StationaryUnitWasDestroyedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.attacker, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.StationaryUnitWasDestroyedByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.StationaryUnit("0_Static"),
            attacker=actors.HumanAircraft("User0", "Pe-8"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Static",
                },
                'attacker': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "StationaryUnitWasDestroyedByHumanAircraft",
                'verbose_name': "Stationary unit was destroyed by human aircraft",
            }
        )


class StationaryUnitWasDestroyedByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.StationaryUnitWasDestroyedByAIAircraft.from_s(
            "[8:33:05 PM] 0_Static destroyed by r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.StationaryUnitWasDestroyedByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.StationaryUnitWasDestroyedByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.StationaryUnit("0_Static"),
            attacker=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Static",
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "StationaryUnitWasDestroyedByAIAircraft",
                'verbose_name': "Stationary unit was destroyed by AI aircraft",
            }
        )


class BridgeWasDestroyedByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.BridgeWasDestroyedByHumanAircraft.from_s(
            "[8:33:05 PM]  Bridge0 destroyed by User0:Pe-8 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.BridgeWasDestroyedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.Bridge("Bridge0"))
        self.assertEqual(event.attacker, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.BridgeWasDestroyedByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.Bridge("Bridge0"),
            attacker=actors.HumanAircraft("User0", "Pe-8"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "Bridge0",
                },
                'attacker': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BridgeWasDestroyedByHumanAircraft",
                'verbose_name': "Bridge was destroyed by human aircraft",
            }
        )


class BridgeWasDestroyedByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.BridgeWasDestroyedByStationaryUnit.from_s(
            "[8:33:05 PM]  Bridge0 destroyed by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.BridgeWasDestroyedByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.Bridge("Bridge0"))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.BridgeWasDestroyedByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.Bridge("Bridge0"),
            attacker=actors.StationaryUnit("0_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "Bridge0",
                },
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BridgeWasDestroyedByStationaryUnit",
                'verbose_name': "Bridge was destroyed by stationary unit",
            }
        )


class BridgeWasDestroyedByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.BridgeWasDestroyedByMovingUnitMember.from_s(
            "[8:33:05 PM]  Bridge0 destroyed by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.BridgeWasDestroyedByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.Bridge("Bridge0"))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.BridgeWasDestroyedByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.Bridge("Bridge0"),
            attacker=actors.MovingUnitMember("0_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "Bridge0",
                },
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BridgeWasDestroyedByMovingUnitMember",
                'verbose_name': "Bridge was destroyed by moving unit member",
            }
        )


class BridgeWasDestroyedByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.BridgeWasDestroyedByMovingUnit.from_s(
            "[8:33:05 PM]  Bridge0 destroyed by 0_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.BridgeWasDestroyedByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.Bridge("Bridge0"))
        self.assertEqual(event.attacker, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.BridgeWasDestroyedByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.Bridge("Bridge0"),
            attacker=actors.MovingUnit("0_Chief"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "Bridge0",
                },
                'attacker': {
                    'id': "0_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BridgeWasDestroyedByMovingUnit",
                'verbose_name': "Bridge was destroyed by moving unit",
            }
        )


class BridgeWasDestroyedByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.BridgeWasDestroyedByAIAircraft.from_s(
            "[8:33:05 PM]  Bridge0 destroyed by r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.BridgeWasDestroyedByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.Bridge("Bridge0"))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.BridgeWasDestroyedByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.Bridge("Bridge0"),
            attacker=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "Bridge0",
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BridgeWasDestroyedByAIAircraft",
                'verbose_name': "Bridge was destroyed by AI aircraft",
            }
        )


class MovingUnitWasDestroyedByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MovingUnitWasDestroyedByMovingUnit.from_s(
            "[8:33:05 PM] 0_Chief destroyed by 1_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.MovingUnitWasDestroyedByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.attacker, actors.MovingUnit("1_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.MovingUnitWasDestroyedByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.MovingUnit("0_Chief"),
            attacker=actors.MovingUnit("1_Chief"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Chief",
                },
                'attacker': {
                    'id': "1_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitWasDestroyedByMovingUnit",
                'verbose_name': "Moving unit was destroyed by moving unit",
            }
        )


class MovingUnitWasDestroyedByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MovingUnitWasDestroyedByMovingUnitMember.from_s(
            "[8:33:05 PM] 0_Chief destroyed by 1_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.MovingUnitWasDestroyedByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.attacker, actors.MovingUnitMember("1_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.MovingUnitWasDestroyedByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.MovingUnit("0_Chief"),
            attacker=actors.MovingUnitMember("1_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Chief",
                },
                'attacker': {
                    'id': "1_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitWasDestroyedByMovingUnitMember",
                'verbose_name': "Moving unit was destroyed by moving unit member",
            }
        )


class MovingUnitWasDestroyedByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MovingUnitWasDestroyedByStationaryUnit.from_s(
            "[8:33:05 PM] 0_Chief destroyed by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.MovingUnitWasDestroyedByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.MovingUnitWasDestroyedByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.MovingUnit("0_Chief"),
            attacker=actors.StationaryUnit("0_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Chief",
                },
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitWasDestroyedByStationaryUnit",
                'verbose_name': "Moving unit was destroyed by stationary unit",
            }
        )


class MovingUnitWasDestroyedByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MovingUnitWasDestroyedByHumanAircraft.from_s(
            "[8:33:05 PM] 0_Chief destroyed by User0:Pe-8 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.MovingUnitWasDestroyedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.attacker, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.MovingUnitWasDestroyedByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.MovingUnit("0_Chief"),
            attacker=actors.HumanAircraft("User0", "Pe-8"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Chief",
                },
                'attacker': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitWasDestroyedByHumanAircraft",
                'verbose_name': "Moving unit was destroyed by human aircraft",
            }
        )


class MovingUnitWasDestroyedByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MovingUnitWasDestroyedByAIAircraft.from_s(
            "[8:33:05 PM] 0_Chief destroyed by r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.MovingUnitWasDestroyedByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.MovingUnitWasDestroyedByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.MovingUnit("0_Chief"),
            attacker=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Chief",
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitWasDestroyedByAIAircraft",
                'verbose_name': "Moving unit was destroyed by AI aircraft",
            }
        )


class MovingUnitMemberWasDestroyedByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MovingUnitMemberWasDestroyedByStationaryUnit.from_s(
            "[8:33:05 PM] 0_Chief0 destroyed by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.MovingUnitMemberWasDestroyedByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.MovingUnitMemberWasDestroyedByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.MovingUnitMember("0_Chief", 0),
            attacker=actors.StationaryUnit("0_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitMemberWasDestroyedByStationaryUnit",
                'verbose_name': "Moving unit member was destroyed by stationary unit",
            }
        )


class MovingUnitMemberWasDestroyedByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MovingUnitMemberWasDestroyedByAIAircraft.from_s(
            "[8:33:05 PM] 0_Chief0 destroyed by r01000 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.MovingUnitMemberWasDestroyedByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.MovingUnitMemberWasDestroyedByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.MovingUnitMember("0_Chief", 0),
            attacker=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitMemberWasDestroyedByAIAircraft",
                'verbose_name': "Moving unit member was destroyed by AI aircraft",
            }
        )


class MovingUnitMemberWasDestroyedByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MovingUnitMemberWasDestroyedByHumanAircraft.from_s(
            "[8:33:05 PM] 0_Chief0 destroyed by User0:Pe-8 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.MovingUnitMemberWasDestroyedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.attacker, actors.HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.MovingUnitMemberWasDestroyedByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.MovingUnitMember("0_Chief", 0),
            attacker=actors.HumanAircraft("User0", "Pe-8"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'attacker': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitMemberWasDestroyedByHumanAircraft",
                'verbose_name': "Moving unit member was destroyed by human aircraft",
            }
        )


class MovingUnitMemberWasDestroyedByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MovingUnitMemberWasDestroyedByMovingUnit.from_s(
            "[8:33:05 PM] 0_Chief0 destroyed by 1_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.MovingUnitMemberWasDestroyedByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.attacker, actors.MovingUnit("1_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.MovingUnitMemberWasDestroyedByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.MovingUnitMember("0_Chief", 0),
            attacker=actors.MovingUnit("1_Chief"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'attacker': {
                    'id': "1_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitMemberWasDestroyedByMovingUnit",
                'verbose_name': "Moving unit member was destroyed by moving unit",
            }
        )


class MovingUnitMemberWasDestroyedByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.MovingUnitMemberWasDestroyedByMovingUnitMember.from_s(
            "[8:33:05 PM] 0_Chief0 destroyed by 1_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.MovingUnitMemberWasDestroyedByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.attacker, actors.MovingUnitMember("1_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.MovingUnitMemberWasDestroyedByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.MovingUnitMember("0_Chief", 0),
            attacker=actors.MovingUnitMember("1_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'attacker': {
                    'id': "1_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitMemberWasDestroyedByMovingUnitMember",
                'verbose_name': "Moving unit member was destroyed by moving unit member",
            }
        )


class AIAircraftHasDespawnedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftHasDespawned.from_s(
            "[8:33:05 PM] r01000 removed at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftHasDespawned)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftHasDespawned(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftHasDespawned",
                'verbose_name': "AI aircraft has despawned",
            }
        )


class AIAircraftWasDamagedOnGroundTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasDamagedOnGround.from_s(
            "[8:33:05 PM] r01000 damaged on the ground at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasDamagedOnGround)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasDamagedOnGround(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasDamagedOnGround",
                'verbose_name': "AI aircraft was damaged on the ground",
            }
        )


class AIAircraftWasDamagedByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasDamagedByHumanAircraft.from_s(
            "[8:33:05 PM] r01000 damaged by User1:Bf-109G-6_Late at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasDamagedByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.HumanAircraft("User1", "Bf-109G-6_Late"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasDamagedByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.HumanAircraft("User1", "Bf-109G-6_Late"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-6_Late",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasDamagedByHumanAircraft",
                'verbose_name': "AI aircraft was damaged by human aircraft",
            }
        )


class AIAircraftWasDamagedByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasDamagedByStationaryUnit.from_s(
            "[8:33:05 PM] r01000 damaged by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasDamagedByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasDamagedByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.StationaryUnit("0_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasDamagedByStationaryUnit",
                'verbose_name': "AI aircraft was damaged by stationary unit",
            }
        )


class AIAircraftWasDamagedByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasDamagedByMovingUnitMember.from_s(
            "[8:33:05 PM] r01000 damaged by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasDamagedByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasDamagedByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.MovingUnitMember("0_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasDamagedByMovingUnitMember",
                'verbose_name': "AI aircraft was damaged by moving unit member",
            }
        )


class AIAircraftWasDamagedByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasDamagedByMovingUnit.from_s(
            "[8:33:05 PM] r01000 damaged by 0_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasDamagedByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasDamagedByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.MovingUnit("0_Chief"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'id': "0_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasDamagedByMovingUnit",
                'verbose_name': "AI aircraft was damaged by moving unit",
            }
        )


class AIAircraftWasDamagedByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasDamagedByAIAircraft.from_s(
            "[8:33:05 PM] r01000 damaged by r01001 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasDamagedByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 1))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasDamagedByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.AIAircraft("r0100", 1),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 1,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasDamagedByAIAircraft",
                'verbose_name': "AI aircraft was damaged by AI aircraft",
            }
        )


class AIHasDamagedOwnAircraftTestCase(unittest.TestCase):

    def test_from_s_by_landscape(self):
        event = events.AIHasDamagedOwnAircraft.from_s(
            "[8:33:05 PM] r01000 damaged by landscape at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIHasDamagedOwnAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_from_s_by_noname(self):
        event = events.AIHasDamagedOwnAircraft.from_s(
            "[8:33:05 PM] r01000 damaged by NONAME at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIHasDamagedOwnAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIHasDamagedOwnAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIHasDamagedOwnAircraft",
                'verbose_name': "AI has damaged own aircraft",
            }
        )


class AIHasDestroyedOwnAircraftTestCase(unittest.TestCase):

    def test_from_s_by_landscape(self):
        event = events.AIHasDestroyedOwnAircraft.from_s(
            "[8:33:05 PM] r01000 shot down by landscape at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIHasDestroyedOwnAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_from_s_by_noname(self):
        event = events.AIHasDestroyedOwnAircraft.from_s(
            "[8:33:05 PM] r01000 shot down by NONAME at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIHasDestroyedOwnAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIHasDestroyedOwnAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIHasDestroyedOwnAircraft",
                'verbose_name': "AI has destroyed own aircraft",
            }
        )


class AIAircraftHasLandedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftHasLanded.from_s(
            "[8:33:05 PM] r01000 landed at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftHasLanded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftHasLanded(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftHasLanded",
                'verbose_name': "AI aircraft has landed",
            }
        )


class AIAircraftHasCrashedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftHasCrashed.from_s(
            "[8:33:05 PM] r01000 crashed at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftHasCrashed)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftHasCrashed(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftHasCrashed",
                'verbose_name': "AI aircraft has crashed",
            }
        )


class AIAircraftWasShotDownByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasShotDownByHumanAircraft.from_s(
            "[8:33:05 PM] r01000 shot down by User1:Bf-109G-6_Late at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasShotDownByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.HumanAircraft("User1", "Bf-109G-6_Late"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasShotDownByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.HumanAircraft("User1", "Bf-109G-6_Late"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-6_Late",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasShotDownByHumanAircraft",
                'verbose_name': "AI aircraft was shot down by human aircraft",
            }
        )


class AIAircraftWasShotDownByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasShotDownByAIAircraft.from_s(
            "[8:33:05 PM] r01000 shot down by r01001 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasShotDownByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 1))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasShotDownByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.AIAircraft("r0100", 1),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 1,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasShotDownByAIAircraft",
                'verbose_name': "AI aircraft was shot down by AI aircraft",
            }
        )


class AIAircraftWasShotDownByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasShotDownByStationaryUnit.from_s(
            "[8:33:05 PM] r01000 shot down by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasShotDownByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasShotDownByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.StationaryUnit("0_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasShotDownByStationaryUnit",
                'verbose_name': "AI aircraft was shot down by stationary unit",
            }
        )


class AIAircraftWasShotDownByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasShotDownByMovingUnitMember.from_s(
            "[8:33:05 PM] r01000 shot down by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasShotDownByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasShotDownByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.MovingUnitMember("0_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasShotDownByMovingUnitMember",
                'verbose_name': "AI aircraft was shot down by moving unit member",
            }
        )


class AIAircraftWasShotDownByMovingUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasShotDownByMovingUnit.from_s(
            "[8:33:05 PM] r01000 shot down by 0_Chief at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasShotDownByMovingUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.MovingUnit("0_Chief"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasShotDownByMovingUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.MovingUnit("0_Chief"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'id': "0_Chief",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasShotDownByMovingUnit",
                'verbose_name': "AI aircraft was shot down by moving unit",
            }
        )


class AIAircraftWasShotDownByAIAircraftAndAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasShotDownByAIAircraftAndAIAircraft.from_s(
            "[8:33:05 PM] r01000 shot down by r01001 and r01002 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasShotDownByAIAircraftAndAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 1))
        self.assertEqual(event.assistant, actors.AIAircraft("r0100", 2))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasShotDownByAIAircraftAndAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.AIAircraft("r0100", 1),
            assistant=actors.AIAircraft("r0100", 2),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 1,
                },
                'assistant': {
                    'flight': "r0100",
                    'aircraft': 2,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasShotDownByAIAircraftAndAIAircraft",
                'verbose_name': "AI aircraft was shot down by AI aircraft and AI aircraft",
            }
        )


class AIAircraftWasShotDownByHumanAircraftAndHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftWasShotDownByHumanAircraftAndHumanAircraft.from_s(
            "[8:33:05 PM] r01000 shot down by User0:Bf-109G-2 and User1:Bf-109G-2 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftWasShotDownByHumanAircraftAndHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraft("r0100", 0))
        self.assertEqual(event.attacker, actors.HumanAircraft("User0", "Bf-109G-2"))
        self.assertEqual(event.assistant, actors.HumanAircraft("User1", "Bf-109G-2"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftWasShotDownByHumanAircraftAndHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraft("r0100", 0),
            attacker=actors.HumanAircraft("User0", "Bf-109G-2"),
            assistant=actors.HumanAircraft("User1", "Bf-109G-2"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                },
                'attacker': {
                    'callsign': "User0",
                    'aircraft': "Bf-109G-2",
                },
                'assistant': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-2"
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasShotDownByHumanAircraftAndHumanAircraft",
                'verbose_name': "AI aircraft was shot down by human aircraft and human aircraft",
            }
        )


class AIAircraftCrewMemberWasKilledTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberWasKilled.from_s(
            "[8:33:05 PM] r01000(0) was killed at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberWasKilled)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberWasKilled(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasKilled",
                'verbose_name': "AI aircraft crew member was killed",
            }
        )


class AIAircraftCrewMemberWasKilledByStationaryUnitTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberWasKilledByStationaryUnit.from_s(
            "[8:33:05 PM] r01000(0) was killed by 0_Static at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberWasKilledByStationaryUnit)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.attacker, actors.StationaryUnit("0_Static"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberWasKilledByStationaryUnit(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            attacker=actors.StationaryUnit("0_Static"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'attacker': {
                    'id': "0_Static",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasKilledByStationaryUnit",
                'verbose_name': "AI aircraft crew member was killed by stationary unit",
            }
        )


class AIAircraftCrewMemberWasKilledByHumanAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberWasKilledByHumanAircraft.from_s(
            "[8:33:05 PM] r01000(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberWasKilledByHumanAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.attacker, actors.HumanAircraft("User1", "Bf-109G-6_Late"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberWasKilledByHumanAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            attacker=actors.HumanAircraft("User1", "Bf-109G-6_Late"),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'attacker': {
                    'callsign': "User1",
                    'aircraft': "Bf-109G-6_Late",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasKilledByHumanAircraft",
                'verbose_name': "AI aircraft crew member was killed by human aircraft",
            }
        )


class AIAircraftCrewMemberWasKilledByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberWasKilledByAIAircraft.from_s(
            "[8:33:05 PM] r01000(0) was killed by r01001 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberWasKilledByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 1))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberWasKilledByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            attacker=actors.AIAircraft("r0100", 1),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 1,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasKilledByAIAircraft",
                'verbose_name': "AI aircraft crew member was killed by AI aircraft",
            }
        )


class AIAircraftCrewMemberWasKilledByMovingUnitMemberTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberWasKilledByMovingUnitMember.from_s(
            "[8:33:05 PM] r01000(0) was killed by 0_Chief0 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberWasKilledByMovingUnitMember)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.attacker, actors.MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberWasKilledByMovingUnitMember(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            attacker=actors.MovingUnitMember("0_Chief", 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'attacker': {
                    'id': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasKilledByMovingUnitMember",
                'verbose_name': "AI aircraft crew member was killed by moving unit member",
            }
        )


class AIAircraftCrewMemberWasKilledInParachuteByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberWasKilledInParachuteByAIAircraft.from_s(
            "[8:33:05 PM] r01000(0) was killed in his chute by r01001 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberWasKilledInParachuteByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 1))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberWasKilledInParachuteByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            attacker=actors.AIAircraft("r0100", 1),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 1,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasKilledInParachuteByAIAircraft",
                'verbose_name': "AI aircraft crew member was killed in parachute by AI aircraft",
            }
        )


class AIAircraftCrewMemberParachuteWasDestroyedByAIAircraftTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberParachuteWasDestroyedByAIAircraft.from_s(
            "[8:33:05 PM] r01000(0) has chute destroyed by r01001 at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberParachuteWasDestroyedByAIAircraft)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.attacker, actors.AIAircraft("r0100", 1))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberParachuteWasDestroyedByAIAircraft(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            attacker=actors.AIAircraft("r0100", 1),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'attacker': {
                    'flight': "r0100",
                    'aircraft': 1,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberParachuteWasDestroyedByAIAircraft",
                'verbose_name': "AI aircraft crew member's parachute was destroyed by AI aircraft",
            }
        )


class AIAircraftCrewMemberParachuteWasDestroyedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberParachuteWasDestroyed.from_s(
            "[8:33:05 PM] r01000(0) has chute destroyed at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberParachuteWasDestroyed)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberParachuteWasDestroyed(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberParachuteWasDestroyed",
                'verbose_name': "AI aircraft crew member's parachute was destroyed",
            }
        )


class AIAircraftCrewMemberWasWoundedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberWasWounded.from_s(
            "[8:33:05 PM] r01000(0) was wounded at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberWasWounded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberWasWounded(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasWounded",
                'verbose_name': "AI aircraft crew member was wounded",
            }
        )


class AIAircraftCrewMemberWasHeavilyWoundedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberWasHeavilyWounded.from_s(
            "[8:33:05 PM] r01000(0) was heavily wounded at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberWasHeavilyWounded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberWasHeavilyWounded(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasHeavilyWounded",
                'verbose_name': "AI aircraft crew member was heavily wounded",
            }
        )


class AIAircraftCrewMemberWasCapturedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberWasCaptured.from_s(
            "[8:33:05 PM] r01000(0) was captured at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberWasCaptured)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberWasCaptured(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasCaptured",
                'verbose_name': "AI aircraft crew member was captured",
            }
        )


class AIAircraftCrewMemberHasBailedOutTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberHasBailedOut.from_s(
            "[8:33:05 PM] r01000(0) bailed out at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberHasBailedOut)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberHasBailedOut(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberHasBailedOut",
                'verbose_name': "AI aircraft crew member has bailed out",
            }
        )


class AIAircraftCrewMemberHasLandedTestCase(unittest.TestCase):

    def test_from_s(self):
        event = events.AIAircraftCrewMemberHasLanded.from_s(
            "[8:33:05 PM] r01000(0) successfully bailed out at 100.0 200.99"
        )
        self.assertIsInstance(event, events.AIAircraftCrewMemberHasLanded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, actors.AIAircraftCrewMember("r0100", 0, 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))

    def test_to_primitive(self):
        event = events.AIAircraftCrewMemberHasLanded(
            time=datetime.time(20, 33, 5),
            actor=actors.AIAircraftCrewMember("r0100", 0, 0),
            pos=Point2D(100.0, 200.99),
        )
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'flight': "r0100",
                    'aircraft': 0,
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberHasLanded",
                'verbose_name': "AI aircraft crew member has landed",
            }
        )
