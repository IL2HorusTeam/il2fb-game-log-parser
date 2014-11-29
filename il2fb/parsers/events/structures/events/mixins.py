# -*- coding: utf-8 -*-


def mixin_for_attribute(attribute_name):

    class Mixin(object):

        def __init__(self, **kwargs):
            super(Mixin, self).__init__(**kwargs)
            value = kwargs[attribute_name]
            setattr(self, attribute_name, value)

    return Mixin


EventWithTime = mixin_for_attribute('time')
EventWithDate = mixin_for_attribute('date')
EventWithBelligerent = mixin_for_attribute('belligerent')
EventWithPos = mixin_for_attribute('pos')
EventWithCallsign = mixin_for_attribute('callsign')
EventWithAircraft = mixin_for_attribute('aircraft')
EventWithCrewMember = mixin_for_attribute('crew_member')
EventWithEnemy = mixin_for_attribute('enemy')


class EventWithDateTime(EventWithDate, EventWithTime):
    pass


class EventWithPilot(EventWithCallsign, EventWithAircraft):
    pass


class EventWithToggleValue(object):

    def __init__(self, **kwargs):
        super(EventWithToggleValue, self).__init__(**kwargs)
        self.value = kwargs['toggle_value'].value
