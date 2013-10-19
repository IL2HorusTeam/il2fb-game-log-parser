# -*- coding: utf-8 -*-

import re

#------------------------------------------------------------------------------
# Commons
#------------------------------------------------------------------------------

"""Flags to be used for matching strings."""
RX_FLAGS = re.VERBOSE

RX_TIME_BASE = """
# Capturing base event time stamp. E.g.:
#
# "foo 8:33:05 PM bar"
#
# "8:33:05 PM" will be captured into 'time' group.
                # any beginning of the string
(?P<time>       # 'time' group start
    \d{1,2}     # 1 or 2 digits for hours (e.g. 8, 08 or 18)
    :           # hours-minutes separator
    \d{2}       # 2 digits for minutes
    :           # minutes-seconds separator
    \d{2}       # 2 digits for seconds
    \s          # single whitespace
    [AP]M       # day period (e.g. AM or PM)
)               # 'time' group end
                # any ending of the string
"""

RX_TIME = """
# Capturing regular event datetime stamp. E.g.:
#
# "[8:33:05 PM] foo"
#
# "8:33:05 PM" will be captured into 'time' group.
^               # beginning of the string
\[              # left time wrapper
{time}          # time regex placeholder
\]              # right time wrapper
                # any ending of the string
""".format(time=RX_TIME_BASE)

RX_DATE_TIME = """
# Capturing regular event datetime stamp. E.g.:
#
# "[Sep 15, 2013 8:33:05 PM] foo"
#
# "Sep 15, 2013" will be captured into 'date' group,
# "8:33:05 PM" will be captured into 'time' group.
^               # beginning of the string
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
{time}          # time regex placeholder
\]              # closing brackets
                # any ending of the string
""".format(time=RX_TIME_BASE)

RX_POS = """
# Capturing map position of the event. E.g.:
#
# "Something has happened at 100.0 200.99"
#
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
                # any beginning of the string
\s              # single whitespace
at              #
\s              # single whitespace
(?P<pos_x>      # 'pos_x' group start
    \d+         # 1 or more digits for integer part
    .           # decimal separator
    \d{1,3}     # 1 to 3 digits for real part
)               # 'pos_x' group end
\s              # single whitespace
(?P<pos_y>      # 'pos_y' group start
    \d+         # 1 or more digits for integer part
    .           # decimal separator
    \d{1,3}     # 1 to 3 digits for real part
)               # 'pos_y' group end
$               # end of the string
"""

RX_TOGGLE_VALUE = """
# Capturing pilot's callsign. E.g.:
#
# "something is on"
#
# "on" will be captured into 'value' group.
                # any beginning of the string
(?P<value>      # 'value' group start
    on|off      # switch value (e.g. 'on' or 'off')
)               # 'value' group end
                # any ending of the string
"""

RX_CALLSIGN = """
# Capturing pilot's callsign. E.g.:
#
# "    User   "
#
# "User" will be captured into 'callsign' group.
                # any beginning of the string
(?P<callsign>   # 'callsign' group start
    \S+         # one or more non-whitespace characters
)               # 'callsign' group end
                # any ending of the string
"""

RX_SEAT = """
# Capturing current user's seat. E.g.:
#
# "Pe-8(0) seat occupied"
#
# "0" will be captured into 'seat' group.
                # any beginning of the string
\(              # opening parenthesis
(?P<seat>       # 'seat' group start
    \d+         # one or more digits for seat number
)               # 'seat' group end
\)              # closing parenthesis
                # any ending of the string
"""

RX_AIRCRAFT = """
# Capturing pilot's aircraft. E.g.:
#
# "User:Pe-8"
#
# "Pe-8" will be captured into 'aircraft' group.
                # any beginning of the string
:               # a colon
(?P<aircraft>   # 'aircraft' group start
    \S+         # one or more non-whitespace characters
)               # 'aircraft' group end
                # any ending of the string
"""

