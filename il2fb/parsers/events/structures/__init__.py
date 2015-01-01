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

    def to_primitive(self, context=None):
        fields = ((key, getattr(self, key)) for key in self.__slots__)
        return {
            key: self._to_primitive(value, context)
            for key, value in fields
        }

    @staticmethod
    def _to_primitive(instance, context):
        from candv import SimpleConstant
        from il2fb.commons.organization import Regiment

        if isinstance(instance, (Base, SimpleConstant, Regiment)):
            return instance.to_primitive(context)
        elif hasattr(instance, 'isoformat'):
            return instance.isoformat()
        else:
            return instance


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


class HumanAircraftCrewMember(HumanAircraft):
    __slots__ = HumanAircraft.__slots__ + ['seat_number', ]

    def __init__(self, callsign, aircraft, seat_number):
        super(HumanAircraftCrewMember, self).__init__(callsign, aircraft)
        self.seat_number = seat_number

    def __repr__(self):
        return ("<Human aircraft crew member #{0} at {1}:{2}>"
                .format(self.seat_number, self.callsign, self.aircraft))


class AIAircraftCrewMember(Base):
    __slots__ = ['aircraft', 'seat_number', ]

    def __init__(self, aircraft, seat_number):
        self.aircraft = aircraft
        self.seat_number = seat_number

    def __repr__(self):
        return "<AI aircraft crew member {0}:{1}>".format(self.aircraft,
                                                          self.seat_number)
