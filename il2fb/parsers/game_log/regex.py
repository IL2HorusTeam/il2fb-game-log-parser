# coding: utf-8

from il2fb.commons.regex import (
    ANYTHING, WHITESPACE, WHITESPACES, NON_WHITESPACES, NUMBER, FLOAT,
    START_OF_STRING, END_OF_STRING,
    group, named_group, choices,
)

from .constants import TOGGLE_VALUES, TARGET_STATES


#: Example: "[8:33:05 PM]"
TIME = "\d{1,2}:\d{2}:\d{2}\s[AP]M"
TIME_GROUP = named_group('time', TIME)
TIME_GROUP_PREFIX = "{start}\[{time_group}\]{ss}".format(
    start=START_OF_STRING,
    time_group=TIME_GROUP,
    ss=WHITESPACES,
)

#: Example: "Sep 15, 2013"
DATE = "\D{3}\s\d{1,2},\s\d{4}"
DATE_GROUP = named_group('date', DATE)
DATE_TIME_GROUP_PREFIX = "{start}\[{date_group}{s}{time_group}\]{ss}".format(
    date_group=DATE_GROUP,
    time_group=TIME_GROUP,
    start=START_OF_STRING,
    s=WHITESPACE,
    ss=WHITESPACES,
)

#: Example: " at 100.99 200.99"
POS_GROUP_SUFFIX = "{s}at{s}{pos_x}{s}{pos_y}{end}".format(
    pos_x=named_group('pos_x', FLOAT),
    pos_y=named_group('pos_y', FLOAT),
    s=WHITESPACE,
    end=END_OF_STRING,
)

TARGET_STATE_GROUP = named_group('state', choices(TARGET_STATES))
TOGGLE_VALUE_GROUP = named_group('value', choices(TOGGLE_VALUES))

BELLIGERENT_GROUP = named_group('belligerent', NON_WHITESPACES)

INDEX = NUMBER
INDEX_ACTOR_GROUP = named_group('actor_index', INDEX)
INDEX_ATTACKER_GROUP = named_group('attacker_index', INDEX)

CALLSIGN = NON_WHITESPACES
HIMSELF = group(choices(['landscape', 'NONAME']))

HUMAN_ACTOR_GROUP = named_group('actor_callsign', CALLSIGN)

AIRCRAFT = NON_WHITESPACES
AIRCRAFT_ACTOR_GROUP = named_group('actor_aircraft', AIRCRAFT)

HUMAN_AIRCRAFT_GROUP_TEMPLATE = "{callsign}:{aircraft}"
HUMAN_AIRCRAFT_ACTOR_GROUP = HUMAN_AIRCRAFT_GROUP_TEMPLATE.format(
    callsign=HUMAN_ACTOR_GROUP,
    aircraft=AIRCRAFT_ACTOR_GROUP,
)
HUMAN_AIRCRAFT_ATTACKER_GROUP = HUMAN_AIRCRAFT_GROUP_TEMPLATE.format(
    callsign=named_group('attacker_callsign', CALLSIGN),
    aircraft=named_group('attacker_aircraft', AIRCRAFT),
)
HUMAN_AIRCRAFT_ASSISTANT_GROUP = HUMAN_AIRCRAFT_GROUP_TEMPLATE.format(
    callsign=named_group('assistant_callsign', CALLSIGN),
    aircraft=named_group('assistant_aircraft', AIRCRAFT),
)

HUMAN_AIRCRAFT_CREW_MEMBER_GROUP_TEMPlATE = "{callsign}:{aircraft}\({index}\)"
HUMAN_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP = HUMAN_AIRCRAFT_CREW_MEMBER_GROUP_TEMPlATE.format(
    callsign=HUMAN_ACTOR_GROUP,
    aircraft=AIRCRAFT_ACTOR_GROUP,
    index=INDEX_ACTOR_GROUP,
)

