# -*- coding: utf-8 -*-

from pyparsing import (
    Combine, oneOf, Literal,
)


day_period = Combine(oneOf("A P") + 'M').setResultsName('day_period')
