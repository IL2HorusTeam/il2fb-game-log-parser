# -*- coding: utf-8 -*-

import datetime

from .constants import LOG_TIME_FORMAT, LOG_DATE_FORMAT, TOGGLE_VALUES
from .structures import Point2D


def convert_time(tokens):
    value = tokens.time.asList()[0]
    return datetime.datetime.strptime(value, LOG_TIME_FORMAT).time()


def convert_date(tokens):
    value = tokens.date
    return datetime.datetime.strptime(value, LOG_DATE_FORMAT).date()


def convert_int(tokens):
    return int(tokens.asList()[0])


def convert_float(tokens):
    return float(tokens.asList()[0])


def convert_pos(tokens):
    return Point2D(tokens.pos.x, tokens.pos.y)


def convert_toggle_value(tokens):
    return TOGGLE_VALUES.get_by_value(tokens.toggle_value)
