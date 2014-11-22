# -*- coding: utf-8 -*-

from pyparsing import (
    Combine, White, Word, oneOf, nums,
)

from .actions import (
    convert_time,
)


single_space = White(exact=1)

#: ``AM`` or ``PM``
day_period = Combine(
    oneOf("A P") + 'M'
).setResultsName('day_period')


#: Example: ``8:33:05 PM``
time = Combine(
    Word(nums, min=1, max=2)            # hours
    + (':' + Word(nums, exact=2)) * 2   # minutes and seconds
    + single_space
    + day_period
).setResultsName('time').setParseAction(convert_time)
