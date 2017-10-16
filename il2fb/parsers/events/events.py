# coding: utf-8
"""
Data structures for events.

"""

import inspect
import sys

from il2fb.commons.events import ParsableEvent
from il2fb.commons.regex import (
    WHITESPACE, NON_WHITESPACES, NUMBER, END_OF_STRING,
    make_matcher, named_group,
)
from il2fb.commons.transformers import (
    get_int_transformer, transform_belligerent, transform_2d_pos,
)

from .constants import TARGET_STATES
from .l10n import translations
from .regex import (
    DATE_TIME_GROUP_PREFIX, TIME_GROUP_PREFIX, BELLIGERENT_GROUP,
    TARGET_STATE_GROUP, TOGGLE_VALUE_GROUP, POS_GROUP_SUFFIX,
    CALLSIGN, HIMSELF, HUMAN_ACTOR_GROUP, HUMAN_AIRCRAFT_ACTOR_GROUP,
    HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP, HUMAN_AIRCRAFT_ATTACKER_GROUP,
    HUMAN_AIRCRAFT_ASSISTANT_GROUP,
    STATIONARY_UNIT_ACTOR_GROUP, STATIONARY_UNIT_ATTACKER_GROUP,
    MOVING_UNIT_ACTOR_GROUP, MOVING_UNIT_ATTACKER_GROUP,
    MOVING_UNIT_MEMBER_ACTOR_GROUP, MOVING_UNIT_MEMBER_ATTACKER_GROUP,
    AI_AIRCRAFT_ACTOR_GROUP, AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
    AI_AIRCRAFT_ATTACKER_GROUP, AI_AIRCRAFT_ASSISTANT_GROUP,
    BUILDING_ACTOR_GROUP, BRIDGE_ACTOR_GROUP, TREE,
)
from .transformers import (
    transform_date, transform_time,
    transform_human_as_actor,
    transform_human_aircraft_as_actor,
    transform_human_aircraft_as_attacker,
    transform_human_aircraft_as_assistant,
    transform_human_aircraft_crew_member_as_actor,
    transform_ai_aircraft_as_actor,
    transform_ai_aircraft_as_attacker,
    transform_ai_aircraft_as_assistant,
    transform_ai_aircraft_crew_member_as_seat,
    transform_ai_aircraft_crew_member_as_actor,
    transform_moving_unit_as_actor,
    transform_moving_unit_as_attacker,
    transform_moving_unit_member_as_actor,
    transform_moving_unit_member_as_attacker,
    transform_stationary_unit_as_actor,
    transform_stationary_unit_as_attacker,
    transform_building_as_actor,
    transform_bridge_as_actor,
)


_ = translations.ugettext_lazy


def get_all_events():
    module = sys.modules[__name__]
    members = inspect.getmembers(module, inspect.isclass)
    return [
        cls for name, cls in members
        if issubclass(cls, ParsableEvent) and cls is not ParsableEvent
    ]


class MissionIsPlaying(ParsableEvent):
    """
    Example:

        "[Sep 15, 2013 8:33:05 PM] Mission: PH.mis is Playing"

    """
    __slots__ = ['date', 'time', 'mission', ]

    verbose_name = _("Mission is playing")
    matcher = make_matcher(
        "{datetime}Mission:{s}{mission}{s}is{s}Playing{end}"
        .format(
            datetime=DATE_TIME_GROUP_PREFIX,
            mission=named_group('mission', ".+\.mis"),
            s=WHITESPACE,
            end=END_OF_STRING,
        )
    )
    transformers = (
        transform_date,
        transform_time,
    )


class MissionHasBegun(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] Mission BEGIN"

    """
    __slots__ = ['time', ]

    verbose_name = _("Mission has begun")
    matcher = make_matcher(
        "{time}Mission{s}BEGIN{end}"
        .format(
            time=TIME_GROUP_PREFIX,
            s=WHITESPACE,
            end=END_OF_STRING,
        )
    )
    transformers = (
        transform_time,
    )


class MissionHasEnded(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] Mission END"

    """
    __slots__ = ['time', ]

    verbose_name = _("Mission has ended")
    matcher = make_matcher(
        "{time}Mission{s}END{end}"
        .format(
            time=TIME_GROUP_PREFIX,
            s=WHITESPACE,
            end=END_OF_STRING,
        )
    )
    transformers = (
        transform_time,
    )


