# coding: utf-8

from collections import namedtuple


LOG_TIME_FORMAT = "%I:%M:%S %p"
LOG_DATE_FORMAT = "%b %d, %Y"


TARGET_END_STATES = namedtuple(
    'TARGET_END_STATES',
    ['COMPLETE', 'FAILED']
)._make(
    ['Complete', 'Failed']
)

TOGGLE_VALUES = namedtuple(
    'TOGGLE_VALUES',
    ['ON', 'OFF']
)._make(
    ['on', 'off']
)
