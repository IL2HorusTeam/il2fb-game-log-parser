# coding: utf-8
"""
Regex primitives.

"""

from .constants import TOGGLE_VALUES, TARGET_END_STATES


TIME_GROUP = """
# Capture raw time stamp. E.g.:
#
# "foo 8:33:05 PM bar"
#
# "8:33:05 PM" will be captured into 'time' group.
                # any beginning of a string
(?P<time>       # 'time' group start
    \d{1,2}     # 1 or 2 digits for hours (e.g. 8, 08 or 18)
    :           # hours-minutes separator
    \d{2}       # 2 digits for minutes
    :           # minutes-seconds separator
    \d{2}       # 2 digits for seconds
    \s          # single whitespace
    [AP]M       # day period (e.g. AM or PM)
)               # 'time' group end
                # any ending of a string
"""

TIME_PREFIX = """
# Capture event's time stamp prefix. E.g.:
#
# "[8:33:05 PM] foo"
#
# "8:33:05 PM" will be captured into 'time' group.
^               # beginning of a string
\[              # left time wrapper
{time_group}    # 'time_group' regex placeholder
\]              # right time wrapper
\s+             # one or more whitespaces
                # any ending of a string
""".format(
    time_group=TIME_GROUP,
)

DATE_TIME_PREFIX = """
# Capture event's datetime stamp prefix. E.g.:
#
# "[Sep 15, 2013 8:33:05 PM] foo"
#
# "Sep 15, 2013" will be captured into 'date' group,
# "8:33:05 PM" will be captured into 'time' group.
^               # beginning of a string
\[              # opening brackets
(?P<date>       # 'date' group start
    \D{{3}}     # 3 non-digits for month abbreviation (e.g. Jan, Feb, Sep, etc)
    \s          # single whitespace
    \d{{1,2}}   # 1 or 2 digits for day number (e.g. 8, 08 or 18)
    ,           # single comma
    \s          # single whitespace
    \d{{4}}     # 4 digits for year (e.g. 2013)
)               # 'date' group end
\s              # single whitespace
{time_group}    # 'time_group' regex placeholder
\]              # closing brackets
\s+             # one or more whitespaces
                # any ending of a string
""".format(
    time_group=TIME_GROUP,
)

BELLIGERENT_GROUP = """
# Capture belligerent's name. E.g.:
#
# "  Red  "
#
# "Red" will be captured into 'belligerent' group.
                 # any beginning of a string
(?P<belligerent> # 'belligerent' group start
    \S+          # one or more non-whitespaces for belligerent's name
)                # 'belligerent' group end
                 # any ending of a string
"""

HUMAN_CALLSIGN = """
# Detect pilot's callsign. E.g.:
#
# "    User   "
#
\S+              # one or more non-whitespaces for belligerent's name
"""

HUMAN_CALLSIGN_GROUP = """
# Capture pilot's callsign. E.g.:
#
# "    User   "
#
# "User" will be captured into 'callsign' group.
                # any beginning of a string
(?P<callsign>   # 'callsign' group start
    {callsign}  # one or more non-whitespace characters
)               # 'callsign' group end
                # any ending of a string
""".format(
    callsign=HUMAN_CALLSIGN,
)

HUMAN_AIRCRAFT_GROUP = """
# Capture pilot's callsign and aircraft. E.g.:
#
# "  User:Pe-8   "
#
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group.
                  # any beginning of a string
{callsign_group}  # 'callsign_group' regex placeholder
:                 # a colon
(?P<aircraft>     # 'aircraft' group start
    \S+           # one or more non-whitespace characters
)                 # 'aircraft' group end
                  # any ending of a string
""".format(
    callsign_group=HUMAN_CALLSIGN_GROUP,
)

SEAT_GROUP = """
# Capture seat number. E.g.:
#
# "Pe-8(0) seat occupied"
#
# "0" will be captured into 'seat_number' group.
                 # any beginning of a string
\(               # opening parenthesis
(?P<seat_number> # 'seat_number' group start
    \d+          # one or more digits for seat number
)                # 'seat_number' group end
\)               # closing parenthesis
                 # any ending of a string
"""

HUMAN_AIRCRAFT_CREW_MEMBER_GROUP = """
# Capture pilot's callsign, aircraft and seat number. E.g.:
#
# " User:Pe-8(0) "
#
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "0" will be captured into 'seat_number' group.
                  # any beginning of a string
{aircraft_group}  # 'aircraft_group' regex placeholder
{seat_group}      # 'seat_group' regex placeholder
                  # any ending of a string
""".format(
    aircraft_group=HUMAN_AIRCRAFT_GROUP,
    seat_group=SEAT_GROUP,
)

POS_SUFFIX = """
# Capture map position of an event. E.g.:
#
# "Something has happened at 100.0 200.99"
#
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
                # any beginning of a string
\s              # single whitespace
at              #
\s              # single whitespace
(?P<pos_x>      # 'pos_x' group start
    \d+         # 1 or more digits for integer part
    .           # decimal separator
    \d+         # 1 or more digits for real part
)               # 'pos_x' group end
\s              # single whitespace
(?P<pos_y>      # 'pos_y' group start
    \d+         # 1 or more digits for integer part
    .           # decimal separator
    \d+         # 1 or more digits for real part
)               # 'pos_y' group end
$               # end of a string
"""

TARGET_END_STATE_GROUP = """
# Capture end state of target. E.g.:
#
# "something is Complete"
#
# "Complete" will be captured into 'state' group.
                # any beginning of a string
(?P<state>      # 'state' group start
    {states}    # state choices
)               # 'state' group end
                # end of a string
""".format(
    states="|".join(TARGET_END_STATES)
)

TOGGLE_VALUE_GROUP = """
# Capture toggle value. E.g.:
#
# "something is on"
#
# "on" will be captured into 'value' group.
                # any beginning of a string
(?P<value>      # 'value' group start
    {values}    # switch value (e.g. 'on' or 'off')
)               # 'value' group end
                # any ending of a string
""".format(
    values="|".join(TOGGLE_VALUES)
)

HIMSELF = """
# Detect that actor has done something destructive to own aircraft.
                    # any beginning of a string
(landscape|NONAME)  # self-flag
                    # any ending of a string
"""
