# -*- coding: utf-8 -*-

import datetime
import inspect

from il2fb.commons.organization import Belligerents

from il2fb.parsers.events.constants import TARGET_END_STATES
from il2fb.parsers.events.grammar import events as grammar
from il2fb.parsers.events.structures import (
    Point2D, HumanAircraft, HumanAircraftCrewMember, AIAircraftCrewMember,
    MovingUnitMember, events as structures,
)

from .base import BaseTestCase


class EventsTestCase(BaseTestCase):

    @staticmethod
    def string_to_event(string, event_grammar):
        return event_grammar.parseString(string).event

    def test_structures_defined_in_all(self):

        def members_filter(element):
            name, obj = element
            return (inspect.isclass(obj)
                    and issubclass(obj, structures.Event)
                    and obj is not structures.Event)

        members = filter(members_filter, inspect.getmembers(structures))

        for name, structure in members:
            self.assertIn(name, structures.__all__)

    def test_mission_is_playing(self):
        string = "[Sep 15, 2013 8:33:05 PM] Mission: path/PH.mis is Playing"
        event = self.string_to_event(string, grammar.mission_is_playing)

        self.assertIsInstance(event, structures.MissionIsPlaying)
        self.assertEqual(event.date, datetime.date(2013, 9, 15))
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.mission, "path/PH.mis")
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

    def test_mission_has_begun(self):
        string = "[8:33:05 PM] Mission BEGIN"
        event = self.string_to_event(string, grammar.mission_has_begun)

        self.assertIsInstance(event, structures.MissionHasBegun)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'name': "MissionHasBegun",
                'verbose_name': "Mission has begun",
            }
        )

    def test_mission_has_ended(self):
        string = "[8:33:05 PM] Mission END"
        event = self.string_to_event(string, grammar.mission_has_ended)

        self.assertIsInstance(event, structures.MissionHasEnded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'name': "MissionHasEnded",
                'verbose_name': "Mission has ended",
            }
        )

    def test_mission_was_won(self):
        string = "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"
        event = self.string_to_event(string, grammar.mission_was_won)

        self.assertIsInstance(event, structures.MissionWasWon)
        self.assertEqual(event.date, datetime.date(2013, 9, 15))
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.belligerent, Belligerents.red)
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

    def test_target_state_has_changed(self):
        testee = grammar.target_state_has_changed

        string = "[8:33:05 PM] Target 3 Complete"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, structures.TargetStateWasChanged)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.target_index, 3)
        self.assertEqual(event.state, TARGET_END_STATES.COMPLETE)
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'target_index': 3,
                'state': "Complete",
                'name': "TargetStateWasChanged",
                'verbose_name': "Target state was changed",
            }
        )

        string = "[8:33:05 PM] Target 3 Failed"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, structures.TargetStateWasChanged)
        self.assertEqual(event.state, TARGET_END_STATES.FAILED)
        self.assertEqual(event.to_primitive()['state'], "Failed")

    def test_human_has_connected(self):
        string = "[8:33:05 PM] User0 has connected"
        event = self.string_to_event(string, grammar.human_has_connected)

        self.assertIsInstance(event, structures.HumanHasConnected)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'callsign': "User0",
                'name': "HumanHasConnected",
                'verbose_name': "Human has connected",
            }
        )

    def test_human_has_disconnected(self):
        string = "[8:33:05 PM] User0 has disconnected"
        event = self.string_to_event(string, grammar.human_has_disconnected)

        self.assertIsInstance(event, structures.HumanHasDisconnected)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'callsign': "User0",
                'name': "HumanHasDisconnected",
                'verbose_name': "Human has disconnected",
            }
        )

    def test_human_has_selected_airfield(self):
        string = "[8:33:05 PM] User0 selected army Red at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_has_selected_airfield
        )

        self.assertIsInstance(event, structures.HumanHasSelectedAirfield)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(event.belligerent, Belligerents.red)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
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

    def test_human_has_went_to_briefing(self):
        string = "[8:33:05 PM] User0 entered refly menu"
        event = self.string_to_event(string, grammar.human_has_went_to_briefing)

        self.assertIsInstance(event, structures.HumanHasWentToBriefing)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.callsign, "User0")
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'callsign': "User0",
                'name': "HumanHasWentToBriefing",
                'verbose_name': "Human has went to briefing",
            }
        )

    def test_human_has_toggled_landing_lights(self):
        testee = grammar.human_has_toggled_landing_lights

        string = "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, structures.HumanHasToggledLandingLights)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.value, False)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'value': False,
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanHasToggledLandingLights",
                'verbose_name': "Human has toggled landing lights",
            }
        )

        string = "[8:33:05 PM] User0:Pe-8 turned landing lights on at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertEqual(event.value, True)
        self.assertEqual(event.to_primitive()['value'], True)

    def test_human_has_toggled_wingtip_smokes(self):
        testee = grammar.human_has_toggled_wingtip_smokes

        string = "[8:33:05 PM] User0:Pe-8 turned wingtip smokes off at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertIsInstance(event, structures.HumanHasToggledWingtipSmokes)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.value, False)
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'value': False,
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanHasToggledWingtipSmokes",
                'verbose_name': "Human has toggled wingtip smokes",
            }
        )

        string = "[8:33:05 PM] User0:Pe-8 turned wingtip smokes on at 100.0 200.99"
        event = self.string_to_event(string, testee)

        self.assertEqual(event.value, True)
        self.assertEqual(event.to_primitive()['value'], True)

    def test_human_has_changed_seat(self):
        string = "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"
        event = self.string_to_event(string, grammar.human_has_changed_seat)

        self.assertIsInstance(event, structures.HumanHasChangedSeat)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.actor,
            HumanAircraftCrewMember("User0", "Pe-8", 0)
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
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

    def test_human_has_damaged_his_aircraft(self):

        def _assert(string):
            event = self.string_to_event(
                string,
                grammar.human_has_damaged_his_aircraft
            )
            self.assertIsInstance(event, structures.HumanHasDamagedHisAircraft)
            self.assertEqual(event.time, datetime.time(20, 33, 5))
            self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
            self.assertEqual(event.pos, Point2D(100.0, 200.99))
            self.assertEqual(
                event.to_primitive(),
                {
                    'time': "20:33:05",
                    'victim': {
                        'callsign': "User0",
                        'aircraft': "Pe-8",
                    },
                    'pos': {
                        'x': 100.0,
                        'y': 200.99,
                    },
                    'name': "HumanHasDamagedHisAircraft",
                    'verbose_name': "Human has damaged his aircraft",
                }
            )

        _assert("[8:33:05 PM] User0:Pe-8 damaged by landscape at 100.0 200.99")
        _assert("[8:33:05 PM] User0:Pe-8 damaged by NONAME at 100.0 200.99")

    def test_human_has_destroyed_his_aircraft(self):

        def _assert(string):
            event = self.string_to_event(
                string,
                grammar.human_has_destroyed_his_aircraft
            )
            self.assertIsInstance(
                event,
                structures.HumanHasDestroyedHisAircraft
            )
            self.assertEqual(event.time, datetime.time(20, 33, 5))
            self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
            self.assertEqual(event.pos, Point2D(100.0, 200.99))
            self.assertEqual(
                event.to_primitive(),
                {
                    'time': "20:33:05",
                    'victim': {
                        'callsign': "User0",
                        'aircraft': "Pe-8",
                    },
                    'pos': {
                        'x': 100.0,
                        'y': 200.99,
                    },
                    'name': "HumanHasDestroyedHisAircraft",
                    'verbose_name': "Human has destroyed his aircraft",
                }
            )

        _assert("[8:33:05 PM] User0:Pe-8 shot down by landscape at 100.0 200.99")
        _assert("[8:33:05 PM] User0:Pe-8 shot down by NONAME at 100.0 200.99")

    def test_human_aircraft_has_spawned(self):
        string = "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_has_spawned
        )

        self.assertIsInstance(event, structures.HumanAircraftHasSpawned)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.weapons, "40fab100")
        self.assertEqual(event.fuel, 40)
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

    def test_human_aircraft_has_took_off(self):
        string = "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_has_took_off
        )

        self.assertIsInstance(event, structures.HumanAircraftHasTookOff)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
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

    def test_human_aircraft_has_landed(self):
        string = "[8:33:05 PM] User0:Pe-8 landed at 100.0 200.99"
        event = self.string_to_event(string, grammar.human_aircraft_has_landed)

        self.assertIsInstance(event, structures.HumanAircraftHasLanded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
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

    def test_human_aircraft_has_crashed(self):
        string = "[8:33:05 PM] User0:Pe-8 crashed at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_has_crashed
        )
        self.assertIsInstance(event, structures.HumanAircraftHasCrashed)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
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

    def test_human_aircraft_was_damaged_on_ground(self):
        string = "[8:33:05 PM] User0:Pe-8 damaged on the ground at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_was_damaged_on_ground
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftWasDamagedOnGround
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasDamagedOnGround",
                'verbose_name': "Human aircraft was damaged on ground",
            }
        )

    def test_human_aircraft_was_damaged_by_human_aircraft(self):
        string = "[8:33:05 PM] User0:Pe-8 damaged by User1:Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_was_damaged_by_human_aircraft
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftWasDamagedByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.victim,
            HumanAircraft("User0", "Pe-8")
        )
        self.assertEqual(
            event.aggressor,
            HumanAircraft("User1", "Bf-109G-6_Late")
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'aggressor': {
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

    def test_human_aircraft_was_damaged_by_static(self):
        string = "[8:33:05 PM] User0:Pe-8 damaged by 0_Static at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_was_damaged_by_static
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftWasDamagedByStatic
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.aggressor, "0_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'aggressor': "0_Static",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasDamagedByStatic",
                'verbose_name': "Human aircraft was damaged by static",
            }
        )

    def test_human_aircraft_was_damaged_by_ai_aircraft(self):
        string = "[8:33:05 PM] User0:Pe-8 damaged by Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_was_damaged_by_ai_aircraft
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftWasDamagedByAIAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.aggressor, "Bf-109G-6_Late")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'aggressor': "Bf-109G-6_Late",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasDamagedByAIAircraft",
                'verbose_name': "Human aircraft was damaged by AI aircraft",
            }
        )

    def test_human_aircraft_was_shot_down_by_human_aircraft(self):
        string = "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_was_shot_down_by_human_aircraft
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftWasShotDownByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.victim, HumanAircraft("User0", "Pe-8")
        )
        self.assertEqual(
            event.aggressor,
            HumanAircraft("User1", "Bf-109G-6_Late")
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'aggressor': {
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

    def test_human_aircraft_was_shot_down_by_static(self):
        string = "[8:33:05 PM] User0:Pe-8 shot down by 0_Static at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_was_shot_down_by_static
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftWasShotDownByStatic
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.aggressor, "0_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'aggressor': "0_Static",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasShotDownByStatic",
                'verbose_name': "Human aircraft was shot down by static",
            }
        )

    def test_human_aircraft_was_shot_down_by_ai_aircraft(self):
        string = "[8:33:05 PM] User0:Pe-8 shot down by Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_was_shot_down_by_ai_aircraft
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftWasShotDownByAIAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.aggressor, "Bf-109G-6_Late")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'aggressor': "Bf-109G-6_Late",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftWasShotDownByAIAircraft",
                'verbose_name': "Human aircraft was shot down by AI aircraft",
            }
        )

    def test_human_aircraft_crew_member_has_bailed_out(self):
        string = "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_crew_member_has_bailed_out
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftCrewMemberHasBailedOut
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.actor, HumanAircraftCrewMember("User0", "Pe-8", 0)
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
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
                'name': "HumanAircraftCrewMemberHasBailedOut",
                'verbose_name': "Human aircraft crew member has bailed out",
            }
        )

    def test_human_aircraft_crew_member_has_touched_down(self):
        string = "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_crew_member_has_touched_down
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftCrewMemberHasTouchedDown
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.actor,
            HumanAircraftCrewMember("User0", "Pe-8", 0)
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
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
                'name': "HumanAircraftCrewMemberHasTouchedDown",
                'verbose_name': "Human aircraft crew member has touched down",
            }
        )

    def test_human_aircraft_crew_member_was_captured(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was captured at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_crew_member_was_captured
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftCrewMemberWasCaptured
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.victim,
            HumanAircraftCrewMember("User0", "Pe-8", 0)
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasCaptured",
                'verbose_name': "Human aircraft crew member was captured",
            }
        )

    def test_human_aircraft_crew_member_was_wounded(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_crew_member_was_wounded
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftCrewMemberWasWounded
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.victim,
            HumanAircraftCrewMember("User0", "Pe-8", 0)
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasWounded",
                'verbose_name': "Human aircraft crew member was wounded",
            }
        )

    def test_human_aircraft_crew_member_was_heavily_wounded(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_crew_member_was_heavily_wounded
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftCrewMemberWasHeavilyWounded
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.victim,
            HumanAircraftCrewMember("User0", "Pe-8", 0)
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasHeavilyWounded",
                'verbose_name': "Human aircraft crew member was heavily wounded",
            }
        )

    def test_human_aircraft_crew_member_was_killed(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was killed at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_crew_member_was_killed
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftCrewMemberWasKilled
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.victim,
            HumanAircraftCrewMember("User0", "Pe-8", 0)
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilled",
                'verbose_name': "Human aircraft crew member was killed",
            }
        )

    def test_human_aircraft_crew_member_was_killed_by_human_aircraft(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_crew_member_was_killed_by_human_aircraft
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftCrewMemberWasKilledByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.victim,
            HumanAircraftCrewMember("User0", "Pe-8", 0)
        )
        self.assertEqual(
            event.aggressor,
            HumanAircraft("User1", "Bf-109G-6_Late")
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'aggressor': {
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

    def test_human_aircraft_crew_member_was_killed_by_static(self):
        string = "[8:33:05 PM] User0:Pe-8(0) was killed by 0_Static at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.human_aircraft_crew_member_was_killed_by_static
        )
        self.assertIsInstance(
            event,
            structures.HumanAircraftCrewMemberWasKilledByStatic
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(
            event.victim,
            HumanAircraftCrewMember("User0", "Pe-8", 0)
        )
        self.assertEqual(event.aggressor, "0_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'aggressor': "0_Static",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "HumanAircraftCrewMemberWasKilledByStatic",
                'verbose_name': "Human aircraft crew member was killed by static",
            }
        )

    def test_building_was_destroyed_by_human_aircraft(self):
        testee = grammar.building_was_destroyed_by_human_aircraft

        string = "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
        event = self.string_to_event(string, testee)
        self.assertIsInstance(
            event,
            structures.BuildingWasDestroyedByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Finland/CenterHouse1_w")
        self.assertEqual(event.aggressor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Finland/CenterHouse1_w",
                'aggressor': {
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

        string = "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/mono.sim destroyed by User1:Pe-8 at 300.0 400.99"
        event = self.string_to_event(string, testee)
        self.assertIsInstance(
            event,
            structures.BuildingWasDestroyedByHumanAircraft
        )
        self.assertEqual(event.victim, "Russia/Piter/House3_W")

    def test_building_was_destroyed_by_static(self):
        string = "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by 0_Static at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.building_was_destroyed_by_static
        )
        self.assertIsInstance(event, structures.BuildingWasDestroyedByStatic)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Finland/CenterHouse1_w")
        self.assertEqual(event.aggressor, "0_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Finland/CenterHouse1_w",
                'aggressor': "0_Static",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BuildingWasDestroyedByStatic",
                'verbose_name': "Building was destroyed by static",
            }
        )

    def test_building_was_destroyed_by_ai_aircraft(self):
        string = "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.building_was_destroyed_by_ai_aircraft
        )
        self.assertIsInstance(
            event,
            structures.BuildingWasDestroyedByAIAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Finland/CenterHouse1_w")
        self.assertEqual(event.aggressor, "Bf-109G-6_Late")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Finland/CenterHouse1_w",
                'aggressor': "Bf-109G-6_Late",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BuildingWasDestroyedByAIAircraft",
                'verbose_name': "Building was destroyed by AI aircraft",
            }
        )

    def test_building_was_destroyed_by_moving_unit(self):
        string = "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by 0_Chief at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.building_was_destroyed_by_moving_unit
        )
        self.assertIsInstance(
            event,
            structures.BuildingWasDestroyedByMovingUnit
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Finland/CenterHouse1_w")
        self.assertEqual(event.aggressor, "0_Chief")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Finland/CenterHouse1_w",
                'aggressor': "0_Chief",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "BuildingWasDestroyedByMovingUnit",
                'verbose_name': "Building was destroyed by moving unit",
            }
        )

    def test_tree_was_destroyed_by_human_aircraft(self):

        def _assert(string):
            event = self.string_to_event(
                string,
                grammar.tree_was_destroyed_by_human_aircraft
            )
            self.assertIsInstance(
                event,
                structures.TreeWasDestroyedByHumanAircraft
            )
            self.assertEqual(event.time, datetime.time(20, 33, 5))
            self.assertEqual(event.aggressor, HumanAircraft("User0", "Pe-8"))
            self.assertEqual(event.pos, Point2D(100.0, 200.99))
            self.assertEqual(
                event.to_primitive(),
                {
                    'time': "20:33:05",
                    'aggressor': {
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

        _assert("[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by User0:Pe-8 at 100.0 200.99")
        _assert("[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by User0:Pe-8 at 100.0 200.99")

    def test_tree_was_destroyed_by_static(self):

        def _assert(string):
            event = self.string_to_event(
                string,
                grammar.tree_was_destroyed_by_static
            )
            self.assertIsInstance(
                event,
                structures.TreeWasDestroyedByStatic
            )
            self.assertEqual(event.time, datetime.time(20, 33, 5))
            self.assertEqual(event.aggressor, "0_Static")
            self.assertEqual(event.pos, Point2D(100.0, 200.99))
            self.assertEqual(
                event.to_primitive(),
                {
                    'time': "20:33:05",
                    'aggressor': "0_Static",
                    'pos': {
                        'x': 100.0,
                        'y': 200.99,
                    },
                    'name': "TreeWasDestroyedByStatic",
                    'verbose_name': "Tree was destroyed by static",
                }
            )

        _assert("[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by 0_Static at 100.0 200.99")
        _assert("[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by 0_Static at 100.0 200.99")

    def test_tree_was_destroyed_by_ai_aircraft(self):

        def _assert(string):
            event = self.string_to_event(
                string,
                grammar.tree_was_destroyed_by_ai_aircraft
            )
            self.assertIsInstance(
                event,
                structures.TreeWasDestroyedByAIAircraft
            )
            self.assertEqual(event.time, datetime.time(20, 33, 5))
            self.assertEqual(event.aggressor, "Pe-8")
            self.assertEqual(event.pos, Point2D(100.0, 200.99))
            self.assertEqual(
                event.to_primitive(),
                {
                    'time': "20:33:05",
                    'aggressor': "Pe-8",
                    'pos': {
                        'x': 100.0,
                        'y': 200.99,
                    },
                    'name': "TreeWasDestroyedByAIAircraft",
                    'verbose_name': "Tree was destroyed by AI aircraft",
                }
            )

        _assert("[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by Pe-8 at 100.0 200.99")
        _assert("[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by Pe-8 at 100.0 200.99")

    def test_tree_was_destroyed(self):
        string = "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by at 100.0 200.99"
        event = self.string_to_event(string, grammar.tree_was_destroyed)
        self.assertIsInstance(event, structures.TreeWasDestroyed)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
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

    def test_static_was_destroyed(self):
        string = "[8:33:05 PM] 0_Static crashed at 100.0 200.99"
        event = self.string_to_event(string, grammar.static_was_destroyed)

        self.assertIsInstance(event, structures.StaticWasDestroyed)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "0_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "0_Static",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "StaticWasDestroyed",
                'verbose_name': "Static was destroyed",
            }
        )

    def test_static_was_destroyed_by_human_aircraft(self):
        string = "[8:33:05 PM] 0_Static destroyed by User0:Pe-8 at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.static_was_destroyed_by_human_aircraft
        )
        self.assertIsInstance(
            event,
            structures.StaticWasDestroyedByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "0_Static")
        self.assertEqual(event.aggressor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "0_Static",
                'aggressor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "StaticWasDestroyedByHumanAircraft",
                'verbose_name': "Static was destroyed by human aircraft",
            }
        )

    def test_static_was_destroyed_by_ai_aircraft(self):
        string = "[8:33:05 PM] 0_Static destroyed by Pe-8 at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.static_was_destroyed_by_ai_aircraft
        )
        self.assertIsInstance(
            event,
            structures.StaticWasDestroyedByAIAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "0_Static")
        self.assertEqual(event.aggressor, "Pe-8")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "0_Static",
                'aggressor': "Pe-8",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "StaticWasDestroyedByAIAircraft",
                'verbose_name': "Static was destroyed by AI aircraft",
            }
        )

    def test_static_was_destroyed_by_static(self):
        string = "[8:33:05 PM] 0_Static destroyed by 1_Static at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.static_was_destroyed_by_static
        )
        self.assertIsInstance(
            event,
            structures.StaticWasDestroyedByStatic
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "0_Static")
        self.assertEqual(event.aggressor, "1_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "0_Static",
                'aggressor': "1_Static",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "StaticWasDestroyedByStatic",
                'verbose_name': "Static was destroyed by static",
            }
        )

    def test_static_was_destroyed_by_moving_unit(self):
        string = "[8:33:05 PM] 0_Static destroyed by 0_Chief at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.static_was_destroyed_moving_unit
        )
        self.assertIsInstance(
            event,
            structures.StaticWasDestroyedByMovingUnit
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "0_Static")
        self.assertEqual(event.aggressor, "0_Chief")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "0_Static",
                'aggressor': "0_Chief",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "StaticWasDestroyedByMovingUnit",
                'verbose_name': "Static was destroyed by moving unit",
            }
        )

    def test_bridge_was_destroyed_by_human_aircraft(self):
        string = "[8:33:05 PM]  Bridge0 destroyed by User0:Pe-8 at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.bridge_was_destroyed_by_human_aircraft
        )
        self.assertIsInstance(
            event,
            structures.BridgeWasDestroyedByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Bridge0")
        self.assertEqual(event.aggressor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Bridge0",
                'aggressor': {
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

    def test_ai_aircraft_has_despawned(self):
        string = "[8:33:05 PM] Pe-8 removed at 100.0 200.99"
        event = self.string_to_event(string, grammar.ai_aircraft_has_despawned)

        self.assertIsInstance(event, structures.AIAircraftHasDespawned)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, "Pe-8")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': "Pe-8",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftHasDespawned",
                'verbose_name': "AI aircraft has despawned",
            }
        )

    def test_ai_aircraft_was_damaged_on_ground(self):
        string = "[8:33:05 PM] Pe-8 damaged on the ground at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_was_damaged_on_ground
        )

        self.assertIsInstance(event, structures.AIAircraftWasDamagedOnGround)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Pe-8")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Pe-8",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasDamagedOnGround",
                'verbose_name': "AI aircraft was damaged on ground",
            }
        )

    def test_ai_has_damaged_his_aircraft(self):

        def _assert(string):
            event = self.string_to_event(
                string,
                grammar.ai_has_damaged_his_aircraft
            )

            self.assertIsInstance(event, structures.AIHasDamagedHisAircraft)
            self.assertEqual(event.time, datetime.time(20, 33, 5))
            self.assertEqual(event.victim, "Pe-8")
            self.assertEqual(event.pos, Point2D(100.0, 200.99))
            self.assertEqual(
                event.to_primitive(),
                {
                    'time': "20:33:05",
                    'victim': "Pe-8",
                    'pos': {
                        'x': 100.0,
                        'y': 200.99,
                    },
                    'name': "AIHasDamagedHisAircraft",
                    'verbose_name': "AI has damaged his aircraft",
                },

            )

        _assert("[8:33:05 PM] Pe-8 damaged by landscape at 100.0 200.99")
        _assert("[8:33:05 PM] Pe-8 damaged by NONAME at 100.0 200.99")

    def test_ai_has_destroyed_his_aircraft(self):

        def _assert(string):
            event = self.string_to_event(
                string,
                grammar.ai_has_destroyed_his_aircraft
            )

            self.assertIsInstance(event, structures.AIHasDestroyedHisAircraft)
            self.assertEqual(event.time, datetime.time(20, 33, 5))
            self.assertEqual(event.victim, "Pe-8")
            self.assertEqual(event.pos, Point2D(100.0, 200.99))
            self.assertEqual(
                event.to_primitive(),
                {
                    'time': "20:33:05",
                    'victim': "Pe-8",
                    'pos': {
                        'x': 100.0,
                        'y': 200.99,
                    },
                    'name': "AIHasDestroyedHisAircraft",
                    'verbose_name': "AI has destroyed his aircraft",
                }
            )

        _assert("[8:33:05 PM] Pe-8 shot down by landscape at 100.0 200.99")
        _assert("[8:33:05 PM] Pe-8 shot down by NONAME at 100.0 200.99")

    def test_ai_aircraft_has_crashed(self):
        string = "[8:33:05 PM] Pe-8 crashed at 100.0 200.99"
        event = self.string_to_event(string, grammar.ai_aircraft_has_crashed)

        self.assertIsInstance(event, structures.AIAircraftHasCrashed)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Pe-8")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Pe-8",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftHasCrashed",
                'verbose_name': "AI aircraft has crashed",
            }
        )

    def test_ai_aircraft_has_landed(self):
        string = "[8:33:05 PM] Pe-8 landed at 100.0 200.99"
        event = self.string_to_event(string, grammar.ai_aircraft_has_landed)

        self.assertIsInstance(event, structures.AIAircraftHasLanded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, "Pe-8")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': "Pe-8",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftHasLanded",
                'verbose_name': "AI aircraft has landed",
            }
        )

    def test_ai_aircraft_was_damaged_by_human_aircraft(self):
        string = "[8:33:05 PM] Pe-8 damaged by User1:Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_was_damaged_by_human_aircraft
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftWasDamagedByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Pe-8")
        self.assertEqual(
            event.aggressor,
            HumanAircraft("User1", "Bf-109G-6_Late")
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Pe-8",
                'aggressor': {
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

    def test_ai_aircraft_was_damaged_by_ai_aircraft(self):
        string = "[8:33:05 PM] Pe-8 damaged by Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_was_damaged_by_ai_aircraft
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftWasDamagedByAIAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Pe-8")
        self.assertEqual(event.aggressor, "Bf-109G-6_Late")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Pe-8",
                'aggressor': "Bf-109G-6_Late",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasDamagedByAIAircraft",
                'verbose_name': "AI aircraft was damaged by AI aircraft",
            }
        )

    def test_ai_aircraft_was_shot_down_by_human_aircraft(self):
        string = "[8:33:05 PM] Pe-8 shot down by User1:Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_was_shot_down_by_human_aircraft
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftWasShotDownByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Pe-8")
        self.assertEqual(
            event.aggressor,
            HumanAircraft("User1", "Bf-109G-6_Late")
        )
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Pe-8",
                'aggressor': {
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

    def test_ai_aircraft_was_shot_down_by_ai_aircraft(self):
        string = "[8:33:05 PM] Pe-8 shot down by Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_was_shot_down_by_ai_aircraft
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftWasShotDownByAIAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Pe-8")
        self.assertEqual(event.aggressor, "Bf-109G-6_Late")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Pe-8",
                'aggressor': "Bf-109G-6_Late",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasShotDownByAIAircraft",
                'verbose_name': "AI aircraft was shot down by AI aircraft",
            }
        )

    def test_ai_aircraft_was_shot_down_by_static(self):
        string = "[8:33:05 PM] Pe-8 shot down by 0_Static at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_was_shot_down_by_static
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftWasShotDownByStatic
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Pe-8")
        self.assertEqual(event.aggressor, "0_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Pe-8",
                'aggressor': "0_Static",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasShotDownByStatic",
                'verbose_name': "AI aircraft was shot down by static",
            }
        )

    def test_ai_aircraft_was_shot_down_moving_unit_member(self):
        string = "[8:33:05 PM] Pe-8 shot down by 0_Chief0 at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_was_shot_down_by_moving_unit_member
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftWasShotDownByMovingUnitMember
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "Pe-8")
        self.assertEqual(event.aggressor, MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "Pe-8",
                'aggressor': {
                    'moving_unit': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftWasShotDownByMovingUnitMember",
                'verbose_name': "AI aircraft was shot down by moving unit "
                                "member",
            }
        )

    def test_ai_aircraft_crew_member_was_killed(self):
        string = "[8:33:05 PM] Pe-8(0) was killed at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_was_killed
        )
        self.assertIsInstance(event, structures.AIAircraftCrewMemberWasKilled)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasKilled",
                'verbose_name': "AI aircraft crew member was killed",
            }
        )

    def test_ai_aircraft_crew_member_was_killed_by_static(self):
        string = "[8:33:05 PM] Pe-8(0) was killed by 0_Static at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_was_killed_by_static
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftCrewMemberWasKilledByStatic
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.aggressor, "0_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'aggressor': "0_Static",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasKilledByStatic",
                'verbose_name': "AI aircraft crew member was killed by static",
            }
        )

    def test_ai_aircraft_crew_member_was_killed_by_ai_aircraft(self):
        string = "[8:33:05 PM] Pe-8(0) was killed by Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_was_killed_by_ai_aircraft
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftCrewMemberWasKilledByAIAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.aggressor, "Bf-109G-6_Late")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'aggressor': "Bf-109G-6_Late",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasKilledByAIAircraft",
                'verbose_name': "AI aircraft crew member was killed by "
                                "AI aircraft",
            }
        )

    def test_ai_aircraft_crew_member_was_killed_by_moving_unit_member(self):
        string = "[8:33:05 PM] Pe-8(0) was killed by 0_Chief0 at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_was_killed_by_moving_unit_member
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftCrewMemberWasKilledByMovingUnitMember
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.aggressor, MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'aggressor': {
                    'moving_unit': "0_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasKilledByMovingUnitMember",
                'verbose_name': "AI aircraft crew member was killed by "
                                "moving unit member",
            }
        )

    def test_ai_aircraft_crew_member_was_killed_in_parachute_by_ai_aircraft(self):
        string = "[8:33:05 PM] Pe-8(0) was killed in his chute by Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_was_killed_in_parachute_by_ai_aircraft
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftCrewMemberWasKilledInParachuteByAIAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.aggressor, "Bf-109G-6_Late")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'aggressor': "Bf-109G-6_Late",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasKilledInParachuteByAIAircraft",
                'verbose_name': "AI aircraft crew member was killed in "
                                "parachute by AI aircraft",
            }
        )

    def test_ai_aircraft_crew_member_parachute_was_destroyed_by_ai_aircraft(self):
        string = "[8:33:05 PM] Pe-8(0) has chute destroyed by Bf-109G-6_Late at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_parachute_was_destroyed_by_ai_aircraft
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftCrewMemberParachuteWasDestroyedByAIAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.aggressor, "Bf-109G-6_Late")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'aggressor': "Bf-109G-6_Late",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberParachuteWasDestroyedByAIAircraft",
                'verbose_name': "AI aircraft crew member's parachute was "
                                "destroyed by AI aircraft",
            }
        )

    def test_ai_aircraft_crew_member_parachute_was_destroyed(self):
        string = "[8:33:05 PM] Pe-8(0) has chute destroyed by at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_parachute_was_destroyed
        )
        self.assertIsInstance(
            event,
            structures.AIAircraftCrewMemberParachuteWasDestroyed
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberParachuteWasDestroyed",
                'verbose_name': "AI aircraft crew member's parachute was "
                                "destroyed",
            }
        )

    def test_ai_aircraft_crew_member_was_wounded(self):
        string = "[8:33:05 PM] Pe-8(0) was wounded at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_was_wounded
        )
        self.assertIsInstance(event, structures.AIAircraftCrewMemberWasWounded)
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasWounded",
                'verbose_name': "AI aircraft crew member was wounded",
            }
        )

    def test_ai_aircraft_crew_member_was_heavily_wounded(self):
        string = "[8:33:05 PM] Pe-8(0) was heavily wounded at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_was_heavily_wounded
        )
        self.assertIsInstance(
            event, structures.AIAircraftCrewMemberWasHeavilyWounded
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasHeavilyWounded",
                'verbose_name': "AI aircraft crew member was heavily wounded",
            }
        )

    def test_ai_aircraft_crew_member_was_captured(self):
        string = "[8:33:05 PM] Pe-8(0) was captured at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_was_captured
        )
        self.assertIsInstance(
            event, structures.AIAircraftCrewMemberWasCaptured
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberWasCaptured",
                'verbose_name': "AI aircraft crew member was captured",
            }
        )

    def test_ai_aircraft_crew_member_has_bailed_out(self):
        string = "[8:33:05 PM] Pe-8(0) bailed out at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_has_bailed_out
        )
        self.assertIsInstance(
            event, structures.AIAircraftCrewMemberHasBailedOut
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberHasBailedOut",
                'verbose_name': "AI aircraft crew member has bailed out",
            }
        )

    def test_ai_aircraft_crew_member_has_touched_down(self):
        string = "[8:33:05 PM] Pe-8(0) successfully bailed out at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.ai_aircraft_crew_member_has_touched_down
        )
        self.assertIsInstance(
            event, structures.AIAircraftCrewMemberHasTouchedDown
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.actor, AIAircraftCrewMember("Pe-8", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'actor': {
                    'aircraft': "Pe-8",
                    'seat_number': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "AIAircraftCrewMemberHasTouchedDown",
                'verbose_name': "AI aircraft crew member has touched down",
            }
        )

    def test_moving_unit_was_destroyed_by_moving_unit(self):
        string = "[8:33:05 PM] 0_Chief destroyed by 1_Chief at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.moving_unit_was_destroyed_by_moving_unit
        )
        self.assertIsInstance(
            event,
            structures.MovingUnitWasDestroyedByMovingUnit
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "0_Chief")
        self.assertEqual(event.aggressor, "1_Chief")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "0_Chief",
                'aggressor': "1_Chief",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitWasDestroyedByMovingUnit",
                'verbose_name': "Moving unit was destroyed by moving unit",
            }
        )

    def test_moving_unit_was_destroyed_by_moving_unit_member(self):
        string = "[8:33:05 PM] 0_Chief destroyed by 1_Chief0 at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.moving_unit_was_destroyed_by_moving_unit_member
        )
        self.assertIsInstance(
            event,
            structures.MovingUnitWasDestroyedByMovingUnitMember
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "0_Chief")
        self.assertEqual(event.aggressor, MovingUnitMember("1_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "0_Chief",
                'aggressor': {
                    'moving_unit': "1_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitWasDestroyedByMovingUnitMember",
                'verbose_name': "Moving unit was destroyed by moving unit "
                                "member",
            }
        )

    def test_moving_unit_was_destroyed_by_static(self):
        string = "[8:33:05 PM] 0_Chief destroyed by 0_Static at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.moving_unit_was_destroyed_by_static
        )
        self.assertIsInstance(
            event,
            structures.MovingUnitWasDestroyedByStatic
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, "0_Chief")
        self.assertEqual(event.aggressor, "0_Static")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': "0_Chief",
                'aggressor': "0_Static",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitWasDestroyedByStatic",
                'verbose_name': "Moving unit was destroyed by static",
            }
        )

    def test_moving_unit_member_was_destroyed_by_ai_aircraft(self):
        string = "[8:33:05 PM] 0_Chief0 destroyed by Pe-8 at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.moving_unit_member_was_destroyed_by_ai_aircraft
        )
        self.assertIsInstance(
            event,
            structures.MovingUnitMemberWasDestroyedByAIAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.aggressor, "Pe-8")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'moving_unit': "0_Chief",
                    'index': 0,
                },
                'aggressor': "Pe-8",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitMemberWasDestroyedByAIAircraft",
                'verbose_name': "Moving unit member was destroyed by "
                                "AI aircraft",
            }
        )

    def test_moving_unit_member_was_destroyed_by_human_aircraft(self):
        string = "[8:33:05 PM] 0_Chief0 destroyed by User0:Pe-8 at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.moving_unit_member_was_destroyed_by_human_aircraft
        )
        self.assertIsInstance(
            event,
            structures.MovingUnitMemberWasDestroyedByHumanAircraft
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.aggressor, HumanAircraft("User0", "Pe-8"))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'moving_unit': "0_Chief",
                    'index': 0,
                },
                'aggressor': {
                    'callsign': "User0",
                    'aircraft': "Pe-8",
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitMemberWasDestroyedByHumanAircraft",
                'verbose_name': "Moving unit member was destroyed by "
                                "human aircraft",
            }
        )

    def test_moving_unit_member_was_destroyed_by_moving_unit(self):
        string = "[8:33:05 PM] 0_Chief0 destroyed by 1_Chief at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.moving_unit_member_was_destroyed_by_moving_unit
        )
        self.assertIsInstance(
            event,
            structures.MovingUnitMemberWasDestroyedByMovingUnit
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.aggressor, "1_Chief")
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'moving_unit': "0_Chief",
                    'index': 0,
                },
                'aggressor': "1_Chief",
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitMemberWasDestroyedByMovingUnit",
                'verbose_name': "Moving unit member was destroyed by "
                                "moving unit",
            }
        )

    def test_moving_unit_member_was_destroyed_by_moving_unit_member(self):
        string = "[8:33:05 PM] 0_Chief0 destroyed by 1_Chief0 at 100.0 200.99"
        event = self.string_to_event(
            string,
            grammar.moving_unit_member_was_destroyed_by_moving_unit_member
        )
        self.assertIsInstance(
            event,
            structures.MovingUnitMemberWasDestroyedByMovingUnitMember
        )
        self.assertEqual(event.time, datetime.time(20, 33, 5))
        self.assertEqual(event.victim, MovingUnitMember("0_Chief", 0))
        self.assertEqual(event.aggressor, MovingUnitMember("1_Chief", 0))
        self.assertEqual(event.pos, Point2D(100.0, 200.99))
        self.assertEqual(
            event.to_primitive(),
            {
                'time': "20:33:05",
                'victim': {
                    'moving_unit': "0_Chief",
                    'index': 0,
                },
                'aggressor': {
                    'moving_unit': "1_Chief",
                    'index': 0,
                },
                'pos': {
                    'x': 100.0,
                    'y': 200.99,
                },
                'name': "MovingUnitMemberWasDestroyedByMovingUnitMember",
                'verbose_name': "Moving unit member was destroyed by "
                                "moving unit member",
            }
        )
