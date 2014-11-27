# -*- coding: utf-8 -*-

import datetime

from .constants import (
    LOG_TIME_FORMAT, LOG_DATE_FORMAT, ToggleValues, TargetEndStates,
)


__all__ = (
    'process_time', 'process_date', 'process_number', 'process_target_result',
    'process_fuel', 'process_position', 'process_toggle_value', 'process_seat',
    'process_attacking_user', 'process_army',
)


def process_time(data):
    data['time'] = datetime.datetime.strptime(
        data['time'], LOG_TIME_FORMAT).time()


def process_date(data):
    data['date'] = datetime.datetime.strptime(
        data['date'], LOG_DATE_FORMAT).date()


def process_number(data):
    data['number'] = int(data['number'])


def process_target_result(data):
    r = data.get('result')
    if r in TargetEndStates.values():
        data['result'] = (r == TargetEndStates.COMPLETE.value)
    else:
        raise ValueError(
            "Target result value '{value}' is invalid. "
            "Valid values: {valid}."
            .format(value=r, valid=TargetEndStates.list_choices()))


def process_fuel(data):
    data['fuel'] = int(data['fuel'])


def process_position(data):
    x = data.pop('pos_x')
    y = data.pop('pos_y')
    data['pos'] = {
        'x': float(x),
        'y': float(y),
    }


def process_toggle_value(data):
    v = data.get('value')
    if v in ToggleValues.values():
        data['value'] = (v == ToggleValues.ON.value)
    else:
        raise ValueError(
            "Toggle value '{value}' is invalid. Valid values: {valid}."
            .format(value=v, valid=ToggleValues.list_choices()))


def process_seat(data):
    data['seat'] = int(data['seat'])


def process_attacking_user(data):
    callsign = data.pop('e_callsign')
    aircraft = data.pop('e_aircraft')
    data['attacker'] = {
        'callsign': callsign,
        'aircraft': aircraft,
    }


def process_army(data):
    data['army'] = data['army'].capitalize()
