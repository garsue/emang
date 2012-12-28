#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, division, unicode_literals

from . import common
from . import utils


def build_filename_tuples():
    olds = common.get_files()
    filename_tuples = zip(olds, map(utils.normalize, olds))
    return [(old, new) for old, new in filename_tuples
            if not common.exists(new)]


def main(args):
    filename_tuples = build_filename_tuples()
    sequence = [
        common.list_up,
        common.require_confirm,
        common.execute_rename,
        common.done]
    return reduce(lambda acc, f: f(acc), sequence, filename_tuples)