RX_ENEMY_CALLSIGN_AIRCRAFT = """
# Capturing enemy pilot's callsign and aircraft. E.g.:
#
# "  User:Pe-8   "
#
# "User" will be captured into 'e_callsign' group,
# "Pe-8" will be captured into 'e_aircraft' group.
                # any beginning of the string
(?P<e_callsign> # 'e_callsign' group start
    \S+         # one or more non-whitespace characters
)               # 'e_callsign' group end
:               # a colon
(?P<e_aircraft> # 'e_aircraft' group start
    \S+         # one or more non-whitespace characters
)               # 'e_aircraft' group end
                # any ending of the string
"""

RX_STATIC = """
# Capturing static's name. E.g.:
#
# "  0_Static  "
#
# "0_Static" will be captured into 'static' group.
                # any beginning of the string
(?P<static>     # 'static' group start
    \d+         # one or more digits for static's ID
    _Static     #
)               # 'static' group end
                # any ending of the string
"""

RX_CALLSIGN_AIRCRAFT = """
# Capturing pilot's callsign and aircraft. E.g.:
#
# "  User:Pe-8   "
#
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group.
                # any beginning of the string
{callsign}      # callsign regex placeholder
{aircraft}      # aircraft regex placeholder
                # any ending of the string
""".format(callsign=RX_CALLSIGN, aircraft=RX_AIRCRAFT)

RX_TIME_CALLSIGN = """
# Capturing time and pilot's callsign. E.g.:
#
# "[8:33:05 PM] User  "
#
# "8:33:05 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group.
{time}          # time regex placeholder
\s              # single whitespace
{callsign}      # callsign regex placeholder
                # any ending of the string
""".format(time=RX_TIME, callsign=RX_CALLSIGN)

RX_TIME_AIRCRAFT = """
# Capturing time, pilot's callsign and aircraft. E.g.:
#
# "[8:33:05 PM] User:Pe-8  "
#
# "8:33:05 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group.
{time}              # time regex placeholder
\s                  # single whitespace
{callsign_aircraft} # callsign with aircraft regex placeholder
                    # any ending of the string
""".format(time=RX_TIME, callsign_aircraft=RX_CALLSIGN_AIRCRAFT)

RX_TIME_SEAT = """
# Capturing time, pilot's callsign, aircraft and seat number. E.g.:
#
# "[8:33:05 PM] User:Pe-8(0)  "
#
# "8:33:05 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "0" will be captured into 'seat' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
{seat}          # seat regex placeholder
                # any ending of the string
""".format(time_aircraft=RX_TIME_AIRCRAFT, seat=RX_SEAT)

RX_DESTROYED_BY = """
# Capturing objrct destroyed by user event. E.g.:
#
# " destroyed by User:Pe-8 at 100.0 200.99"
#
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
\s                  # single whitespace
destroyed           #
\s                  # single whitespace
by                  #
\s                  # single whitespace
{callsign_aircraft} # callsign with aircraft regex placeholder
{pos}               # position regex placeholder
""".format(callsign_aircraft=RX_CALLSIGN_AIRCRAFT, pos=RX_POS)

#------------------------------------------------------------------------------
# Mission flow
#------------------------------------------------------------------------------

RX_MISSION_PLAYING = """
# Capture mission playing event. E.g.:
#
# "[Sep 15, 2013 8:33:05 PM] Mission: PH.mis is Playing"
#
# "Sep 15, 2013" will be captured into 'date' group,
# "8:33:05 PM" will be captured into 'time' group,
# "PH.mis" will be captured into 'mission' group.
{datetime}      # datetime regex placeholder
\s              # single whitespace
Mission:        #
\s              # single whitespace
(?P<mission>    # 'mission' group start
    .+          # any one or more symbols (e.g. "test" or "dogfight/test")
    \.mis       # mission file extension
)               # 'mission' group end
\s              # single whitespace
is              #
\s              # single whitespace
Playing         #
$               # end of the string
""".format(datetime=RX_DATE_TIME)

