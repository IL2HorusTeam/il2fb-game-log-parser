# -*- coding: utf-8 -*-


class Base(object):
    __slots__ = []

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return all([
            getattr(self, x) == getattr(other, x)
            for x in self.__slots__
        ])

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(tuple(
            getattr(self, x) for x in self.__slots__
        ))


class Point2D(Base):
    __slots__ = ['x', 'y', ]

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "<Point2D '{0};{1}'>".format(self.x, self.y)


class HumanAircraft(Base):
    __slots__ = ['callsign', 'aircraft', ]

    def __init__(self, callsign, aircraft):
        self.callsign = callsign
        self.aircraft = aircraft

    def __repr__(self):
        return "<Human aircraft {0}:{1}>".format(self.callsign, self.aircraft)


class HumanCrewMember(HumanAircraft):
    __slots__ = HumanAircraft.__slots__ + ['seat_number', ]

    def __init__(self, callsign, aircraft, seat_number):
        super(HumanCrewMember, self).__init__(callsign, aircraft)
        self.seat_number = seat_number

    def __repr__(self):
        return ("<Human crew member #{0} at {1}:{2}>"
                .format(self.seat_number, self.callsign, self.aircraft))


class AIAircraftCrewMember(Base):
    __slots__ = ['aircraft', 'seat_number', ]

    def __init__(self, aircraft, seat_number):
        self.aircraft = aircraft
        self.seat_number = seat_number

    def __repr__(self):
        return "<AI aircraft crew member {0}:{1}>".format(self.callsign,
                                                          self.aircraft)
