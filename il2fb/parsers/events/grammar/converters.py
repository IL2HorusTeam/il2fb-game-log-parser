# -*- coding: utf-8 -*-

import datetime

from il2fb.commons.organization import Belligerents

from ..constants import LOG_TIME_FORMAT, LOG_DATE_FORMAT, TOGGLE_VALUES
from ..structures import (
    Point2D, HumanAircraft, HumanAircraftCrewMember, AIAircraftCrewMember,
)


def to_time(tokens):
    value = tokens.time.asList()[0]
    return datetime.datetime.strptime(value, LOG_TIME_FORMAT).time()


def to_date(tokens):
    value = tokens.date
    return datetime.datetime.strptime(value, LOG_DATE_FORMAT).date()


def to_int(tokens):
    return int(tokens.asList()[0])


def to_float(tokens):
    return float(tokens.asList()[0])


def to_pos(tokens):
    return Point2D(tokens.pos.x, tokens.pos.y)


def to_toggle_value(tokens):
    return getattr(TOGGLE_VALUES, tokens.value)


def to_belligerent(tokens):
    return Belligerents[tokens.belligerent.lower()]


def to_human_aircraft(tokens):
    return HumanAircraft(tokens.callsign, tokens.aircraft)


def to_human_aircraft_crew_member(tokens):
    return HumanAircraftCrewMember(tokens.callsign,
                                   tokens.aircraft,
                                   tokens.seat_number)


def to_ai_aircraft_crew_member(tokens):
    return AIAircraftCrewMember(tokens.aircraft, tokens.seat_number)
