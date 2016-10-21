# coding: utf-8

from il2fb.commons.structures import BaseStructure


class Actor(BaseStructure):
    pass


class Human(Actor):
    __slots__ = ['callsign', ]

    def __init__(self, callsign):
        self.callsign = callsign

    def __repr__(self):
        return "<Human {0}>".format(self.callsign)


class HumanAircraft(Human):
    __slots__ = Human.__slots__ + ['aircraft', ]

    def __init__(self, callsign, aircraft):
        super(HumanAircraft, self).__init__(callsign)
        self.aircraft = aircraft

    def __repr__(self):
        return "<Human aircraft {0}:{1}>".format(self.callsign, self.aircraft)


class HumanAircraftCrewMember(HumanAircraft):
    __slots__ = HumanAircraft.__slots__ + ['seat_number', ]

    def __init__(self, callsign, aircraft, seat_number):
        super(HumanAircraftCrewMember, self).__init__(callsign, aircraft)
        self.seat_number = seat_number

    def __repr__(self):
        return (
            "<Human aircraft crew member #{0} at {1}:{2}>"
            .format(self.seat_number, self.callsign, self.aircraft)
        )


class AIMovingUnitMember(Actor):
    __slots__ = ['unit_id', 'index', ]

    def __init__(self, unit_id, index):
        self.unit_id = unit_id
        self.index = index

    def __repr__(self):
        return (
            "<Moving unit member {0}:{1}>"
            .format(self.unit_id, self.index)
        )