class MissionWasWon(ParsableEvent):
    """
    Example:

        "[Sep 15, 2013 8:33:05 PM] Mission: RED WON"

    """
    __slots__ = ['date', 'time', 'belligerent', ]

    verbose_name = _("Mission was won")
    matcher = make_matcher(
        "{datetime}Mission:{s}{belligerent}{s}WON{end}"
        .format(
            datetime=DATE_TIME_GROUP_PREFIX,
            belligerent=BELLIGERENT_GROUP,
            s=WHITESPACE,
            end=END_OF_STRING,
        )
    )
    transformers = (
        transform_date,
        transform_time,
        transform_belligerent,
    )


class TargetStateWasChanged(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] Target 3 Complete"

    """
    __slots__ = ['time', 'index', 'state', ]

    verbose_name = _("Target state was changed")
    STATES = TARGET_STATES
    matcher = make_matcher(
        "{time}Target{s}{index}{s}{state}{end}"
        .format(
            time=TIME_GROUP_PREFIX,
            index=named_group('index', NUMBER),
            state=TARGET_STATE_GROUP,
            s=WHITESPACE,
            end=END_OF_STRING,
        )
    )
    transformers = (
        transform_time,
        get_int_transformer('index'),
    )


class HumanHasConnected(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0 has connected"

    """
    __slots__ = ['time', 'actor', ]

    verbose_name = _("Human has connected")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}connected{end}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_ACTOR_GROUP,
            s=WHITESPACE,
            end=END_OF_STRING,
        )
    )
    transformers = (
        transform_time,
        transform_human_as_actor,
    )


