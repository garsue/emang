#!/usr/bin/env python
#vim: fileencoding=utf-8

import unittest
import os
from os import path
import re

from emang import autorename


class TestAutoRename(unittest.TestCase):
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

    def test_get_matche_results(self):
        test = autorename.get_matche_results(self.files)
        self.assertIsNone(test[0])
        self.assertIsNone(test[1])
        self.assertEqual(test[2].groups(), ("author", "title", "exp"))
        self.assertEqual(test[3].groups(), ("author", "title_2", "exp"))
        self.assertEqual(test[4].groups(), ("作者", "タイトル", "exp"))
        self.assertEqual(test[5].groups(), ("作者", "タイトル_2", "exp"))

    def test_get_old_filenames(self):
        test = autorename.get_old_filenames(self.files, self.matches)
        self.assertEqual(test, self.olds)

    def test_get_filename_parts(self):
        pattern = re.compile(r"\[(.*)\](.*)\.(.*)")
        filename = "[作者]タイトル_2.exp"
        test = autorename.get_filename_parts(re.match(pattern, filename))
        expect = "作者", "タイトル", "exp"
        self.assertEqual(test, expect)

    def test_compose_new_filenames(self):
        test = autorename.compose_new_filenames(self.matches)
        self.assertEqual(test, self.news)

    def test_execute(self):
        orignal = autorename.os.rename
        autorename.os.rename = lambda x, y: (x, y)  # stub
        to_abspath_dummy = lambda x: x
        test = autorename.execute(to_abspath_dummy)(self.olds, self.news)
        self.assertEqual(test, (self.olds, self.news))
        autorename.os.rename = orignal

if __name__ == '__main__':
    unittest.main(verbosity=2)