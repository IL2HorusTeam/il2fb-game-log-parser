# -*- coding: utf-8 -*-

from pyparsing import (
    Combine, LineStart, Regex, White, Word, alphas, nums, oneOf,
)

from .actions import (
    convert_time, convert_date, convert_float,
)


single_space = White(ws=' ', exact=1)
float_number = Regex(r"\d+.\d+").setParseAction(convert_float)

# Example: "AM" or "PM"
day_period = Combine(
    oneOf("A P") + 'M'
).setResultsName('day_period')

# Example: "8:33:05 PM" or "08:33:05 PM"
time = Combine(
    Word(nums, min=1, max=2)            # Hours (e.g. 8, 08 or 18)
    + (':' + Word(nums, exact=2)) * 2   # Minutes and seconds
    + single_space                      #
    + day_period                        #
).setResultsName('time').setParseAction(convert_time)

# Example: "[8:33:05 PM] "
event_time = Combine(LineStart() + '[' + time + ']' + single_space)

# Example: "Sep 15, 2013"
date = Combine(
    Word(alphas, exact=3)       # Month abbreviation (e.g. Jan, Feb, Sep, etc.)
    + single_space              #
    + Word(nums, min=1, max=2)  # Day number (e.g. 8, 08 or 18)
    + ','                       #
    + single_space              #
    + Word(nums, exact=4)       # Year
).setResultsName('date').setParseAction(convert_date)

# Example: "Sep 15, 2013 8:33:05 PM"
date_time = Combine(date + single_space + time)

# Example: "[Sep 15, 2013 8:33:05 PM] "
event_date_time = Combine(LineStart() + '[' + date_time + ']' + single_space)
