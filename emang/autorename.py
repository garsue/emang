#!/usr/bin/env python
#vim: fileencoding=utf-8

import os
from os import path
import re
from functools import partial, wraps, reduce
from itertools import compress


def get_matche_results(files):
    # group(1): author, group(2): title, group(3): extension
    pattern = re.compile(r"\[(.*)\](.*)\.(.*)")
    return [re.match(pattern, n) for n in files]


def get_old_filenames(files, matches):
    return list(compress(files, matches))


def get_filename_parts(match):
    """Return (author, title, extension)"""
    author, title, extension = match.group(1), match.group(2), match.group(3)
    title = title[:-2] if title.endswith("_2") else title
    return author, title, extension


def compose_new_filenames(matches):
    filename_parts = [get_filename_parts(m) for m in matches if m]
    return ["{0} - {1}.{2}".format(a, t, e) for a, t, e in filename_parts]


def fail(f):
    @wraps(f)
    def decorated(olds, news, *args, **kwargs):
        if (olds, news) == ([], []):
            return [], []
        return f(olds, news, *args, **kwargs)
    return decorated


def list_up(olds, news):
    if news:
        print("Rename to:")
        [print("\t", old, "->", new) for old, new in zip(olds, news)]
        return olds, news
    print("Nothing to rename.")
    return [], []


def check_existence(to_abspath):
    @fail
    def curried(olds, news):
        existence = [(new, path.exists(to_abspath(new))) for new in news]
        if not any(exists for _, exists in existence):
            return olds, news
        print("Already existed: ")
        [print("\t", new) for new, exists in existence if exists]
        return [], []
    return curried


@fail
def require_confirm(olds, news):
    ans = input("Do you want to rename? ('yes' or 'no'): ")
    if ans in ["y", "yes"]:
        return olds, news
    print("Canceled by user.")
    return [], []


def execute(to_abspath):
    @fail
    def curried(olds, news):
        rename = lambda old, new: os.rename(to_abspath(old), to_abspath(new))
        [rename(old, new) for old, new in zip(olds, news)]
        return olds, news
    return curried


@fail
def done(olds, news):
    print("Done!")
    return olds, news


def main():
    curdir = path.abspath(os.curdir)
    files = os.listdir(curdir)
    matches = get_matche_results(files)
    olds = get_old_filenames(files, matches)
    news = compose_new_filenames(matches)
    to_abspath = partial(path.join, curdir)
    sequence = [
            list_up,
            check_existence(to_abspath),
            require_confirm,
            execute(to_abspath),
            done,
            ]
    return reduce(lambda args, f: f(*args), sequence, (olds, news))
