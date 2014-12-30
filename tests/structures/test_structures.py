# -*- coding: utf-8 -*-

from datetime import time, date
from il2fb.parsers.events.structures import Point2D, serialize


from ..base import BaseTestCase


class StructuresTestCase(BaseTestCase):

    def test_serialize(self):
        self.assertEqual(serialize("test"), "test")
        self.assertEqual(serialize(lambda: 100), 100)
        self.assertEqual(serialize(date(1999, 12, 31)), "1999-12-31")
        self.assertEqual(serialize(time(12, 34, 56)), "12:34:56")

        p = Point2D(1, 2)
        self.assertEqual(serialize(p), {'x': 1, 'y': 2})

        p = Point2D(lambda: 1, lambda: 2)
        self.assertEqual(serialize(p), {'x': 1, 'y': 2})
