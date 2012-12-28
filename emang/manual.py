#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
from functools import reduce

from . import common


def build_rename_table_body(files):
    template = "old: {0}\nnew: {1}"
    return "\n\n".join(template.format(n, n) for n in files)


def to_pair(block):
    old, new = tuple(block.split("\n")[:2])
    old = old.replace("old: ", "", 1).rstrip("\n")
    new = new.replace("new: ", "", 1).rstrip("\n")
    return old, new


def to_tuples(rename_table):
    tuples = [to_pair(block) for block in rename_table.split("\n\n")]
    return [(old, new) for old, new in tuples if old != new]


def main(_):
    files = common.get_files()
    rename_table_body = build_rename_table_body(files)
    edited_rename_table = common.edit_rename_table(rename_table_body)
    filename_tuples = to_tuples(edited_rename_table)
    sequence = [
        common.list_up,
        common.check_old_existence,
        common.check_new_existence,
        common.require_confirm,
        common.execute_rename,
        common.done]
    return reduce(lambda acc, f: f(acc), sequence, filename_tuples)
