#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import unittest
import re

from mock import patch
from emang import autorename


class TestAutoRename(unittest.TestCase):
    pattern = re.compile(r"\[(.*)\] *(.*)\.(.*)")
    files = [
        "spam1",
        "spam2",
        "[author]title.exp",
        "[author]title_2.exp",
        "[作者]タイトル.exp",
        "[作者]タイトル_2.exp",
        "[作者] タイトル_3.exp"]
    matches = [
        None,
        None,
        re.match(pattern, "[author]title.exp"),
        re.match(pattern, "[author]title_2.exp"),
        re.match(pattern, "[作者]タイトル.exp"),
        re.match(pattern, "[作者]タイトル_2.exp"),
        re.match(pattern, "[作者] タイトル_3.exp")]
    olds = [
        "[author]title.exp",
        "[author]title_2.exp",
        "[作者]タイトル.exp",
        "[作者]タイトル_2.exp",
        "[作者] タイトル_3.exp"]
    news = [
        "author - title.exp",
        "author - title.exp",
        "作者 - タイトル.exp",
        "作者 - タイトル.exp",
        "作者 - タイトル.exp"]
    filename_tuples = [
        ("[author]title.exp", "author - title.exp"),
        ("[author]title_2.exp", "author - title.exp"),
        ("[作者]タイトル.exp", "作者 - タイトル.exp"),
        ("[作者]タイトル_2.exp", "作者 - タイトル.exp"),
        ("[作者] タイトル_3.exp", "作者 - タイトル.exp")]

    def test_get_matche_results(self):
        test = autorename.get_matche_results(self.files)
        self.assertIsNone(test[0])
        self.assertIsNone(test[1])
        self.assertEqual(test[2].groups(), ("author", "title", "exp"))
        self.assertEqual(test[3].groups(), ("author", "title_2", "exp"))
        self.assertEqual(test[4].groups(), ("作者", "タイトル", "exp"))
        self.assertEqual(test[5].groups(), ("作者", "タイトル_2", "exp"))
        self.assertEqual(test[6].groups(), ("作者", "タイトル_3", "exp"))

    def test_get_old_filenames(self):
        test = autorename.get_old_filenames(self.files, self.matches)
        self.assertEqual(test, self.olds)

    def test_get_filename_parts(self):
        filename = "[作者]  タイトル_3.exp"
        test = autorename.get_filename_parts(re.match(self.pattern, filename))
        expect = "作者", "タイトル", "exp"
        self.assertEqual(test, expect)

    def test_compose_new_filenames(self):
        test = autorename.compose_new_filenames(self.matches)
        self.assertEqual(test, self.news)

    def test_build_filename_tuples(self):
        attrs = {
            "get_matche_results.return_value": False,
            "get_old_filenames.return_value": self.files,
            "compose_new_filenames.return_value": self.files}
        with patch(
            "emang.autorename.common.get_files",
            return_value=self.files
        ), patch(
            "emang.autorename",
            **attrs
        ):
            test = autorename.build_filename_tuples()
            self.assertEqual(test, self.filename_tuples)

    def test_main(self):
        attrs = {
            "list_up.return_value": self.filename_tuples,
            "check_new_existence.return_value": self.filename_tuples,
            "require_confirm.return_value": self.filename_tuples,
            "execute_rename.return_value": self.filename_tuples,
            "done.return_value": self.filename_tuples}
        with patch(
            "emang.autorename.build_filename_tuples",
            return_value=self.filename_tuples
        ), patch(
            "emang.autorename.common", **attrs
        ):
            test = autorename.main(None)
            self.assertEqual(test, self.filename_tuples)
