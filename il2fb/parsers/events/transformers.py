# coding: utf-8
"""
Data transformers.

"""

import datetime

from il2fb.commons import actors

from .constants import LOG_TIME_FORMAT, LOG_DATE_FORMAT


def transform_time(data):
    value = data['time']
    data['time'] = datetime.datetime.strptime(value, LOG_TIME_FORMAT).time()


def transform_date(data):
    value = data['date']
    data['date'] = datetime.datetime.strptime(value, LOG_DATE_FORMAT).date()


def get_human_transformer(dst_field_name, src_field_prefix=None):
    if not src_field_prefix:
        src_field_prefix = dst_field_name

    callsign_field_name = '{0}_callsign'.format(src_field_prefix)

    def transformer(data):
        data[dst_field_name] = actors.Human(
            data.pop(callsign_field_name),
        )

    return transformer


transform_human_as_actor = get_human_transformer('actor')


def get_human_aircraft_transformer(dst_field_name, src_field_prefix=None):
    if not src_field_prefix:
        src_field_prefix = dst_field_name

    callsign_field_name = '{0}_callsign'.format(src_field_prefix)
    aircraft_field_name = '{0}_aircraft'.format(src_field_prefix)

    def transformer(data):
        data[dst_field_name] = actors.HumanAircraft(
            data.pop(callsign_field_name),
            data.pop(aircraft_field_name),
        )

    return transformer


transform_human_aircraft_as_actor = get_human_aircraft_transformer('actor')
transform_human_aircraft_as_attacker = get_human_aircraft_transformer('attacker')
transform_human_aircraft_as_assistant = get_human_aircraft_transformer('assistant')


def get_human_aircraft_crew_member_transformer(dst_field_name, src_field_prefix=None):
    if not src_field_prefix:
        src_field_prefix = dst_field_name

    callsign_field_name = '{0}_callsign'.format(src_field_prefix)
    aircraft_field_name = '{0}_aircraft'.format(src_field_prefix)
    index_field_name = '{0}_index'.format(src_field_prefix)

    def transformer(data):
        data[dst_field_name] = actors.HumanAircraftCrewMember(
            data.pop(callsign_field_name),
            data.pop(aircraft_field_name),
            int(data.pop(index_field_name)),
        )

    return transformer


transform_human_aircraft_crew_member_as_actor = get_human_aircraft_crew_member_transformer('actor')


def get_ai_aircraft_transformer(dst_field_name, src_field_prefix=None):
    if not src_field_prefix:
        src_field_prefix = dst_field_name

    flight_field_name = '{0}_flight'.format(src_field_prefix)
    aircraft_field_name = '{0}_aircraft'.format(src_field_prefix)

    def transformer(data):
        data[dst_field_name] = actors.AIAircraft(
            data.pop(flight_field_name),
            int(data.pop(aircraft_field_name)),
        )

    return transformer


transform_ai_aircraft_as_actor = get_ai_aircraft_transformer('actor')
transform_ai_aircraft_as_attacker = get_ai_aircraft_transformer('attacker')
transform_ai_aircraft_as_assistant = get_ai_aircraft_transformer('assistant')


def get_ai_aircraft_crew_member_transformer(dst_field_name, src_field_prefix=None):
    if not src_field_prefix:
        src_field_prefix = dst_field_name

    flight_field_name = '{0}_flight'.format(src_field_prefix)
    aircraft_field_name = '{0}_aircraft'.format(src_field_prefix)
    index_field_name = '{0}_index'.format(src_field_prefix)

    def transformer(data):
        data[dst_field_name] = actors.AIAircraftCrewMember(
            data.pop(flight_field_name),
            int(data.pop(aircraft_field_name)),
            int(data.pop(index_field_name)),
        )

    return transformer


transform_ai_aircraft_crew_member_as_actor = get_ai_aircraft_crew_member_transformer('actor')
transform_ai_aircraft_crew_member_as_seat = get_ai_aircraft_crew_member_transformer('seat', 'actor')


def get_stationary_unit_transformer(dst_field_name, src_field_prefix=None):
    if not src_field_prefix:
        src_field_prefix = dst_field_name

    stationary_unit_field_name = '{0}_stationary_unit'.format(src_field_prefix)

    def transformer(data):
        data[dst_field_name] = actors.StationaryUnit(
            data.pop(stationary_unit_field_name),
        )

    return transformer


transform_stationary_unit_as_actor = get_stationary_unit_transformer('actor')
transform_stationary_unit_as_attacker = get_stationary_unit_transformer('attacker')


def get_moving_unit_transformer(dst_field_name, src_field_prefix=None):
    if not src_field_prefix:
        src_field_prefix = dst_field_name

    moving_unit_field_name = '{0}_moving_unit'.format(src_field_prefix)

    def transformer(data):
        data[dst_field_name] = actors.MovingUnit(
            data.pop(moving_unit_field_name),
        )

    return transformer


transform_moving_unit_as_actor = get_moving_unit_transformer('actor')
transform_moving_unit_as_attacker = get_moving_unit_transformer('attacker')


def get_moving_unit_member_transformer(dst_field_name, src_field_prefix=None):
    if not src_field_prefix:
        src_field_prefix = dst_field_name

    moving_unit_field_name = '{0}_moving_unit'.format(src_field_prefix)
    index_field_name = '{0}_index'.format(src_field_prefix)

    def transformer(data):
        data[dst_field_name] = actors.MovingUnitMember(
            data.pop(moving_unit_field_name),
            int(data.pop(index_field_name)),
        )

    return transformer


transform_moving_unit_member_as_actor = get_moving_unit_member_transformer('actor')
transform_moving_unit_member_as_attacker = get_moving_unit_member_transformer('attacker')


def get_building_transformer(dst_field_name, src_field_prefix=None):
    if not src_field_prefix:
        src_field_prefix = dst_field_name

    building_field_name = '{0}_building'.format(src_field_prefix)

    def transformer(data):
        data[dst_field_name] = actors.Building(
            data.pop(building_field_name),
        )

    return transformer


transform_building_as_actor = get_building_transformer('actor')


def get_bridge_transformer(dst_field_name, src_field_prefix=None):
    if not src_field_prefix:
        src_field_prefix = dst_field_name

    bridge_field_name = '{0}_bridge'.format(src_field_prefix)

    def transformer(data):
        data[dst_field_name] = actors.Bridge(
            data.pop(bridge_field_name),
        )

    return transformer


transform_bridge_as_actor = get_bridge_transformer('actor')
