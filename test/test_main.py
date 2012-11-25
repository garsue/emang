#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import unittest

from mock import patch
from emang import main


class TestMain(unittest.TestCase):
    def test_invalid_command(self):
        with patch("__builtin__.print") as m:
            main.invalid_command()
            args, _ = m.call_args
            self.assertEqual(args[0], "No such a command")

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