RX_MISSION_BEGIN = """
# Capture mission beginning event. E.g.:
#
# "[8:33:05 PM] Mission BEGIN"
#
# "8:33:05 PM" will be captured into 'time' group.
{time}          # time regex placeholder
\s              # single whitespace
Mission         #
\s              # single whitespace
BEGIN           #
$               # end of the string
""".format(time=RX_TIME)

RX_MISSION_END = """
# Capture mission end event. E.g.:
#
# "[8:33:05 PM] Mission END"
#
# "8:33:05 PM" will be captured into 'time' group.
{time}          # time regex placeholder
\s              # single whitespace
Mission         #
\s              # single whitespace
END             #
$               # end of the string
""".format(time=RX_TIME)

#------------------------------------------------------------------------------
# Action events
#------------------------------------------------------------------------------

RX_CONNECTED = """
# Capture user connection event. E.g.:
#
# "[8:45:57 PM] User has connected"
#
# "8:45:57 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group.
{time_callsign} # time with callsign regex placeholder
\s              # single whitespace
has             #
\s              # single whitespace
connected       #
$               # end of the string
""".format(time_callsign=RX_TIME_CALLSIGN)

RX_DISCONNECTED = """
# Capture user disconnection event. E.g.:
#
# "[8:46:37 PM] User has disconnected"
#
# "8:46:37 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group.
{time_callsign} # time with callsign regex placeholder
\s              # single whitespace
has             #
\s              # single whitespace
disconnected    #
$               # end of the string
""".format(time_callsign=RX_TIME_CALLSIGN)

RX_WENT_TO_MENU = """
# Capture user went to refly menu event. E.g.:
#
# "[8:49:20 PM] User entered refly menu"
#
# "8:49:20 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group.
{time_callsign} # time with callsign regex placeholder
\s              # single whitespace
entered         #
\s              # single whitespace
refly           #
\s              # single whitespace
menu            #
$               # end of the string
""".format(time_callsign=RX_TIME_CALLSIGN)

RX_SELECTED_ARMY = """
# Capture user selected army event. E.g.:
#
# "[8:46:55 PM] User selected army Red at 100.0 200.99"
#
# "8:46:55 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Red" will be captured into 'army' group,
# "53377.0" will be captured into 'pos_x' group,
# "1303.10" will be captured into 'pos_y' group.
{time_callsign} # time with callsign regex placeholder
\s              # single whitespace
selected        #
\s              # single whitespace
army            #
\s              # single whitespace
(?P<army>       # 'army' group start
    \S+         # one or more non-whitespace characters
)               # 'army' group end
{pos}           # position regex placeholder
""".format(time_callsign=RX_TIME_CALLSIGN, pos=RX_POS)

RX_IN_FLIGHT = """
# Capture user took-off event. E.g.:
#
# "[8:49:32 PM] User:Pe-8 in flight at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
in              #
\s              # single whitespace
flight          #
{pos}           # position regex placeholder
""".format(time_aircraft=RX_TIME_AIRCRAFT, pos=RX_POS)

RX_WEAPONS_LOADED = """
# Capture user weapons load event. E.g.:
#
# "[8:49:35 PM] User:Pe-8 loaded weapons '40fab100' fuel 40%"
#
# "8:49:35 PM PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "40fab100" will be captured into 'weapons' group,
# "40" will be captured into 'fuel' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
loaded          #
\s              # single whitespace
weapons         #
\s              # single whitespace
\'              # opening single quote
(?P<loadout>    # 'loadout' group start
    \S+         # one or more non-whitespace characters
)               # 'loadout' group end
\'              # closing single quote
\s              # single whitespace
fuel            #
\s              # single whitespace
(?P<fuel>       # 'fuel' group start
    \d{{2,3}}   # 2 or 3 digits for fuel percentage
)               # 'fuel' group end
%               # percent sign
$
""".format(time_aircraft=RX_TIME_AIRCRAFT, pos=RX_POS)

