#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import unittest
import site
import io

from mock import patch
from emang import manual


class TestManual(unittest.TestCase):
    files = [
        "spam1",
        "spam2",
        "[author]title.exp",
        "[作者]タイトル.exp"]

    tempfile_body = """old: spam1
new: spam1

old: spam2
new: spam2

old: [author]title.exp
new: [author]title.exp

old: [作者]タイトル.exp
new: [作者]タイトル.exp"""
    rename_table = """old: spam1
new: spam1

old: spam2
new: spam2

old: [author]title.exp
new: author - title.exp

old: [作者]タイトル.exp
new: 作者 - タイトル.exp"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_build_tempfile_body(self):
        test = manual.build_tempfile_body(self.files)
        self.assertEqual(test, self.tempfile_body)

    def test_to_tuples(self):
        test = manual.to_tuples(self.rename_table)
        expect = [
            ("[author]title.exp", "author - title.exp"),
            ("[作者]タイトル.exp", "作者 - タイトル.exp")]
        self.assertEqual(test, expect)

    def test_to_filename_tuples(self):
        with patch("subprocess.call"):
            test = manual.to_filename_tuples(self.files)
            self.assertEqual(test, [])
        open_name = site.builtins.__name__ + ".open"
        config = {"return_value": io.BytesIO(self.rename_table.encode("utf8"))}
        with patch("subprocess.call"), patch(open_name, **config):
            test = manual.to_filename_tuples(self.files)
            expect = [
                ("[author]title.exp", "author - title.exp"),
                ("[作者]タイトル.exp", "作者 - タイトル.exp")]
            self.assertEqual(test, expect)
