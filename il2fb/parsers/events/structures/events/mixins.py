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
EventWithActor = mixin_for_attribute('actor')
EventWithVictim = mixin_for_attribute('victim')
EventWithAggressor = mixin_for_attribute('aggressor')


class EventWithDateTime(EventWithDate, EventWithTime):
    pass


class EventWithToggleValue(object):

    def __init__(self, **kwargs):
        super(EventWithToggleValue, self).__init__(**kwargs)
        self.value = kwargs['toggle_value'].value
