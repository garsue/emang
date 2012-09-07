#!/usr/bin/env python
#vim: fileencoding=utf-8

import os
import unittest

import pep8


class TestPEP8(unittest.TestCase):
    def test_pep8(self):
        self.pep8style = pep8.StyleGuide(
            first=True, show_source=True, statistics=True, repeat=True)
        self.pep8style.input_dir(os.curdir)
        report = self.pep8style.check_files()
        report.print_statistics()
        errors = report.get_count('E')
        warnings = report.get_count('W')
        message = '{0} errors / {1} warnings'.format(errors, warnings)
        self.assertEqual(errors, warnings, message)
