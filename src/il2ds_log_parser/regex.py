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
# Actor events
#------------------------------------------------------------------------------

RX_POS = r" at (?P<pos_x>\d+.\d+) (?P<pos_y>\d+.\d+)$"
RX_CALLSIGN = r"(?P<callsign>.+)"
RX_SEAT = r"\((?P<seat>\d+)\)"

RX_AIRCRAFT = r":(?P<aircraft>.+)"
RX_CALLSIGN_AIRCRAFT = RX_CALLSIGN + RX_AIRCRAFT
RX_CALLSIGN_AIRCRAFT_POS = RX_CALLSIGN_AIRCRAFT + RX_POS

RX_TIME_CALLSIGN = RX_TIME + " " + RX_CALLSIGN
RX_TIME_CALLSIGN_AIRCRAFT = RX_TIME + " " + RX_CALLSIGN_AIRCRAFT
RX_TIME_SEAT = RX_TIME_CALLSIGN_AIRCRAFT + RX_SEAT

RX_CONNECTED = RX_TIME_CALLSIGN + r" has connected$"
RX_DISCONNECTED = RX_TIME_CALLSIGN + r" has disconnected$"
RX_WENT_TO_MENU = RX_TIME_CALLSIGN + r" entered refly menu$"

RX_WEAPONS_LOADED = RX_TIME_CALLSIGN_AIRCRAFT + r" loaded weapons \'(?P<loadout>.+)\' fuel (?P<fuel>\d{2,3})%$"
RX_SELECTED_ARMY = RX_TIME_CALLSIGN + r" selected army (?P<army>.+)" + RX_POS
RX_SEAT_OCCUPIED = RX_TIME_SEAT + r" seat occupied .*" + RX_POS
RX_BAILED_OUT = RX_TIME_SEAT + r" bailed out" + RX_POS
RX_SUCCESSFULLY_BAILED_OUT = RX_TIME_SEAT + r" successfully bailed out" + RX_POS
RX_LANDING_LIGHTS = RX_TIME_CALLSIGN_AIRCRAFT + r" turned landing lights (?P<value>on|off)" + RX_POS
RX_WINGTIP_SMOKES = RX_TIME_CALLSIGN_AIRCRAFT + r" turned wingtip smokes (?P<value>on|off)" + RX_POS
RX_IN_FLIGHT = RX_TIME_CALLSIGN_AIRCRAFT + r" in flight" + RX_POS
RX_WOUNDED = RX_TIME_SEAT + r" was wounded" + RX_POS
RX_HEAVILY_WOUNDED = RX_TIME_SEAT + r" was heavily wounded" + RX_POS
RX_KILLED = RX_TIME_SEAT + r" was killed" + RX_POS
RX_CAPTURED = RX_TIME_SEAT + r" was captured" + RX_POS
RX_DESTROYED_BLD = RX_TIME + r" 3do/Buildings/.+/(?P<building>.+)/.+\.sim destroyed by " + RX_CALLSIGN_AIRCRAFT_POS
RX_DESTROYED_STATIC = RX_TIME + r"(?P<static>.+) destroyed by " + RX_CALLSIGN_AIRCRAFT_POS
RX_CRASHED = RX_TIME_CALLSIGN_AIRCRAFT + r" crashed" + RX_POS
RX_LANDED = RX_TIME_CALLSIGN_AIRCRAFT + r" landed" + RX_POS
RX_DAMAGED_ON_GROUND = RX_TIME_CALLSIGN_AIRCRAFT + r" damaged on the ground" + RX_POS
RX_DAMAGED_SELF = RX_TIME_CALLSIGN_AIRCRAFT + r" damaged by landscape" + RX_POS
