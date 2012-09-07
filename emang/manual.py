#!/usr/bin/env python
#vim: fileencoding=utf-8

import os
import tempfile
import subprocess
from functools import reduce

from . import common


def build_tempfile_body(files):
    return "\n".join(n + "\t" + n for n in files)


def to_tuples(rename_table):
    tuples = [tuple(ln.split("\t")) for ln in rename_table]
    return [(old, new) for old, new in tuples if old != new]


def to_filename_tuples(files):
    editor = os.environ.get('EDITOR', 'vim')
    tempfile_body = build_tempfile_body(files)
    with tempfile.NamedTemporaryFile() as rename_table_file:
        rename_table_file.write(bytes(tempfile_body, "utf8"))
        rename_table_file.flush()
        subprocess.call([editor, rename_table_file.name])
        with open(rename_table_file.name) as read_only:
            rename_table = [ln.rstrip("\n") for ln in read_only.readlines()]
    return to_tuples(rename_table)


def main():
    files = common.get_files()
    filename_tuples = to_filename_tuples(files)
    sequence = [
            common.list_up,
            common.check_old_existence,
            common.check_new_existence,
            common.require_confirm,
            common.execute_rename,
            common.done,
            ]
    return reduce(lambda acc, f: f(acc), sequence, filename_tuples)
