#!/usr/bin/env python
#vim: fileencoding=utf-8

import unittest

from emang import main


class TestMain(unittest.TestCase):
    def test_invalid_command(self):
        self.assertIsNone(main.invalid_command())

    def test_dispatch(self):
        test = main.dispatch("autorename")
        self.assertEqual(test.__module__, "emang.autorename")
        self.assertEqual(test.__name__, "main")
        test = main.dispatch("manual")
        self.assertEqual(test.__module__, "emang.manual")
        self.assertEqual(test.__name__, "main")
        test = main.dispatch("invalid")
        self.assertEqual(test.__module__, "emang.main")
        self.assertEqual(test.__name__, "invalid_command")