RX_SEAT_OCCUPIED = """
# Capture user occupied seat event. E.g.:
#
# "[8:49:39 PM] User:Pe-8(0) seat occupied by User at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "0" will be captured into 'seat' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_seat}     # time with pilot's callsign, aircraft and seat regex placeholder
\s              # single whitespace
seat            #
\s              # single whitespace
occupied        #
\s              # single whitespace
.*              # zero or more symbols
{pos}           # position regex placeholder
""".format(time_seat=RX_TIME_SEAT, pos=RX_POS)

RX_BAILED_OUT = """
# Capture crew member bailed out event. E.g.:
#
# "[9:31:20 PM] User:Pe-8(0) bailed out at 100.0 200.99"
#
# "9:31:20 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "0" will be captured into 'seat' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_seat}     # time with pilot's callsign, aircraft and seat regex placeholder
\s              # single whitespace
bailed          #
\s              # single whitespace
out             #
{pos}           # position regex placeholder
""".format(time_seat=RX_TIME_SEAT, pos=RX_POS)

RX_PARACHUTE_OPENED = """
# Capture crew member's parachute opened event. E.g.:
#
# "[9:33:20 PM] User:Pe-8(0) successfully bailed out at 100.0 200.99"
#
# "9:33:20 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "0" will be captured into 'seat' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_seat}     # time with pilot's callsign, aircraft and seat regex placeholder
\s              # single whitespace
successfully    #
\s              # single whitespace
bailed          #
\s              # single whitespace
out             #
{pos}           # position regex placeholder
""".format(time_seat=RX_TIME_SEAT, pos=RX_POS)

RX_TOGGLE_LANDING_LIGHTS = """
# Capture user toggled landing lights event. E.g.:
#
# "[9:33:20 PM] User:Pe-8 turned landing lights off at 100.0 200.99"
#
# "9:33:20 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "off" will be captured into 'value' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
turned          #
\s              # single whitespace
landing         #
\s              # single whitespace
lights          #
\s              # single whitespace
{toggle}        # toggling value regex placeholder
{pos}           # position regex placeholder
""".format(time_aircraft=RX_TIME_AIRCRAFT, toggle=RX_TOGGLE_VALUE, pos=RX_POS)

RX_TOGGLE_WINGTIP_SMOKES = """
# Capture user toggled wingtip smokes event. E.g.:
#
# "[9:33:20 PM] User:Pe-8 turned wingtip smokes off at 100.0 200.99"
#
# "9:33:20 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "off" will be captured into 'value' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
turned          #
\s              # single whitespace
wingtip         #
\s              # single whitespace
smokes          #
\s              # single whitespace
{toggle}        # toggling value regex placeholder
{pos}           # position regex placeholder
""".format(time_aircraft=RX_TIME_AIRCRAFT, toggle=RX_TOGGLE_VALUE, pos=RX_POS)

RX_WOUNDED = """
# Capture crew member wounded event. E.g.:
#
# "[8:49:39 PM] User:Pe-8(0) was wounded at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "0" will be captured into 'seat' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_seat}     # time with pilot's callsign, aircraft and seat regex placeholder
\s              # single whitespace
was             #
\s              # single whitespace
wounded         #
{pos}           # position regex placeholder
""".format(time_seat=RX_TIME_SEAT, pos=RX_POS)

RX_HEAVILY_WOUNDED = """
# Capture crew member heavily wounded event. E.g.:
#
# "[8:49:39 PM] User:Pe-8(0) was heavily wounded at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "0" will be captured into 'seat' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_seat}     # time with pilot's callsign, aircraft and seat regex placeholder
\s              # single whitespace
was             #
\s              # single whitespace
heavily         #
\s              # single whitespace
wounded         #
{pos}           # position regex placeholder
""".format(time_seat=RX_TIME_SEAT, pos=RX_POS)

