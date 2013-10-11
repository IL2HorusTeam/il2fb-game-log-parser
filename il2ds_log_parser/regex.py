# -*- coding: utf-8 -*-

#------------------------------------------------------------------------------
# Commons
#------------------------------------------------------------------------------

"""
Capturing base event time stamp. Example:

    "foo 8:33:05 PM bar"

Output group:

    time - event's time.

"""
RX_TIME_BASE = r"(?P<time>\d{1,2}:\d{2}:\d{2} [AP]M)"
"""
Capturing regular event time stamp. Example:

    "[8:33:05 PM] foo"

Output group:

    time - event's time.

"""
RX_TIME = r"^\[" + RX_TIME_BASE + r"\]"
"""
Capturing regular event datetime stamp. Example:

    "[Sep 15, 2013 8:33:05 PM] foo"

Output group:

    date - event's date;
    time - event's time.

"""
RX_DATE_TIME = r"^\[(?P<date>\D{3} \d{1,2}, \d{4}) " + RX_TIME_BASE + r"\]"

#------------------------------------------------------------------------------
# Mission flow
#------------------------------------------------------------------------------

"""
Capture mission playing event. Example:

    "[Sep 15, 2013 8:33:05 PM] Mission: PH.mis is Playing"

Output group:

    date - event's date;
    time - event's time;
    mission - mission's file name.

"""
RX_MISSION_PLAYING = RX_DATE_TIME + r" Mission: (?P<mission>.+\.mis) is Playing$"
"""
Capture mission beginning event. Example:

    "[8:33:05 PM] Mission BEGIN"

Output group:

    time - event's time;

"""
RX_MISSION_BEGIN = RX_TIME + r" Mission BEGIN$"
"""
Capture mission end event. Example:

    "[8:33:05 PM] Mission END"

Output group:

    time - event's time;

"""
RX_MISSION_END = RX_TIME + r" Mission END$"

#------------------------------------------------------------------------------
# User state events
#------------------------------------------------------------------------------



#------------------------------------------------------------------------------
# Action events
#------------------------------------------------------------------------------
