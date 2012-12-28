#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, division, unicode_literals
import unittest

from mock import patch
from emang import normalize


class TestNormalize(unittest.TestCase):
    files = [
        "spam1",
        "spam2",
        "[author]title.exp",
        "[author]title_2.exp",
        "[作者]タイトル.exp",
        "[作者]タイトル_2.exp"]

    def test_build_filename_tuples(self):
        attrs = {
            "get_files.return_value": self.files,
            "exists.return_value": False}
        with patch("emang.normalize.common", **attrs):
            test = normalize.build_filename_tuples()
            self.assertEqual(test, list(zip(self.files, self.files)))

    def test_main(self):
        filename_tuples = [
            ("[author]title.exp", "author - title.exp"),
            ("[author]title_2.exp", "author - title.exp"),
            ("[作者]タイトル.exp", "作者 - タイトル.exp"),
            ("[作者]タイトル_2.exp", "作者 - タイトル.exp")]
        attrs = {
            "list_up.return_value": filename_tuples,
            "require_confirm.return_value": filename_tuples,
            "execute_rename.return_value": filename_tuples,
            "done.return_value": filename_tuples}
        with patch(
            "emang.normalize.build_filename_tuples",
            return_value=filename_tuples
        ), patch(
            "emang.normalize.common", **attrs
        ):
            test = normalize.main(None)
            self.assertEqual(test, filename_tuples)
