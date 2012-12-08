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

    def test_require_confirm(self):
        with patch(
            "emang.common.input", return_value="yes"
        ) as mock_raw_input:
            test = common.require_confirm(self.filename_tuples)
            mock_raw_input.assert_called_with(
                "Do you want to rename? ('yes' or 'no'): ")
            self.assertEqual(test, self.filename_tuples)
        with patch(
            "emang.common.input",
        ) as mock_raw_input, patch(
            "site.builtins.print"
        ) as mock_print:
            test = common.require_confirm(self.filename_tuples)
            mock_raw_input.assert_called_with(
                "Do you want to rename? ('yes' or 'no'): ")
            mock_print.assert_called_with("Canceled by user.")
            self.assertEqual(test, [])

    def test_exists_pair(self):
        name = "spam"
        with patch(
            "emang.common.to_abspath"
        ) as mock_to_abspath, patch(
            "emang.common.path.exists"
        ) as mock_exists:
            test = common.exists_pair(name)
            mock_to_abspath.assert_called_with(name)
            mock_exists.assert_called_with(mock_to_abspath.return_value)
            self.assertEqual(test, ("spam", mock_exists.return_value))

    def test_check_old_existence(self):
        side_effect = [(old, True) for old, _ in self.filename_tuples]
        with patch("emang.common.exists_pair", side_effect=side_effect):
            test = common.check_old_existence(self.filename_tuples)
            self.assertEqual(test, self.filename_tuples)
        side_effect[0] = (self.filename_tuples[0][0], False)
        side_effect[-1] = (self.filename_tuples[-1][0], False)
        with patch(
            "emang.common.exists_pair", side_effect=side_effect
        ), patch(
            "site.builtins.print"
        ) as mock_print:
            test = common.check_old_existence(self.filename_tuples)
            calls = [
                call("Not existing source file(s):"),
                call("\t", self.filename_tuples[0][0]),
                call("\t", self.filename_tuples[-1][0])]
            mock_print.assert_has_calls(calls)
            self.assertEqual(test, [])

    def test_check_new_existence(self):
        side_effect = [(new, False) for _, new in self.filename_tuples]
        with patch("emang.common.exists_pair", side_effect=side_effect):
            test = common.check_new_existence(self.filename_tuples)
            self.assertEqual(test, self.filename_tuples)
        side_effect[0] = (self.filename_tuples[0][0], True)
        side_effect[-1] = (self.filename_tuples[-1][0], True)
        with patch(
            "emang.common.exists_pair", side_effect=side_effect
        ), patch(
            "site.builtins.print"
        ) as mock_print:
            test = common.check_new_existence(self.filename_tuples)
            calls = [
                call("Already existed destination file(s):"),
                call("\t", self.filename_tuples[0][0]),
                call("\t", self.filename_tuples[-1][0])]
            mock_print.assert_has_calls(calls)
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

    def test_done(self):
        with patch("site.builtins.print") as mock_print:
            test = common.done(self.filename_tuples)
            mock_print.assert_called_once_with("Done!")
            self.assertEqual(test, self.filename_tuples)
