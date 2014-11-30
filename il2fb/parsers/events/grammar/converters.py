# -*- coding: utf-8 -*-

import datetime

from il2fb.commons.organization import Belligerents

from ..constants import (
    LOG_TIME_FORMAT, LOG_DATE_FORMAT, ToggleValues, TargetEndStates,
)
from ..structures import Point2D, HumanActor, HumanCrewMember


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
    return ToggleValues[tokens.toggle_value]


def to_belligerent(tokens):
    return Belligerents[tokens.belligerent.lower()]


def to_building(tokens):
    """
    For example, from
    ["3do", "Buildings", "Finland", "CenterHouse1_w", "live.sim"]
    we will take "CenterHouse1_w" as result
    """
    return tokens.asList()[3]


def to_target_end_state(tokens):
    return TargetEndStates.get_by_value(tokens.target_end_state)


def to_human_actor(tokens):
    return HumanActor(tokens.callsign, tokens.aircraft)


def to_human_crew_member(tokens):
    return HumanCrewMember(tokens.callsign,
                           tokens.aircraft,
                           tokens.seat_number)