class HumanHasDisconnected(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0 has disconnected"

    """
    __slots__ = ['time', 'actor', ]

    verbose_name = _("Human has disconnected")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}disconnected{end}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_ACTOR_GROUP,
            s=WHITESPACE,
            end=END_OF_STRING,
        )
    )
    transformers = (
        transform_time,
        transform_human_as_actor,
    )


class HumanHasSelectedAirfield(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0 selected army Red at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'belligerent', 'pos', ]

    verbose_name = _("Human has selected airfield")
    matcher = make_matcher(
        "{time}{actor}{s}selected{s}army{s}{belligerent}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_ACTOR_GROUP,
            belligerent=BELLIGERENT_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_as_actor,
        transform_belligerent,
        transform_2d_pos,
    )


class HumanAircraftHasSpawned(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 loaded weapons '40fab100' fuel 40%"

    """
    __slots__ = ['time', 'actor', 'weapons', 'fuel', ]

    verbose_name = _("Human aircraft has spawned")
    matcher = make_matcher(
        "{time}{actor}{s}loaded{s}weapons{s}\'{weapons}\'{s}fuel{s}{fuel}%{end}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            weapons=named_group('weapons', NON_WHITESPACES),
            fuel=named_group('fuel', "\d{2,3}"),
            s=WHITESPACE,
            end=END_OF_STRING,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        get_int_transformer('fuel'),
    )


class HumanHasWentToBriefing(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0 entered refly menu"

    """
    __slots__ = ['time', 'actor', ]

    verbose_name = _("Human has went to briefing")
    matcher = make_matcher(
        "{time}{actor}{s}entered{s}refly{s}menu{end}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_ACTOR_GROUP,
            s=WHITESPACE,
            end=END_OF_STRING,
        )
    )
    transformers = (
        transform_time,
        transform_human_as_actor,
    )


class HumanHasToggledLandingLights(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 turned landing lights off at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'value', 'pos', ]

    verbose_name = _("Human has toggled landing lights")
    matcher = make_matcher(
        "{time}{actor}{s}turned{s}landing{s}lights{s}{value}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            value=TOGGLE_VALUE_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_2d_pos,
    )


class HumanHasToggledWingtipSmokes(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 turned wingtip smokes off at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'value', 'pos', ]

    verbose_name = _("Human has toggled wingtip smokes")
    matcher = make_matcher(
        "{time}{actor}{s}turned{s}wingtip{s}smokes{s}{value}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            value=TOGGLE_VALUE_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_2d_pos,
    )


class HumanHasChangedSeat(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) seat occupied by User0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human has changed seat")
    matcher = make_matcher(
        "{time}{actor}{s}seat{s}occupied{s}by{s}{callsign}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            callsign=CALLSIGN,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class HumanIsTryingToTakeSeat(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0 is trying to occupy seat USN_VF_51A020(0)"

    """
    __slots__ = ['time', 'actor', 'seat', ]

    verbose_name = _("Human is trying to take seat")
    matcher = make_matcher(
        "{time}{actor}{s}is{s}trying{s}to{s}occupy{s}seat{s}{seat}{end}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_ACTOR_GROUP,
            seat=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            s=WHITESPACE,
            end=END_OF_STRING,
        )
    )
    transformers = (
        transform_time,
        transform_human_as_actor,
        transform_ai_aircraft_crew_member_as_seat,
    )


class HumanAircraftHasTookOff(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 in flight at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft has took off")
    matcher = make_matcher(
        "{time}{actor}{s}in{s}flight{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_2d_pos,
    )


class HumanAircraftHasLanded(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 landed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft has landed")
    matcher = make_matcher(
        "{time}{actor}{s}landed{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_2d_pos,
    )


class HumanAircraftHasCrashed(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 crashed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft has crashed")
    matcher = make_matcher(
        "{time}{actor}{s}crashed{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_2d_pos,
    )


class HumanHasDestroyedOwnAircraft(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] User0:Pe-8 shot down by landscape at 100.0 200.99"
        "[8:33:05 PM] User0:Pe-8 shot down by NONAME at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human has destroyed own aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{himself}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            himself=HIMSELF,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_2d_pos,
    )


class HumanHasDamagedOwnAircraft(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] User0:Pe-8 damaged by landscape at 100.0 200.99"
        "[8:33:05 PM] User0:Pe-8 damaged by NONAME at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human has damaged own aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{himself}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            himself=HIMSELF,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_2d_pos,
    )


class HumanAircraftWasDamagedOnGround(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 damaged on the ground at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft was damaged on the ground")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}on{s}the{s}ground{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_2d_pos,
    )


class HumanAircraftWasDamagedByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 damaged by User1:Bf-109G-6_Late at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was damaged by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftWasDamagedByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 damaged by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was damaged by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftWasDamagedByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 damaged by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was damaged by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftWasDamagedByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 damaged by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was damaged by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftWasDamagedByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 damaged by r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was damaged by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftWasShotDownByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-6_Late at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was shot down by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftWasShotDownByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was shot down by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftWasShotDownByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was shot down by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftWasShotDownByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was shot down by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftWasShotDownByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft was shot down by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftWasShotDownByHumanAircraftAndHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-2 and User2:Bf-109G-2 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'assistant', 'pos', ]

    verbose_name = _("Human aircraft was shot down by human aircraft and human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{s}and{s}{assistant}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            assistant=HUMAN_AIRCRAFT_ASSISTANT_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_human_aircraft_as_attacker,
        transform_human_aircraft_as_assistant,
        transform_2d_pos,
    )


class HumanAircraftWasShotDownByHumanAircraftAndAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by User1:Bf-109G-2 and r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'assistant', 'pos', ]

    verbose_name = _("Human aircraft was shot down by human aircraft and AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{s}and{s}{assistant}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            assistant=AI_AIRCRAFT_ASSISTANT_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_human_aircraft_as_attacker,
        transform_ai_aircraft_as_assistant,
        transform_2d_pos,
    )


class HumanAircraftWasShotDownByAIAircraftAndHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by r01000 and User1:Bf-109G-2 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'assistant', 'pos', ]

    verbose_name = _("Human aircraft was shot down by AI aircraft and human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{s}and{s}{assistant}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            assistant=HUMAN_AIRCRAFT_ASSISTANT_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_human_aircraft_as_assistant,
        transform_2d_pos,
    )


