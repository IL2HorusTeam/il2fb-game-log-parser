# coding: utf-8

import unittest


class BaseTestCase(unittest.TestCase):

    maxDiff = None

    def assertRaisesWithMessage(self, exception_type, message, func,
                                *args, **kwargs):
        try:
            func(*args, **kwargs)
        except exception_type as e:
            self.assertEqual(e.args[0], message)
        else:
            self.fail(
                '"{:}" was expected to throw "{:}" exception'
                .format(func.__name__, exception_type.__name__))
