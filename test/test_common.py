#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import unittest

from emang import common


class TestCommon(unittest.TestCase):
    class Empty(object):
        pass

    orignal = Empty()
    orignal.path = Empty()
    orignal.os = Empty()
    orignal.path.isfile = common.path.isfile
    orignal.os.listdir = common.os.listdir
    orignal.os.rename = common.os.rename
    orignal.to_abspath = common.to_abspath

    def setUp(self):
        pass

    def test_decode(self):
        test = common.decode("すぱむ")
        self.assertEqual(test, "すぱむ")
        common.decode("すぱむ".encode("utf8"))
        self.assertEqual(test, "すぱむ")

    def tearDown(self):
        common.path.isfile = self.orignal.path.isfile
        common.os.listdir = self.orignal.os.listdir
        common.os.rename = self.orignal.os.rename
        common.os.to_abspath = self.orignal.to_abspath

    def test_get_files(self):
        files = [
            ".hidden".encode("utf8"),
            "filename".encode("utf8"),
            "マルチバイト".encode("utf8")]
        common.path.isfile = lambda _: True
        common.os.listdir = lambda _: files
        test = common.get_files()
        self.assertEqual(test, ["filename", "マルチバイト"])

    def test_execute_rename(self):
        common.os.rename = lambda x, y: (x, y)  # stub
        common.to_abspath = lambda x: x
        sample = [(1, 'a'), (2, 'b')]
        test = common.execute_rename(sample)
        self.assertEqual(test, sample)
