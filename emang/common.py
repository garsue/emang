#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
from functools import partial, wraps
import os
from os import path
import subprocess
import tempfile
import site

from . import utils


input = getattr(site.builtins, "raw_input", input)
curdir = path.abspath(os.curdir)
to_abspath = partial(path.join, curdir)
exists = lambda filename: path.exists(to_abspath(filename))


def get_files():
    not_dotfile = lambda name: path.isfile(name) and not name.startswith(".")
    return [f for f in map(utils.decode, os.listdir(curdir)) if not_dotfile(f)]


def fail(f):
    @wraps(f)
    def decorated(tuples, *args, **kwargs):
        return f(tuples, *args, **kwargs) if tuples else []
    return decorated


def list_up(filename_tuples):
    if [new for _, new in filename_tuples]:
        print("Rename to:")
        [print("\t", old, "->", new) for old, new in filename_tuples]
        return filename_tuples
    print("Nothing to rename.")
    return []


@fail
def require_confirm(filename_tuples):
    ans = input("Do you want to rename? ('yes' or 'no'): ")
    if ans in ["y", "yes"]:
        return filename_tuples
    print("Canceled by user.")
    return []


def exists_pair(filename):
    return filename, exists(filename)


@fail
def check_old_existence(filename_tuples):
    old_existence = [exists_pair(old) for old, _ in filename_tuples]
    if all(exists for _, exists in old_existence):
        return filename_tuples
    print("Not existing source file(s):")
    [print("\t", old) for old, exists in old_existence if not exists]
    return []


@fail
def check_new_existence(filename_tuples):
    new_existence = [exists_pair(new) for _, new in filename_tuples]
    if any(exists for _, exists in new_existence):
        print("Already existed destination file(s):")
        [print("\t", new) for new, exists in new_existence if exists]
        return []
    return filename_tuples


@fail
def execute_rename(filename_tuples):
    rename = lambda old, new: os.rename(to_abspath(old), to_abspath(new))
    [rename(old, new) for old, new in filename_tuples]
    return filename_tuples


@fail
def done(tuples):
    print("Done!")
    return tuples


def call_editor(filename):
    editor = os.environ.get("EDITOR", "vim")
    subprocess.call([editor, filename])
    return


def read_file(filename):
    with open(filename) as f:
        return f.read()


def edit_rename_table(rename_table_body):
    with tempfile.NamedTemporaryFile() as rename_table_file:
        rename_table_file.write(rename_table_body.encode("utf8"))
        rename_table_file.flush()
        call_editor(rename_table_file.name)
        rename_table = read_file(rename_table_file.name)
    return utils.decode(rename_table)
