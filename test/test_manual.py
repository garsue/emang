#!/usr/bin/env python
#vim: fileencoding=utf-8

import unittest

from emang import manual


class TestManual(unittest.TestCase):
    files = [
        "spam1",
        "spam2",
        "[author]title.exp",
        "[作者]タイトル.exp"]

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_build_tempfile_body(self):
        test = manual.build_tempfile_body(self.files)
        expect = """old: spam1
new: spam1

old: spam2
new: spam2

old: [author]title.exp
new: [author]title.exp

old: [作者]タイトル.exp
new: [作者]タイトル.exp"""
        self.assertEqual(test, expect)

    def test_to_tuples(self):
        rename_table = """old: spam1
new: spam1

old: spam2
new: spam2

old: [author]title.exp
new: author - title.exp

old: [作者]タイトル.exp
new: 作者 - タイトル.exp"""
        test = manual.to_tuples(rename_table)
        expect = [
            ("[author]title.exp", "author - title.exp"),
            ("[作者]タイトル.exp", "作者 - タイトル.exp")]
        self.assertEqual(test, expect)
