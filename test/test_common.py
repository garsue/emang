#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import unittest
from mock import patch, call

from emang import common


class TestCommon(unittest.TestCase):
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

    def test_execute_rename(self):
        with patch(
                "emang.common.to_abspath"
        ) as mock_to_abspath, patch(
                "emang.common.os.rename"
        ) as mock_os_rename:
            sample = [(1, "a"), (2, "b")]
            test = common.execute_rename(sample)
            calls = [call(1), call("a"), call(2), call("b")]
            mock_to_abspath.assert_has_calls(calls)
            calls = [
                call(
                    mock_to_abspath.return_value, mock_to_abspath.return_value
                ),
                call(
                    mock_to_abspath.return_value, mock_to_abspath.return_value
                )]
            mock_os_rename.assert_has_calls(calls)
            self.assertEqual(test, sample)
