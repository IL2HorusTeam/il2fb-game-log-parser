# -*- coding: utf-8 -*-

from operator import itemgetter
from six.moves import map

from il2fb.parsers.events import parse_string
from il2fb.parsers.events.exceptions import EventParsingError
from il2fb.parsers.events.structures import events

from .base import BaseTestCase


class ParserTestCase(BaseTestCase):

    def test_parse_string(self):
        data = [
            (
                events.MissionIsPlaying,
                "[Sep 15, 2013 8:33:05 PM] Mission: path/PH.mis is Playing"
            ),
            (
                events.MissionHasBegun,
                "[8:33:05 PM] Mission BEGIN"
            ),
            (
                events.MissionHasEnded,
                "[8:33:05 PM] Mission END"
            ),
            (
                events.MissionWasWon,
                "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"
            ),
            (
                events.MissionWasWon,
                "[Sep 15, 2013 8:33:05 PM] Mission: BLUE WON"
            ),
            (
                events.TargetStateWasChanged,
                "[8:33:05 PM] Target 3 Complete"
            ),
            (
                events.TargetStateWasChanged,
                "[8:33:05 PM] Target 4 Failed"
            ),
            (
                events.HumanHasConnected,
                "[8:33:05 PM] User0 has connected"
            ),
            (
                events.HumanAircraftHasCrashed,
                "[8:33:05 PM] User0:Pe-8 crashed at 100.0 200.99"
            ),
            (
                events.HumanHasDamagedHisAircraft,
                "[8:33:05 PM] User0:Pe-8 damaged by landscape at 100.0 200.99"
            ),
            (
                events.HumanHasDamagedHisAircraft,
                "[8:33:05 PM] User0:Pe-8 damaged by NONAME at 100.0 200.99"
            ),
            (
                events.HumanHasDestroyedHisAircraft,
                "[8:33:05 PM] User0:Pe-8 shot down by landscape at 100.0 200.99"
            ),
            (
                events.HumanHasDestroyedHisAircraft,
                "[8:33:05 PM] User0:Pe-8 shot down by NONAME at 100.0 200.99"
            ),
            (
                events.HumanHasDisconnected,
                "[8:33:05 PM] User0 has disconnected"
            ),
            (
                events.HumanAircraftHasLanded,
                "[8:33:05 PM] User0:Pe-8 landed at 100.0 200.99"
            ),
            (
                events.HumanHasSelectedAirfield,
                "[8:33:05 PM] User0 selected army Red at 100.0 200.99"
            ),
            (
                events.HumanAircraftHasSpawned,
                "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"
            ),
            (
                events.HumanAircraftHasTookOff,
                "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"
            ),
            (
                events.HumanHasWentToBriefing,
                "[8:33:05 PM] User0 entered refly menu"
            ),
            (
                events.HumanAircraftWasDamagedByHumanAircraft,
                "[8:33:05 PM] User0:Pe-8 damaged by User1:Bf-109G-6_Late at 100.0 200.99"
            ),
            (
                events.HumanAircraftWasDamagedByStatic,
                "[8:33:05 PM] User0:Pe-8 damaged by 0_Static at 100.0 200.99"
            ),
            (
                events.HumanAircraftWasDamagedByAIAircraft,
                "[8:33:05 PM] User0:Pe-8 damaged by Bf-109G-6_Late at 100.0 200.99"
            ),
            (
                events.HumanAircraftWasDamagedOnGround,
                "[8:33:05 PM] User0:Pe-8 damaged on the ground at 100.0 200.99"
            ),
            (
                events.HumanAircraftWasShotDownByHumanAircraft,
                "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-6_Late at 100.0 200.99"
            ),
            (
                events.HumanAircraftWasShotDownByStatic,
                "[8:33:05 PM] User0:Pe-8 shot down by 0_Static at 100.0 200.99"
            ),
            (
                events.HumanAircraftWasShotDownByAIAircraft,
                "[8:33:05 PM] User0:Pe-8 shot down by Bf-109G-6_Late at 100.0 200.99"
            ),
            (
                events.HumanHasToggledLandingLights,
                "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"
            ),
            (
                events.HumanHasToggledLandingLights,
                "[8:33:05 PM] User0:Pe-8 turned landing lights on at 100.0 200.99"
            ),
            (
                events.HumanHasToggledWingtipSmokes,
                "[8:33:05 PM] User0:Pe-8 turned wingtip smokes off at 100.0 200.99"
            ),
            (
                events.HumanHasToggledWingtipSmokes,
                "[8:33:05 PM] User0:Pe-8 turned wingtip smokes on at 100.0 200.99"
            ),
            (
                events.HumanAircraftCrewMemberHasBailedOut,
                "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"
            ),
            (
                events.HumanAircraftCrewMemberHasTouchedDown,
                "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"
            ),
            (
                events.HumanAircraftCrewMemberWasCaptured,
                "[8:33:05 PM] User0:Pe-8(0) was captured at 100.0 200.99"
            ),
            (
                events.HumanAircraftCrewMemberWasHeavilyWounded,
                "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"
            ),
            (
                events.HumanAircraftCrewMemberWasKilled,
                "[8:33:05 PM] User0:Pe-8(0) was killed at 100.0 200.99"
            ),
            (
                events.HumanAircraftCrewMemberWasKilledByHumanAircraft,
                "[8:33:05 PM] User0:Pe-8(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"
            ),
            (
                events.HumanAircraftCrewMemberWasKilledByStatic,
                "[8:33:05 PM] User0:Pe-8(0) was killed by 0_Static at 100.0 200.99"
            ),
            (
                events.HumanAircraftCrewMemberWasWounded,
                "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"
            ),
            (
                events.HumanHasChangedSeat,
                "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"
            ),
            (
                events.StaticWasDestroyed,
                "[8:33:05 PM] 0_Static crashed at 100.0 200.99"
            ),
            (
                events.StaticWasDestroyedByStatic,
                "[8:33:05 PM] 0_Static destroyed by 1_Static at 100.0 200.99"
            ),
            (
                events.StaticWasDestroyedByHumanAircraft,
                "[8:33:05 PM] 0_Static destroyed by User0:Pe-8 at 100.0 200.99"
            ),
            (
                events.StaticWasDestroyedByAIAircraft,
                "[8:33:05 PM] 0_Static destroyed by Pe-8 at 100.0 200.99"
            ),
            (
                events.BuildingWasDestroyedByHumanAircraft,
                "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
            ),
            (
                events.BridgeWasDestroyedByHumanAircraft,
                "[8:33:05 PM]  Bridge0 destroyed by User0:Pe-8 at 100.0 200.99"
            ),
            (
                events.TreeWasDestroyedByHumanAircraft,
                "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
            ),
            (
                events.TreeWasDestroyedByHumanAircraft,
                "[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by User0:Pe-8 at 100.0 200.99"
            ),
            (
                events.AIAircraftHasDespawned,
                "[8:33:05 PM] Pe-8 removed at 100.0 200.99"
            ),
            (
                events.AIAircraftWasDamagedOnGround,
                "[8:33:05 PM] Pe-8 damaged on the ground at 100.0 200.99"
            ),
            (
                events.AIAircraftWasDamagedByHumanAircraft,
                "[8:33:05 PM] Pe-8 damaged by User1:Bf-109G-6_Late at 100.0 200.99"
            ),
            (
                events.AIAircraftWasDamagedByAIAircraft,
                "[8:33:05 PM] Pe-8 damaged by Bf-109G-6_Late at 100.0 200.99"
            ),
            (
                events.AIHasDamagedHisAircraft,
                "[8:33:05 PM] Pe-8 damaged by landscape at 100.0 200.99"
            ),
            (
                events.AIHasDamagedHisAircraft,
                "[8:33:05 PM] Pe-8 damaged by NONAME at 100.0 200.99"
            ),
            (
                events.AIHasDestroyedHisAircraft,
                "[8:33:05 PM] Pe-8 shot down by landscape at 100.0 200.99"
            ),
            (
                events.AIHasDestroyedHisAircraft,
                "[8:33:05 PM] Pe-8 shot down by NONAME at 100.0 200.99"
            ),
            (
                events.AIAircraftHasCrashed,
                "[8:33:05 PM] Pe-8 crashed at 100.0 200.99"
            ),
            (
                events.AIAircraftHasLanded,
                "[8:33:05 PM] Pe-8 landed at 100.0 200.99"
            ),
            (
                events.AIAircraftWasShotDownByHumanAircraft,
                "[8:33:05 PM] Pe-8 shot down by User1:Bf-109G-6_Late at 100.0 200.99"
            ),
            (
                events.AIAircraftWasShotDownByStatic,
                "[8:33:05 PM] Pe-8 shot down by 0_Static at 100.0 200.99"
            ),
            (
                events.AIAircraftCrewMemberWasWounded,
                "[8:33:05 PM] Pe-8(0) was wounded at 100.0 200.99"
            ),
            (
                events.AIAircraftCrewMemberWasHeavilyWounded,
                "[8:33:05 PM] Pe-8(0) was heavily wounded at 100.0 200.99"
            ),
            (
                events.AIAircraftCrewMemberWasKilled,
                "[8:33:05 PM] Pe-8(0) was killed at 100.0 200.99"
            ),
            (
                events.AIAircraftCrewMemberWasKilledByStatic,
                "[8:33:05 PM] Pe-8(0) was killed by 0_Static at 100.0 200.99"
            ),
            (
                events.AIAircraftCrewMemberWasKilledInParachuteByAIAircraft,
                "[8:33:05 PM] Pe-8(0) was killed in his chute by Bf-109G-6_Late at 100.0 200.99"
            ),
            (
                events.AIAircraftCrewMemberParachuteWasDestroyedByAIAircraft,
                "[8:33:05 PM] Pe-8(0) has chute destroyed by Bf-109G-6_Late at 100.0 200.99"
            ),
            (
                events.AIAircraftCrewMemberHasBailedOut,
                "[8:33:05 PM] Pe-8(0) bailed out at 100.0 200.99"
            ),
            (
                events.AIAircraftCrewMemberHasTouchedDown,
                "[8:33:05 PM] Pe-8(0) successfully bailed out at 100.0 200.99"
            ),
        ]

        # Ensure we test all known events
        tested_events = map(itemgetter(0), data)
        tested_events = map(lambda x: x.__name__, tested_events)
        self.assertEqual(set(tested_events), set(events.__all__))

        for structure, string in data:
            event = parse_string(string)
            self.assertIsInstance(event, structure)

    def test_parse_string_with_unexpected_data(self):
        string = "foo bar baz quz"
        try:
            parse_string(string)
        except EventParsingError:
            pass
        else:
            self.fail("Parsing '{0}' was expected to raise {1}"
                      .format(string), EventParsingError.__name__)
