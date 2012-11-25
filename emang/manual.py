#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import os
import tempfile
import subprocess
from functools import reduce

from . import common


def build_tempfile_body(files):
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


def to_filename_tuples(files):
    editor = os.environ.get("EDITOR", "vim")
    tempfile_body = build_tempfile_body(files)
    with tempfile.NamedTemporaryFile() as rename_table_file:
        rename_table_file.write(tempfile_body.encode("utf8"))
        rename_table_file.flush()
        subprocess.call([editor, rename_table_file.name])
        with open(rename_table_file.name) as read_only:
            rename_table = read_only.read()
    not_to_decode = lambda _: rename_table
    return to_tuples(getattr(rename_table, "decode", not_to_decode)("utf8"))


def main():
    files = common.get_files()
    filename_tuples = to_filename_tuples(files)
    sequence = [
        common.list_up,
        common.check_old_existence,
        common.check_new_existence,
        common.require_confirm,
        common.execute_rename,
        common.done]
    return reduce(lambda acc, f: f(acc), sequence, filename_tuples)