RX_KILLED = """
# Capture crew member killed event. E.g.:
#
# "[8:49:39 PM] User:Pe-8(0) was killed at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "0" will be captured into 'seat' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_seat}     # time with pilot's callsign, aircraft and seat regex placeholder
\s              # single whitespace
was             #
\s              # single whitespace
killed          #
{pos}           # position regex placeholder
""".format(time_seat=RX_TIME_SEAT, pos=RX_POS)

RX_KILLED_BY_EAIR = """
# Capture crew member killed event. E.g.:
#
# "[8:49:39 PM] User1:Pe-8(0) was killed by User2:Bf-109G-6_Late at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User1" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "0" will be captured into 'seat' group,
# "User2" will be captured into 'e_callsign' group,
# "Bf-109G-6_Late" will be captured into 'e_aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_seat}     # time with pilot's callsign, aircraft and seat regex placeholder
\s              # single whitespace
was             #
\s              # single whitespace
killed          #
\s              # single whitespace
by              #
\s              # single whitespace
{eair}          # enemy callsign with aircraft regex placeholder
{pos}           # position regex placeholder
""".format(time_seat=RX_TIME_SEAT, eair=RX_ENEMY_CALLSIGN_AIRCRAFT, pos=RX_POS)

RX_CAPTURED = """
# Capture crew member captured by enemies event. E.g.:
#
# "[8:49:39 PM] User:Pe-8(0) was captured at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "0" will be captured into 'seat' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_seat}     # time with pilot's callsign, aircraft and seat regex placeholder
\s              # single whitespace
was             #
\s              # single whitespace
captured        #
{pos}           # position regex placeholder
""".format(time_seat=RX_TIME_SEAT, pos=RX_POS)

RX_CRASHED = """
# Capture user crashed event. E.g.:
#
# "[8:49:32 PM] User:Pe-8 crashed at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
crashed         #
{pos}           # position regex placeholder
""".format(time_aircraft=RX_TIME_AIRCRAFT, pos=RX_POS)

RX_LANDED = """
# Capture user landed event. E.g.:
#
# "[8:49:32 PM] User:Pe-8 landed at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
landed          #
{pos}           # position regex placeholder
""".format(time_aircraft=RX_TIME_AIRCRAFT, pos=RX_POS)

RX_DAMAGED_ON_GROUND = """
# Capture user damaged on the ground event. E.g.:
#
# "[8:49:32 PM] User:Pe-8 damaged on the ground at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
damaged         #
\s              # single whitespace
on              #
\s              # single whitespace
the             #
\s              # single whitespace
ground          #
{pos}           # position regex placeholder
""".format(time_aircraft=RX_TIME_AIRCRAFT, pos=RX_POS)

RX_DAMAGED_SELF = """
# Capture user damaged self event. E.g.:
#
# "[8:49:32 PM] User:Pe-8 damaged by landscape at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
damaged         #
\s              # single whitespace
by              #
\s              # single whitespace
landscape       #
{pos}           # position regex placeholder
""".format(time_aircraft=RX_TIME_AIRCRAFT, pos=RX_POS)

RX_DAMAGED_BY_EAIR = """
# Capture user damaged by another user event. E.g.:
#
# "[8:49:32 PM] User1:Pe-8 damaged by User2:Bf-109G-6_Late at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User1" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "User2" will be captured into 'e_callsign' group,
# "Bf-109G-6_Late" will be captured into 'e_aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
damaged         #
\s              # single whitespace
by              #
\s              # single whitespace
{eair}          # enemy callsign with aircraft regex placeholder
{pos}           # position regex placeholder
""".format(time_aircraft=RX_TIME_AIRCRAFT, eair=RX_ENEMY_CALLSIGN_AIRCRAFT, pos=RX_POS)

