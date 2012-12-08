#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, division, unicode_literals
import unittest

from emang import utils


class TestUtils(unittest.TestCase):
    def test_decode(self):
        test = utils.decode("すぱむ")
        self.assertEqual(test, "すぱむ")
        utils.decode("すぱむ".encode("utf8"))
        self.assertEqual(test, "すぱむ")
