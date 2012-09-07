#!/usr/bin/env python
#vim: fileencoding=utf-8

import unittest

from emang import common


class TestCommon(unittest.TestCase):
    class Original(object):
        pass

    orignal = Original()
    orignal.rename = common.os.rename
    orignal.to_abspath = common.to_abspath

    def setUp(self):
        pass

    def tearDown(self):
        common.os.rename = self.orignal.rename
        common.os.rename = self.orignal.to_abspath

    def test_execute_rename(self):
        common.os.rename = lambda x, y: (x, y)  # stub
        common.to_abspath = lambda x: x
        sample = [(1, 'a'), (2, 'b')]
        test = common.execute_rename(sample)
        self.assertEqual(test, sample)
