#!/usr/bin/env python
#vim: fileencoding=utf-8

import unittest
import os
from os import path
import re

import emang


class TestRenamer(unittest.TestCase):
    pattern = re.compile(r"\[(.*)\](.*)\.(.*)")
    files = [
            "spam1",
            "spam2",
            "[author]title.exp",
            "[author]title_2.exp",
            "[作者]タイトル.exp",
            "[作者]タイトル_2.exp",
            ]
    matches = [
            None,
            None,
            re.match(pattern, "[author]title.exp"),
            re.match(pattern, "[author]title_2.exp"),
            re.match(pattern, "[作者]タイトル.exp"),
            re.match(pattern, "[作者]タイトル_2.exp"),
            ]
    olds = [
            "[author]title.exp",
            "[author]title_2.exp",
            "[作者]タイトル.exp",
            "[作者]タイトル_2.exp",
            ]
    news = [
            "author - title.exp",
            "author - title.exp",
            "作者 - タイトル.exp",
            "作者 - タイトル.exp",
            ]

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_get_current_dir(self):
        test = path.abspath(os.curdir)
        expect = path.dirname(path.abspath(__file__))
        self.assertEqual(test, expect)

    def test_get_matche_results(self):
        test = emang.get_matche_results(self.files)
        self.assertIsNone(test[0])
        self.assertIsNone(test[1])
        self.assertEqual(test[2].groups(), ("author", "title", "exp"))
        self.assertEqual(test[3].groups(), ("author", "title_2", "exp"))
        self.assertEqual(test[4].groups(), ("作者", "タイトル", "exp"))
        self.assertEqual(test[5].groups(), ("作者", "タイトル_2", "exp"))

    def test_get_old_filenames(self):
        test = emang.get_old_filenames(self.files, self.matches)
        self.assertEqual(test, self.olds)

    def test_get_filename_parts(self):
        pattern = re.compile(r"\[(.*)\](.*)\.(.*)")
        filename = "[作者]タイトル_2.exp"
        test = emang.get_filename_parts(re.match(pattern, filename))
        expect = "作者", "タイトル", "exp"
        self.assertEqual(test, expect)

    def test_compose_new_filenames(self):
        test = emang.compose_new_filenames(self.matches)
        self.assertEqual(test, self.news)

    def test_execute(self):
        orignal = emang.os.rename
        emang.os.rename = lambda x, y: (x, y)  #stub
        to_abspath_dummy = lambda x: x
        test = emang.execute(to_abspath_dummy, self.olds, self.news)
        expect = [
                ("[author]title.exp", "author - title.exp"),
                ("[author]title_2.exp", "author - title.exp"),
                ("[作者]タイトル.exp", "作者 - タイトル.exp"),
                ("[作者]タイトル_2.exp", "作者 - タイトル.exp"),
                ]
        self.assertEqual(test, expect)
        emang.os.rename = orignal

if __name__ == '__main__':
    unittest.main(verbosity=2)