RX_SHOT_DOWN_SELF = """
# Capture user shot down self event. E.g.:
#
# "[8:49:32 PM] User:Pe-8 shot down by landscape at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
shot            #
\s              # single whitespace
down            #
\s              # single whitespace
by              #
\s              # single whitespace
landscape       #
{pos}           # position regex placeholder
""".format(time_aircraft=RX_TIME_AIRCRAFT, pos=RX_POS)

RX_SHOT_DOWN_BY_EAIR = """
# Capture user shot down by another user event. E.g.:
#
# "[8:49:32 PM] User1:Pe-8 shot down by User2:Bf-109G-6_Late at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User1" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "User2" will be captured into 'e_callsign' group,
# "Bf-109G-6_Late" will be captured into 'e_aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
shot            #
\s              # single whitespace
down            #
\s              # single whitespace
by              #
\s              # single whitespace
{eair}          # enemy callsign with aircraft regex placeholder
{pos}           # position regex placeholder
""".format(time_aircraft=RX_TIME_AIRCRAFT, eair=RX_ENEMY_CALLSIGN_AIRCRAFT, pos=RX_POS)

RX_SHOT_DOWN_BY_STATIC = """
# Capture user shot down by static event. E.g.:
#
# "[8:49:32 PM] User:Pe-8 shot down by 0_Static at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "0_Static" will be captured into 'static' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time_aircraft} # time with callsign and aircraft regex placeholder
\s              # single whitespace
shot            #
\s              # single whitespace
down            #
\s              # single whitespace
by              #
\s              # single whitespace
{static}        # static regex placeholder
{pos}           # position regex placeholder
""".format(time_aircraft=RX_TIME_AIRCRAFT, static=RX_STATIC, pos=RX_POS)

RX_DESTROYED_BLD = """
# Capture user destroyed building event. E.g.:
#
# "[8:49:39 PM] 3do/Buildings/Finland/CenterHouse1_w/live.sim destroyed by User:Pe-8 at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "CenterHouse1_w" will be captured into 'building' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time}          # time regex placeholder
\s              # single whitespace
3do/Buildings/  #
\S+             # one or more non-whitespace characters
/               # single slash
(?P<building>   # 'building' group start
    \S+         # one or more non-whitespace characters
)               # 'building' group end
/               # single slash
\S+             # one or more non-whitespace characters
\.sim           # object's file extension
{destroyed_by}  # destroyed by regex placeholder
""".format(time=RX_TIME, destroyed_by=RX_DESTROYED_BY)

RX_DESTROYED_TREE = """
# Capture user destroyed tree event. E.g.:
#
# "[8:49:39 PM] 3do/Tree/Line_W/live.sim destroyed by User:Pe-8 at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "Line_W" wiil be captured into 'tree' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time}          # time regex placeholder
\s              # single whitespace
3do/Tree/       #
(?P<tree>       # 'tree' group start
    \S+         # one or more non-whitespace characters
)               # 'tree' group end
/               # single slash
\S+             # one or more non-whitespace characters
\.sim           # object's file extension
{destroyed_by}  # destroyed by regex placeholder
""".format(time=RX_TIME, destroyed_by=RX_DESTROYED_BY)

RX_DESTROYED_STATIC = """
# Capture user destroyed static event. E.g.:
#
# "[8:49:39 PM] 0_Static destroyed by User:Pe-8 at 100.0 200.99"
#
# "8:49:32 PM" will be captured into 'time' group,
# "0_Static" wiil be captured into 'static' group,
# "User" will be captured into 'callsign' group,
# "Pe-8" will be captured into 'aircraft' group,
# "100.0" will be captured into 'pos_x' group,
# "200.99" will be captured into 'pos_y' group.
{time}          # time regex placeholder
\s              # single whitespace
{static}        # static regex placeholder
{destroyed_by}  # destroyed by regex placeholder
""".format(time=RX_TIME, static=RX_STATIC, destroyed_by=RX_DESTROYED_BY)
