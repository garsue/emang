#!/usr/bin/env python
#vim: fileencoding=utf-8

import os
from os import path
import re
from functools import partial, wraps
from itertools import compress


def get_matches(files):
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


def check_existence(f):
    @wraps(f)
    def decorated(to_abspath, olds, news):
        existence = [(new, path.exists(to_abspath(new))) for new in news]
        if not any(exists for _, exists in existence):
            return f(to_abspath, olds, news)
        print("Already existed: ")
        [print("\t", new) for new, exists in existence if exists]
    return decorated


def rename_or_not(f):
    @wraps(f)
    def decorated(to_abspath, olds, news):
        if news:
            print("Rename to:")
            [print("\t", old, "->", new) for old, new in zip(olds, news)]
            return f(to_abspath, olds, news)
        print("Nothing to rename.")
    return decorated


def require_confirm(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        ans = input("Do you want to rename? ('yes' or 'no'): ")
        if ans in ["y", "yes"]:
            f(*args, **kwargs)
            return print("Done!")
        print("Canceled by user.")
    return decorated


@check_existence
@rename_or_not
@require_confirm
def execute(to_abspath, olds, news):
    rename = lambda old, new: os.rename(to_abspath(old), to_abspath(new))
    [rename(old, new) for old, new in zip(olds, news)]


if __name__ == "__main__":
    curdir = path.abspath(os.curdir)
    files = next(os.walk(curdir))[2]
    matches = get_matches(files)
    olds = get_old_filenames(files, matches)
    news = compose_new_filenames(matches)
    to_abspath = partial(path.join, curdir)
    execute(to_abspath, olds, news)
