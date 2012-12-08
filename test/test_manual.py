#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import unittest
import io

from mock import patch, Mock
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
        with patch("emang.manual.os.environ.get", return_value="some_editor"):
            mock_rename_table_file = Mock()
            with patch(
                "emang.manual.tempfile.NamedTemporaryFile",
                **{("return_value."
                    "__enter__."
                    "return_value"): mock_rename_table_file}
            ), patch(
                "emang.manual.subprocess.call"
            ) as mock_subprocess_call, patch(
                "site.builtins.open",
                return_value=io.BytesIO(self.rename_table.encode("utf8"))
            ) as mock_open:
                test = manual.to_filename_tuples(self.files)
                mock_rename_table_file.write.assert_called_with(
                    self.tempfile_body.encode("utf8"))
                mock_rename_table_file.flush.assert_called_with()
                mock_subprocess_call.assert_called_with(
                    ["some_editor", mock_rename_table_file.name])
                mock_open.assert_called_with(mock_rename_table_file.name)
                expect = [
                    ("[author]title.exp", "author - title.exp"),
                    ("[作者]タイトル.exp", "作者 - タイトル.exp")]
                self.assertEqual(test, expect)
