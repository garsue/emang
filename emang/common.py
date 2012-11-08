#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
from functools import partial, wraps
import os
from os import path


curdir = path.abspath(os.curdir)
to_abspath = partial(path.join, curdir)


def decode(string):
    if getattr(string, "decode", False):
        return string.decode('utf8')
    return string


def get_files():
    not_dotfile = lambda name: path.isfile(name) and not name.startswith(".")
    return [n for n in map(decode, os.listdir(curdir)) if not_dotfile(n)]


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
    ans = raw_input("Do you want to rename? ('yes' or 'no'): ")
    if ans in ["y", "yes"]:
        return filename_tuples
    print("Canceled by user.")
    return []


def exists_pair(name):
    return name, path.exists(to_abspath(name))


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
        print("Already existed destination file(s): ")
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
