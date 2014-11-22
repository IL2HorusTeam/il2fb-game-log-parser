# -*- coding: utf-8 -*-

import datetime

from .constants import LOG_TIME_FORMAT


def convert_time(tokens):
    value = tokens.time.asList()[0]
    return datetime.datetime.strptime(value, LOG_TIME_FORMAT).time()
