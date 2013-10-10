# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# Commons
#------------------------------------------------------------------------------

"""
Regex for capturing base event timestamp. Example:

    "foo 8:33:05 PM bar"

"""
RX_TIME_BASE = r"(?P<time>\d{1,2}:\d{2}:\d{2} [AP]M)"
"""
Regex for capturing regular event timestamp. Example:

    "[8:33:05 PM] foo"

"""
RX_TIME = r"^\[" + RX_TIME_BASE + r"\]"
"""
Regex for capturing regular event timestamp. Example:

    "[Sep 15, 2013 8:33:05 PM] foo"

"""
RX_DATE_TIME = r"^\[(?P<date>\D{3} \d{1,2}, \d{4}) " + RX_TIME_BASE + r"\]"
