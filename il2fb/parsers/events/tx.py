# coding: utf-8
"""
Data transformers.

"""

import datetime

from il2fb.commons.organization import Belligerents
from il2fb.commons.spatial import Point2D

from .actors import HumanAircraft, HumanAircraftCrewMember
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


def human_aircraft_as_actor(data):
    data['actor'] = HumanAircraft(
        data.pop('callsign'),
        data.pop('aircraft'),
    )


def human_aircraft_crew_member_as_actor(data):
    data['actor'] = HumanAircraftCrewMember(
        data.pop('callsign'),
        data.pop('aircraft'),
        int(data.pop('seat_number')),
    )
