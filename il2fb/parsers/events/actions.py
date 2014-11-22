# -*- coding: utf-8 -*-

import datetime

from .constants import LOG_TIME_FORMAT, LOG_DATE_FORMAT


def convert_time(tokens):
    value = tokens.time.asList()[0]
    return datetime.datetime.strptime(value, LOG_TIME_FORMAT).time()


def convert_date(tokens):
    value = tokens.date
    return datetime.datetime.strptime(value, LOG_DATE_FORMAT).date()


def convert_float(tockens):
    return float(tockens.asList()[0])
