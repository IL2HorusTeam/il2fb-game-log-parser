# -*- coding: utf-8 -*-

from collections import namedtuple


LOG_TIME_FORMAT = "%I:%M:%S %p"
LOG_DATE_FORMAT = "%b %d, %Y"

TOGGLE_VALUES = namedtuple(
    'TOGGLE_VALUES',
    ['on', 'off']
)._make(
    [True, False]
)

TARGET_END_STATES = namedtuple(
    'TARGET_END_STATES',
    ['COMPLETE', 'FAILED']
)._make(
    ['Complete', 'Failed']
)
