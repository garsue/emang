#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import unittest

from mock import patch
from emang import manual


class TestManual(unittest.TestCase):
    files = [
        "spam1",
        "spam2",
        "[author]title.exp",
        "[作者]タイトル.exp"]

    rename_table_body = """old: spam1
new: spam1

old: spam2
new: spam2

old: [author]title.exp
new: [author]title.exp

old: [作者]タイトル.exp
new: [作者]タイトル.exp"""
    edited_rename_table = """old: spam1
new: spam1

old: spam2
new: spam2

old: [author]title.exp
new: author - title.exp

old: [作者]タイトル.exp
new: 作者 - タイトル.exp"""

    def test_build_rename_table_body(self):
        test = manual.build_rename_table_body(self.files)
        self.assertEqual(test, self.rename_table_body)

    def test_to_tuples(self):
        test = manual.to_tuples(self.edited_rename_table)
        expect = [
            ("[author]title.exp", "author - title.exp"),
            ("[作者]タイトル.exp", "作者 - タイトル.exp")]
        self.assertEqual(test, expect)

    def test_main(self):
        filename_tuples = [
            ("[author]title.exp", "author - title.exp"),
            ("[作者]タイトル.exp", "作者 - タイトル.exp")]
        attrs = {
            "get_files.return_value": self.files,
            "edited_content.return_value": self.edited_rename_table,
            "list_up.return_value": filename_tuples,
            "check_old_existence.return_value": filename_tuples,
            "check_new_existence.return_value": filename_tuples,
            "require_confirm.return_value": filename_tuples,
            "execute_rename.return_value": filename_tuples,
            "done.return_value": filename_tuples}
        with patch("emang.manual.common", **attrs):
            test = manual.main(None)
            self.assertEqual(test, filename_tuples)
