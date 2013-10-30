# -*- coding: utf-8 -*-

import datetime

from il2ds_log_parser.constants import (LOG_TIME_FORMAT, LOG_DATE_FORMAT,
    TARGET_RESULT_COMPLETE, TARGET_RESULTS, TOGGLE_VALUE_ON, TOGGLE_VALUES, )


__all__ = [
    'process_time', 'process_date', 'process_number', 'process_target_result',
    'process_fuel', 'process_position', 'process_toggle_value', 'process_seat',
    'process_attacking_user', 'process_army',
]


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
    if r in TARGET_RESULTS:
        data['result'] = (r == TARGET_RESULT_COMPLETE)
    else:
        raise ValueError(
            "Target result value '{value}' is invalid. "
            "Valid values: {valid}.".format(
                value=r,
                valid=', '.join(TARGET_RESULTS)))


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
    if v in TOGGLE_VALUES:
        data['value'] = (v == TOGGLE_VALUE_ON)
    else:
        raise ValueError(
            "Toggle value '{value}' is invalid. Valid values: {valid}.".format(
                value=v,
                valid=', '.join(TOGGLE_VALUES)))


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
    army = data['army']
    data['army'] = army[0].upper() + army[1:].lower()
