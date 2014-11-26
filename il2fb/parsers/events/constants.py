# -*- coding: utf-8 -*-

from candv import Values, ValueConstant


LOG_TIME_FORMAT = "%I:%M:%S %p"
LOG_DATE_FORMAT = "%b %d, %Y"


class RegexChoices(Values):

    @classmethod
    def regex_choices(cls):
        return '|'.join(cls.values())

    @classmethod
    def list_choices(cls):
        return ', '.join(cls.values())


class TOGGLE_VALUES(RegexChoices):
    ON = ValueConstant('on')
    OFF = ValueConstant('off')


class TARGET_END_STATES(RegexChoices):
    COMPLETE = ValueConstant('Complete')
    FAILED = ValueConstant('Failed')
