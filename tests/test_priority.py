# coding: utf-8

import unittest

from il2fb.parsers.events import events
from il2fb.parsers.events.priority import get_event_priority


class PriorityTestCase(unittest.TestCase):

    def test_ai_actor_is_less_prioritized_than_human_actor(self):
        self.assertGreater(
            get_event_priority(events.AIAircraftHasLanded),
            get_event_priority(events.HumanAircraftHasLanded),
        )

    def test_ai_actor_is_less_prioritized_than_other_actors(self):
        self.assertGreater(
            get_event_priority(events.AIAircraftWasShotDownByMovingUnit),
            get_event_priority(events.MovingUnitWasDestroyedByMovingUnit),
        )

    def test_human_actor_is_less_prioritized_than_other_actors(self):
        self.assertGreater(
            get_event_priority(events.AIAircraftHasLanded),
            get_event_priority(events.MovingUnitWasDestroyedByMovingUnit),
        )

    def test_other_actors_have_equal_prioriry(self):
        self.assertEqual(
            get_event_priority(events.StationaryUnitWasDestroyedByMovingUnit),
            get_event_priority(events.MovingUnitWasDestroyedByMovingUnit),
        )

    def test_other_events_have_equal_prioriry(self):
        self.assertEqual(
            get_event_priority(events.MissionIsPlaying),
            get_event_priority(events.TargetStateWasChanged),
        )

    def test_ai_attacker_is_less_prioritized_than_human_attacker(self):
        self.assertGreater(
            get_event_priority(events.StationaryUnitWasDestroyedByAIAircraft),
            get_event_priority(events.StationaryUnitWasDestroyedByHumanAircraft),
        )

    def test_ai_attacker_is_less_prioritized_than_other_attackers(self):
        self.assertGreater(
            get_event_priority(events.StationaryUnitWasDestroyedByAIAircraft),
            get_event_priority(events.StationaryUnitWasDestroyedByMovingUnit),
        )

    def test_human_attacker_is_less_prioritized_than_other_attackers(self):
        self.assertGreater(
            get_event_priority(events.StationaryUnitWasDestroyedByHumanAircraft),
            get_event_priority(events.StationaryUnitWasDestroyedByMovingUnit),
        )

    def test_other_attackers_have_equal_prioriry(self):
        self.assertEqual(
            get_event_priority(events.StationaryUnitWasDestroyedByStationaryUnit),
            get_event_priority(events.StationaryUnitWasDestroyedByMovingUnit),
        )

    def test_ai_assistant_is_less_prioritized_than_human_assistant(self):
        self.assertGreater(
            get_event_priority(events.AIAircraftWasShotDownByAIAircraftAndAIAircraft),
            get_event_priority(events.AIAircraftWasShotDownByAIAircraftAndHumanAircraft),
        )

    def test_priority_can_be_used_for_sorting(self):
        given = [
            events.BridgeWasDestroyedByAIAircraft,
            events.BridgeWasDestroyedByStationaryUnit,
            events.BridgeWasDestroyedByMovingUnitMember,
            events.BridgeWasDestroyedByMovingUnit,
            events.BridgeWasDestroyedByHumanAircraft,
        ]
        expected = [
            events.BridgeWasDestroyedByStationaryUnit,
            events.BridgeWasDestroyedByMovingUnitMember,
            events.BridgeWasDestroyedByMovingUnit,
            events.BridgeWasDestroyedByHumanAircraft,
            events.BridgeWasDestroyedByAIAircraft,
        ]
        result = sorted(given, key=get_event_priority)
        self.assertEqual(result, expected)