class HumanAircraftWasShotDownByAIAircraftAndAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8 shot down by r01000 and r01001 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'assistant', 'pos', ]

    verbose_name = _("Human aircraft was shot down by AI aircraft and AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{s}and{s}{assistant}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            assistant=AI_AIRCRAFT_ASSISTANT_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_ai_aircraft_as_assistant,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberHasBailedOut(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) bailed out at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member has bailed out")
    matcher = make_matcher(
        "{time}{actor}{s}bailed{s}out{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberHasLanded(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) successfully bailed out at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member has landed")
    matcher = make_matcher(
        "{time}{actor}{s}successfully{s}bailed{s}out{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasCaptured(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was captured at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member was captured")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}captured{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasWounded(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was wounded at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member was wounded")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}wounded{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasHeavilyWounded(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was heavily wounded at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member was heavily wounded")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}heavily{s}wounded{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasKilled(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasKilledByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasKilledByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasKilledByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasKilledByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasKilledByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed by r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasKilledInParachuteByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed in his chute by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed in parachute by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}in{s}his{s}chute{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasKilledInParachuteByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed in his chute by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed in parachute by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}in{s}his{s}chute{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasKilledInParachuteByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed in his chute by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed in parachute by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}in{s}his{s}chute{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasKilledInParachuteByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed in his chute by User1:Bf-109G-2 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed in parachute by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}in{s}his{s}chute{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberWasKilledInParachuteByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) was killed in his chute by r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member was killed in parachute by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}in{s}his{s}chute{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberParachuteWasDestroyedByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) has chute destroyed by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member's parachute was destroyed by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}chute{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) has chute destroyed by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member's parachute was destroyed by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}chute{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberParachuteWasDestroyedByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) has chute destroyed by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member's parachute was destroyed by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}chute{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberParachuteWasDestroyedByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) has chute destroyed by User1:Bf-109G-2 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member's parachute was destroyed by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}chute{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class HumanAircraftCrewMemberParachuteWasDestroyedByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] User0:Pe-8(0) has chute destroyed by r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Human aircraft crew member's parachute was destroyed by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}chute{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_crew_member_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class BuildingWasDestroyedByHumanAircraft(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
        "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/mono.sim destroyed by User1:Pe-8 at 300.0 400.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Building was destroyed by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=BUILDING_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_building_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class BuildingWasDestroyedByStationaryUnit(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by 0_Static at 100.0 200.99"
        "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/mono.sim destroyed by 1_Static at 300.0 400.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Building was destroyed by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=BUILDING_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_building_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class BuildingWasDestroyedByMovingUnitMember(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by 0_Chief0 at 100.0 200.99"
        "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/mono.sim destroyed by 1_Chief0 at 300.0 400.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Building was destroyed by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=BUILDING_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_building_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class BuildingWasDestroyedByMovingUnit(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by 0_Chief at 100.0 200.99"
        "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/mono.sim destroyed by 1_Chief at 300.0 400.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Building was destroyed by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=BUILDING_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_building_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class BuildingWasDestroyedByAIAircraft(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by r01000 at 100.0 200.99"
        "[8:33:05 PM] 3do/Buildings/Russia/Piter/House3_W/mono.sim destroyed by r01001 at 300.0 400.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Building was destroyed by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=BUILDING_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_building_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class TreeWasDestroyedByHumanAircraft(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by User0:Pe-8 at 100.0 200.99"
        "[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by User0:Pe-8 at 100.0 200.99"

    """
    __slots__ = ['time', 'attacker', 'pos', ]

    verbose_name = _("Tree was destroyed by human aircraft")
    matcher = make_matcher(
        "{time}{tree}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            tree=TREE,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class TreeWasDestroyedByStationaryUnit(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by 0_Static at 100.0 200.99"
        "[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'attacker', 'pos', ]

    verbose_name = _("Tree was destroyed by stationary unit")
    matcher = make_matcher(
        "{time}{tree}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            tree=TREE,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class TreeWasDestroyedByAIAircraft(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by r01000 at 100.0 200.99"
        "[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by r01001 at 100.0 200.99"

    """
    __slots__ = ['time', 'attacker', 'pos', ]

    verbose_name = _("Tree was destroyed by AI aircraft")
    matcher = make_matcher(
        "{time}{tree}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            tree=TREE,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class TreeWasDestroyedByMovingUnitMember(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by 0_Chief0 at 100.0 200.99"
        "[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by 0_Chief1 at 100.0 200.99"

    """
    __slots__ = ['time', 'attacker', 'pos', ]

    verbose_name = _("Tree was destroyed by moving unit member")
    matcher = make_matcher(
        "{time}{tree}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            tree=TREE,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class TreeWasDestroyedByMovingUnit(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by 0_Chief at 100.0 200.99"
        "[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by 1_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'attacker', 'pos', ]

    verbose_name = _("Tree was destroyed by moving unit")
    matcher = make_matcher(
        "{time}{tree}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            tree=TREE,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class TreeWasDestroyed(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] 3do/Tree/Line_W/live.sim destroyed by at 100.0 200.99"
        "[8:33:05 PM] 3do/Tree/Line_W/mono.sim destroyed by at 100.0 200.99"

    """
    __slots__ = ['time', 'pos', ]

    verbose_name = _("Tree was destroyed")
    matcher = make_matcher(
        "{time}{tree}{s}destroyed{s}by{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            tree=TREE,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_2d_pos,
    )


class StationaryUnitWasDestroyed(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Static crashed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("Stationary unit was destroyed")
    matcher = make_matcher(
        "{time}{actor}{s}crashed{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=STATIONARY_UNIT_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_stationary_unit_as_actor,
        transform_2d_pos,
    )


class StationaryUnitWasDestroyedByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Static destroyed by 1_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Stationary unit was destroyed by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=STATIONARY_UNIT_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_stationary_unit_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class StationaryUnitWasDestroyedByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Static destroyed by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Stationary unit was destroyed by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=STATIONARY_UNIT_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_stationary_unit_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class StationaryUnitWasDestroyedByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Static destroyed by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Stationary unit was destroyed by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=STATIONARY_UNIT_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_stationary_unit_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class StationaryUnitWasDestroyedByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Static destroyed by User0:Pe-8 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Stationary unit was destroyed by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=STATIONARY_UNIT_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_stationary_unit_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class StationaryUnitWasDestroyedByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Static destroyed by r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Stationary unit was destroyed by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=STATIONARY_UNIT_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_stationary_unit_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class BridgeWasDestroyedByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM]  Bridge0 destroyed by User0:Pe-8 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Bridge was destroyed by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=BRIDGE_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_bridge_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class BridgeWasDestroyedByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM]  Bridge0 destroyed by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Bridge was destroyed by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=BRIDGE_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_bridge_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class BridgeWasDestroyedByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM]  Bridge0 destroyed by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Bridge was destroyed by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=BRIDGE_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_bridge_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class BridgeWasDestroyedByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM]  Bridge0 destroyed by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Bridge was destroyed by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=BRIDGE_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_bridge_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class BridgeWasDestroyedByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM]  Bridge0 destroyed by r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Bridge was destroyed by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=BRIDGE_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_bridge_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class MovingUnitWasDestroyedByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Chief destroyed by 1_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Moving unit was destroyed by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=MOVING_UNIT_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class MovingUnitWasDestroyedByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Chief destroyed by 1_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Moving unit was destroyed by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=MOVING_UNIT_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class MovingUnitWasDestroyedByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Chief destroyed by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Moving unit was destroyed by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=MOVING_UNIT_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class MovingUnitWasDestroyedByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Chief destroyed by User0:Pe-8 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Moving unit was destroyed by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=MOVING_UNIT_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class MovingUnitWasDestroyedByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Chief destroyed by r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Moving unit was destroyed by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=MOVING_UNIT_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class MovingUnitMemberWasDestroyedByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Chief0 destroyed by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Moving unit member was destroyed by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=MOVING_UNIT_MEMBER_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_member_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class MovingUnitMemberWasDestroyedByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Chief0 destroyed by r01000 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Moving unit member was destroyed by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=MOVING_UNIT_MEMBER_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_member_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class MovingUnitMemberWasDestroyedByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Chief0 destroyed by User0:Pe-8 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Moving unit member was destroyed by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=MOVING_UNIT_MEMBER_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_member_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class MovingUnitMemberWasDestroyedByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Chief0 destroyed by 1_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Moving unit member was destroyed by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=MOVING_UNIT_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_member_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class MovingUnitMemberWasDestroyedByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] 0_Chief0 destroyed by 1_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("Moving unit member was destroyed by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=MOVING_UNIT_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_moving_unit_member_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class AIAircraftHasDespawned(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 removed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI aircraft has despawned")
    matcher = make_matcher(
        "{time}{actor}{s}removed{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_2d_pos,
    )


