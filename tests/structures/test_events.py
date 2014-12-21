# -*- coding: utf-8 -*-

import inspect

from il2fb.parsers.events.structures import events

from ..base import BaseTestCase


class EventsStructuresTestCase(BaseTestCase):

    def setUp(self):

        def members_filter(element):
            name, obj = element
            return (inspect.isclass(obj)
                    and issubclass(obj, events.Event)
                    and obj is not events.Event)

        self.structures = filter(members_filter, inspect.getmembers(events))

    def test_structures_defined_in_all(self):
        for name, structure in self.structures:
            self.assertIn(name, events.__all__)
