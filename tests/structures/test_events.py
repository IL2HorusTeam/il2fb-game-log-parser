# -*- coding: utf-8 -*-

import inspect

from il2fb.parsers.events.structures import events

from ..base import BaseTestCase


class EventsStructuresTestCase(BaseTestCase):

    def test_structures_defined_in_all(self):
        for name, obj in inspect.getmembers(events):
            if (
                inspect.isclass(obj)
                and issubclass(obj, events.Event)
                and obj is not events.Event
            ):
                self.assertIn(obj.__name__, events.__all__)