class AIAircraftWasDamagedOnGround(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 damaged on the ground at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI aircraft was damaged on the ground")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}on{s}the{s}ground{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_2d_pos,
    )


class AIAircraftWasDamagedByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 damaged by User1:Bf-109G-6_Late at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft was damaged by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class AIAircraftWasDamagedByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 damaged by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft was damaged by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class AIAircraftWasDamagedByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 damaged by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft was damaged by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class AIAircraftWasDamagedByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 damaged by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft was damaged by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class AIAircraftWasDamagedByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 damaged by r01001 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft was damaged by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class AIHasDamagedOwnAircraft(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] r01000 damaged by landscape at 100.0 200.99"
        "[8:33:05 PM] r01000 damaged by NONAME at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI has damaged own aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}damaged{s}by{s}{himself}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            himself=HIMSELF,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_2d_pos,
    )


class AIHasDestroyedOwnAircraft(ParsableEvent):
    """
    Examples:

        "[8:33:05 PM] r01000 shot down by landscape at 100.0 200.99"
        "[8:33:05 PM] r01000 shot down by NONAME at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI has destroyed own aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{himself}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            himself=HIMSELF,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_2d_pos,
    )


class AIAircraftHasLanded(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 landed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI aircraft has landed")
    matcher = make_matcher(
        "{time}{actor}{s}landed{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_2d_pos,
    )


class AIAircraftHasCrashed(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 crashed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI aircraft has crashed")
    matcher = make_matcher(
        "{time}{actor}{s}crashed{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_2d_pos,
    )


class AIAircraftWasShotDownByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 shot down by User1:Bf-109G-6_Late at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft was shot down by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class AIAircraftWasShotDownByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 shot down by r01001 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft was shot down by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class AIAircraftWasShotDownByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 shot down by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft was shot down by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class AIAircraftWasShotDownByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 shot down by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft was shot down by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class AIAircraftWasShotDownByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 shot down by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft was shot down by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class AIAircraftWasShotDownByAIAircraftAndAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 shot down by r01001 and r01002 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'assistant', 'pos', ]

    verbose_name = _("AI aircraft was shot down by AI aircraft and AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{s}and{s}{assistant}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            assistant=AI_AIRCRAFT_ASSISTANT_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_ai_aircraft_as_assistant,
        transform_2d_pos,
    )


class AIAircraftWasShotDownByHumanAircraftAndAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 shot down by User0:Bf-109G-2 and r01001 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'assistant', 'pos', ]

    verbose_name = _("AI aircraft was shot down by human aircraft and AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{s}and{s}{assistant}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            assistant=AI_AIRCRAFT_ASSISTANT_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_human_aircraft_as_attacker,
        transform_ai_aircraft_as_assistant,
        transform_2d_pos,
    )


class AIAircraftWasShotDownByAIAircraftAndHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 shot down by r01001 and User0:Bf-109G-2 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'assistant', 'pos', ]

    verbose_name = _("AI aircraft was shot down by AI aircraft and human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{s}and{s}{assistant}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            assistant=HUMAN_AIRCRAFT_ASSISTANT_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_human_aircraft_as_assistant,
        transform_2d_pos,
    )


class AIAircraftWasShotDownByHumanAircraftAndHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000 shot down by User0:Bf-109G-2 and User1:Bf-109G-2 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'assistant', 'pos', ]

    verbose_name = _("AI aircraft was shot down by human aircraft and human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}shot{s}down{s}by{s}{attacker}{s}and{s}{assistant}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            assistant=HUMAN_AIRCRAFT_ASSISTANT_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_as_actor,
        transform_human_aircraft_as_attacker,
        transform_human_aircraft_as_assistant,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasKilled(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was killed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI aircraft crew member was killed")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasKilledByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was killed by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member was killed by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasKilledByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was killed by User1:Bf-109G-6_Late at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member was killed by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasKilledByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was killed by r01001 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member was killed by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasKilledByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was killed by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member was killed by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasKilledByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was killed by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member was killed by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasKilledInParachuteByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was killed in his chute by r01001 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member was killed in parachute by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}in{s}his{s}chute{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasKilledInParachuteByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was killed in his chute by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member was killed in parachute by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}in{s}his{s}chute{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasKilledInParachuteByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was killed in his chute by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member was killed in parachute by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}in{s}his{s}chute{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasKilledInParachuteByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was killed in his chute by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member was killed in parachute by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}in{s}his{s}chute{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasKilledInParachuteByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was killed in his chute by User0:Pe-8 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member was killed in parachute by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}killed{s}in{s}his{s}chute{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberParachuteWasDestroyedByAIAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) has chute destroyed by r01001 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member's parachute was destroyed by AI aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}chute{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=AI_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_ai_aircraft_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberParachuteWasDestroyedByStationaryUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) has chute destroyed by 0_Static at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member's parachute was destroyed by stationary unit")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}chute{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=STATIONARY_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_stationary_unit_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberParachuteWasDestroyedByMovingUnitMember(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) has chute destroyed by 0_Chief0 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member's parachute was destroyed by moving unit member")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}chute{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_MEMBER_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_moving_unit_member_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberParachuteWasDestroyedByMovingUnit(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) has chute destroyed by 0_Chief at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member's parachute was destroyed by moving unit")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}chute{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=MOVING_UNIT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_moving_unit_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberParachuteWasDestroyedByHumanAircraft(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) has chute destroyed by User0:Bf-109G-2 at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'attacker', 'pos', ]

    verbose_name = _("AI aircraft crew member's parachute was destroyed by human aircraft")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}chute{s}destroyed{s}by{s}{attacker}{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            attacker=HUMAN_AIRCRAFT_ATTACKER_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_human_aircraft_as_attacker,
        transform_2d_pos,
    )


class AIAircraftCrewMemberParachuteWasDestroyed(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) has chute destroyed at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI aircraft crew member's parachute was destroyed")
    matcher = make_matcher(
        "{time}{actor}{s}has{s}chute{s}destroyed{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasWounded(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was wounded at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI aircraft crew member was wounded")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}wounded{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasHeavilyWounded(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was heavily wounded at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI aircraft crew member was heavily wounded")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}heavily{s}wounded{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class AIAircraftCrewMemberWasCaptured(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) was captured at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI aircraft crew member was captured")
    matcher = make_matcher(
        "{time}{actor}{s}was{s}captured{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class AIAircraftCrewMemberHasBailedOut(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) bailed out at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI aircraft crew member has bailed out")
    matcher = make_matcher(
        "{time}{actor}{s}bailed{s}out{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )


class AIAircraftCrewMemberHasLanded(ParsableEvent):
    """
    Example:

        "[8:33:05 PM] r01000(0) successfully bailed out at 100.0 200.99"

    """
    __slots__ = ['time', 'actor', 'pos', ]

    verbose_name = _("AI aircraft crew member has landed")
    matcher = make_matcher(
        "{time}{actor}{s}successfully{s}bailed{s}out{pos}"
        .format(
            time=TIME_GROUP_PREFIX,
            actor=AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP,
            pos=POS_GROUP_SUFFIX,
            s=WHITESPACE,
        )
    )
    transformers = (
        transform_time,
        transform_ai_aircraft_crew_member_as_actor,
        transform_2d_pos,
    )
