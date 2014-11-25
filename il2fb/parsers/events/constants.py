# -*- coding: utf-8 -*-

from candv import Values, ValueConstant, Constants, SimpleConstant


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


class TARGET_RESULT_TYPES(RegexChoices):
    COMPLETE = ValueConstant('Complete')
    FAILED = ValueConstant('Failed')


class EVENT_TYPES(Constants):
    MISSION_IS_PLAYING = SimpleConstant()
    MISSION_BEGAN = SimpleConstant()
    MISSION_ENDED = SimpleConstant()
