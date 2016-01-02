# -*- coding: utf-8 -*-

from il2fb.commons.structures import BaseStructure


class HumanAircraft(BaseStructure):
    __slots__ = ['callsign', 'aircraft', ]

    def __init__(self, callsign, aircraft):
        self.callsign = callsign
        self.aircraft = aircraft

    def __repr__(self):
        return "<Human aircraft {0}:{1}>".format(self.callsign, self.aircraft)


class HumanAircraftCrewMember(HumanAircraft):
    __slots__ = HumanAircraft.__slots__ + ['seat_number', ]

    def __init__(self, callsign, aircraft, seat_number):
        super(HumanAircraftCrewMember, self).__init__(callsign, aircraft)
        self.seat_number = seat_number

    def __repr__(self):
        return ("<Human aircraft crew member #{0} at {1}:{2}>"
                .format(self.seat_number, self.callsign, self.aircraft))


class AIAircraftCrewMember(BaseStructure):
    __slots__ = ['aircraft', 'seat_number', ]

    def __init__(self, aircraft, seat_number):
        self.aircraft = aircraft
        self.seat_number = seat_number

    def __repr__(self):
        return "<AI aircraft crew member {0}:{1}>".format(self.aircraft,
                                                          self.seat_number)


class MovingUnitMember(BaseStructure):
    __slots__ = ['moving_unit', 'index', ]

    def __init__(self, moving_unit, index):
        self.moving_unit = moving_unit
        self.index = index

    def __repr__(self):
        return "<Moving unit member {0}:{1}>".format(self.moving_unit,
                                                     self.index)
