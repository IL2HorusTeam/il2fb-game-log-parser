# coding: utf-8

from il2fb.commons.structures import BaseStructure


class Actor(BaseStructure):

    def __repr__(self):
        return "<Actor>"


class Human(Actor):
    __slots__ = ['callsign', ]

    def __init__(self, callsign):
        self.callsign = callsign

    def __repr__(self):
        return "<Human '{0}'>".format(self.callsign)


class HumanAircraft(Human):
    __slots__ = Human.__slots__ + ['aircraft', ]

    def __init__(self, callsign, aircraft):
        super(HumanAircraft, self).__init__(callsign)
        self.aircraft = aircraft

    def __repr__(self):
        return "<Human aircraft '{0}:{1}'>".format(self.callsign, self.aircraft)


class HumanAircraftCrewMember(HumanAircraft):
    __slots__ = HumanAircraft.__slots__ + ['index', ]

    def __init__(self, callsign, aircraft, index):
        super(HumanAircraftCrewMember, self).__init__(callsign, aircraft)
        self.index = index

    def __repr__(self):
        return (
            "<Human aircraft crew member #{0} in '{1}:{2}'>"
            .format(self.index, self.callsign, self.aircraft)
        )


class AIAircraft(Actor):
    __slots__ = ['flight', 'index', ]

    def __init__(self, flight, index):
        self.flight = flight
        self.index = index

    def __repr__(self):
        return "<AI aircraft #{0} in '{1}'>".format(self.index, self.flight)


class Unit(Actor):
    __slots__ = ['id', ]

    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return "<Unit '{0}'>".format(self.id)


class StationaryUnit(Unit):

    def __repr__(self):
        return "<Stationary unit '{0}'>".format(self.id)


class MovingUnitMember(Unit):
    __slots__ = Unit.__slots__ + ['index', ]

    def __init__(self, id, index):
        super(MovingUnitMember, self).__init__(id)
        self.index = index

    def __repr__(self):
        return "<Moving unit member #{0} in '{1}'>".format(self.index, self.id)


class Building(Actor):
    __slots__ = ['name', ]

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<Building '{0}'>".format(self.name)
