# -*- coding: utf-8 -*-

import datetime

from .constants import LOG_TIME_FORMAT


def convert_time(string, location, tokens):
    return datetime.datetime.strptime(string, LOG_TIME_FORMAT).time()
