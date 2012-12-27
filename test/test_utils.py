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

    def test_normalize(self):
        target = b"\xe3\x81\x99\xe3\x81\xaf\xe3\x82\x9a\xe3\x82\x80"  # NFD
        test = utils.normalize(target.decode("utf8")).encode("utf8")
        self.assertEqual(test, "すぱむ".encode("utf8"))
