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
EventWithCallsign = mixin_for_attribute('callsign')
EventWithBelligerent = mixin_for_attribute('belligerent')
EventWithPos = mixin_for_attribute('pos')


class EventWithDateTime(EventWithDate, EventWithTime):
    pass
