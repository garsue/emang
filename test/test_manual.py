#!/usr/bin/env python
#vim: fileencoding=utf-8

import unittest

from emang import manual


class TestManual(unittest.TestCase):
    files = [
            "spam1",
            "spam2",
            "[author]title.exp",
            "[作者]タイトル.exp",
            ]

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_build_tempfile_body(self):
        test = manual.build_tempfile_body(self.files)
        expect = """spam1\tspam1
spam2\tspam2
[author]title.exp\t[author]title.exp
[作者]タイトル.exp\t[作者]タイトル.exp"""
        self.assertEqual(test, expect)

    def test_to_tuples(self):
        rename_list = [
                "spam1\tspam1",
                "spam2\tspam2",
                "[author]title.exp\tauthor - title.exp",
                "[作者]タイトル.exp\t作者 - タイトル.exp",
                ]
        test = manual.to_tuples(rename_list)
        expect = [
                ("[author]title.exp", "author - title.exp"),
                ("[作者]タイトル.exp", "作者 - タイトル.exp"),
                ]
        self.assertEqual(test, expect)


if __name__ == '__main__':
    unittest.main(verbosity=2)
