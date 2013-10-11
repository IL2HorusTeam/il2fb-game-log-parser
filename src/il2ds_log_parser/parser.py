# -*- coding: utf-8 -*-

import datetime

from il2ds_log_parser.constants import LOG_TIME_FORMAT, LOG_DATE_FORMAT
from il2ds_log_parser.regex import *


def parse_time(value):
    """Take time in format of 'H:MM:SS AM/PM' and convert it to ISO format"""
    dt = datetime.datetime.strptime(value, LOG_TIME_FORMAT)
    return dt.time().isoformat()

def parse_date(value):
    """Take date in format of 'Mon DD, YYYY' and convert it to ISO format"""
    dt = datetime.datetime.strptime(value, LOG_DATE_FORMAT)
    return dt.date().isoformat()
