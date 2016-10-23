# coding: utf-8
"""
Data transformers.

"""

import datetime

from il2fb.commons.organization import Belligerents
from il2fb.commons.spatial import Point2D

from . import actors
from .constants import LOG_TIME_FORMAT, LOG_DATE_FORMAT


def transform_time(data, field_name='time'):
    value = data[field_name]
    data[field_name] = datetime.datetime.strptime(value, LOG_TIME_FORMAT).time()


def transform_date(data, field_name='date'):
    value = data[field_name]
    data[field_name] = datetime.datetime.strptime(value, LOG_DATE_FORMAT).date()


def transform_pos(data):
    data['pos'] = Point2D(
        float(data.pop('pos_x')),
        float(data.pop('pos_y')),
    )


def transform_belligerent(data, field_name='belligerent'):
    value = data[field_name]
    data[field_name] = Belligerents[value.lower()]


def transform_int(data, field_name):
    data[field_name] = int(data[field_name])


def transform_float(data, field_name):
    data[field_name] = float(data[field_name])


def human_as_actor(data):
    data['actor'] = actors.Human(
        data.pop('actor_callsign'),
    )


def human_aircraft_as_actor(data):
    data['actor'] = actors.HumanAircraft(
        data.pop('actor_callsign'),
        data.pop('actor_aircraft'),
    )


def human_aircraft_as_attacker(data):
    data['attacker'] = actors.HumanAircraft(
        data.pop('attacker_callsign'),
        data.pop('attacker_aircraft'),
    )


def human_aircraft_crew_member_as_actor(data):
    data['actor'] = actors.HumanAircraftCrewMember(
        data.pop('actor_callsign'),
        data.pop('actor_aircraft'),
        int(data.pop('actor_index')),
    )


def ai_aircraft_as_attacker(data):
    data['attacker'] = actors.AIAircraft(
        data.pop('attacker_flight'),
        int(data.pop('attacker_index')),
    )


def stationary_unit_as_attacker(data):
    data['attacker'] = actors.StationaryUnit(
        data.pop('attacker_stationary_unit'),
    )
