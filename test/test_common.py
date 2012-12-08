#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import unittest
from mock import patch, call

from emang import common


class TestCommon(unittest.TestCase):
    filename_tuples = [
        ("[author]title.exp", "author - title.exp"),
        ("[author]title_2.exp", "author - title.exp"),
        ("[作者]タイトル.exp", "作者 - タイトル.exp"),
        ("[作者]タイトル_2.exp", "作者 - タイトル.exp")]

    def test_decode(self):
        test = common.decode("すぱむ")
        self.assertEqual(test, "すぱむ")
        common.decode("すぱむ".encode("utf8"))
        self.assertEqual(test, "すぱむ")

    def test_get_files(self):
        files = [
            ".hidden".encode("utf8"),
            "filename".encode("utf8"),
            "マルチバイト".encode("utf8")]
        with patch(
                "emang.common.path.isfile", return_value=True
        ), patch(
                "emang.common.os.listdir", return_value=files
        ):
            test = common.get_files()
            self.assertEqual(test, ["filename", "マルチバイト"])

    def  test_fail(self):
        func = lambda tuples: tuples
        func = common.fail(func)
        self.assertEqual(func([]), [])
        self.assertEqual(func([("spam",)]), [("spam",)])

    def test_list_up(self):
        with patch("site.builtins.print") as mock_print:
            test = common.list_up(self.filename_tuples)
            calls = [
                call("Rename to:"),
                call("\t", "[author]title.exp", "->", "author - title.exp"),
                call("\t", "[author]title_2.exp", "->", "author - title.exp"),
                call("\t", "[作者]タイトル.exp", "->", "作者 - タイトル.exp"),
                call("\t", "[作者]タイトル_2.exp", "->", "作者 - タイトル.exp")]
            mock_print.assert_has_calls(calls)
            self.assertEqual(test, self.filename_tuples)
            test = common.list_up([])
            mock_print.assert_called_with("Nothing to rename.")
            self.assertEqual(test, [])

    def test_execute_rename(self):
        with patch(
                "emang.common.to_abspath"
        ) as mock_to_abspath, patch(
                "emang.common.os.rename"
        ) as mock_os_rename:
            test = common.execute_rename(self.filename_tuples)
            calls = [
                call("[author]title.exp"), call("author - title.exp"),
                call("[author]title_2.exp"), call("author - title.exp"),
                call("[作者]タイトル.exp"), call("作者 - タイトル.exp"),
                call("[作者]タイトル_2.exp"), call("作者 - タイトル.exp")]
            mock_to_abspath.assert_has_calls(calls)
            calls = [
                call(
                    mock_to_abspath.return_value, mock_to_abspath.return_value
                ),
                call(
                    mock_to_abspath.return_value, mock_to_abspath.return_value
                )]
            mock_os_rename.assert_has_calls(calls)
            self.assertEqual(test, self.filename_tuples)
