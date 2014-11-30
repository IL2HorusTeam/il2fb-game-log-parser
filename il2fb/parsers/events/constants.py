# -*- coding: utf-8 -*-

from candv import Values, ValueConstant


LOG_TIME_FORMAT = "%I:%M:%S %p"
LOG_DATE_FORMAT = "%b %d, %Y"


class ToggleValues(Values):
    on = ValueConstant(True)
    off = ValueConstant(False)


class TargetEndStates(Values):
    COMPLETE = ValueConstant('Complete')
    FAILED = ValueConstant('Failed')