AI_FLIGHT = NON_WHITESPACES
AI_FLIGHT_ACTOR_GROUP = named_group('actor_flight', AI_FLIGHT)

AI_AIRCRAFT_INDEX = NUMBER
AI_AIRCRAFT_INDEX_ACTOR_GROUP = named_group('actor_aircraft', AI_AIRCRAFT_INDEX)

AI_AIRCRAFT_GROUP_TEMPLATE = "{flight}{aircraft}"
AI_AIRCRAFT_ACTOR_GROUP = AI_AIRCRAFT_GROUP_TEMPLATE.format(
    flight=AI_FLIGHT_ACTOR_GROUP,
    aircraft=AI_AIRCRAFT_INDEX_ACTOR_GROUP,
)
AI_AIRCRAFT_ATTACKER_GROUP = AI_AIRCRAFT_GROUP_TEMPLATE.format(
    flight=named_group('attacker_flight', AI_FLIGHT),
    aircraft=named_group('attacker_aircraft', AI_AIRCRAFT_INDEX),
)
AI_AIRCRAFT_ASSISTANT_GROUP = AI_AIRCRAFT_GROUP_TEMPLATE.format(
    flight=named_group('assistant_flight', AI_FLIGHT),
    aircraft=named_group('assistant_aircraft', AI_AIRCRAFT_INDEX),
)

AI_AIRCRAFT_CREW_MEMBER_GROUP_TEMPlATE = "{flight}{aircraft}\({index}\)"
AI_AIRCRAFT_CREW_MEMBER_ACTOR_GROUP = AI_AIRCRAFT_CREW_MEMBER_GROUP_TEMPlATE.format(
    flight=AI_FLIGHT_ACTOR_GROUP,
    aircraft=AI_AIRCRAFT_INDEX_ACTOR_GROUP,
    index=INDEX_ACTOR_GROUP,
)

STATIONARY_UNIT = "{0}_Static".format(NUMBER)
STATIONARY_UNIT_ACTOR_GROUP = named_group(
    'actor_stationary_unit',
    STATIONARY_UNIT,
)
STATIONARY_UNIT_ATTACKER_GROUP = named_group(
    'attacker_stationary_unit',
    STATIONARY_UNIT,
)

MOVING_UNIT = "{0}_Chief".format(NUMBER)
MOVING_UNIT_ACTOR_GROUP = named_group('actor_moving_unit', MOVING_UNIT)
MOVING_UNIT_ATTACKER_GROUP = named_group('attacker_moving_unit', MOVING_UNIT)

MOVING_UNIT_MEMBER_GROUP_TEMPLATE = "{moving_unit}{index}"
MOVING_UNIT_MEMBER_ACTOR_GROUP = MOVING_UNIT_MEMBER_GROUP_TEMPLATE.format(
    moving_unit=MOVING_UNIT_ACTOR_GROUP,
    index=INDEX_ACTOR_GROUP,
)
MOVING_UNIT_MEMBER_ATTACKER_GROUP = MOVING_UNIT_MEMBER_GROUP_TEMPLATE.format(
    moving_unit=MOVING_UNIT_ATTACKER_GROUP,
    index=INDEX_ATTACKER_GROUP,
)

BRIDGE = "Bridge{0}".format(NUMBER)
BRIDGE_ACTOR_GROUP = named_group('actor_bridge', BRIDGE)

OBJECT_NAMES = group(choices(['live', 'mono']))

BUILDING = ANYTHING
BUILDING_GROUP_TEMPLATE = (
    "3do/Buildings/{{building}}/{object_names}.sim"
    .format(object_names=OBJECT_NAMES)
)
BUILDING_ACTOR_GROUP = BUILDING_GROUP_TEMPLATE.format(
    building=named_group('actor_building', BUILDING),
)

TREE = (
    "3do/Tree/{any}/{object_names}.sim"
    .format(any=ANYTHING, object_names=OBJECT_NAMES)
)
