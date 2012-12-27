#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import re
from functools import reduce
from itertools import compress

from . import common
from . import utils


def get_matche_results(files):
    # group(1): author, group(2): title, group(3): extension
    pattern = re.compile(r"\[(.*)\](.*)\.(.*)")
    return [re.match(pattern, n) for n in files]


def get_old_filenames(files, matches):
    return list(compress(files, matches))


def get_filename_parts(match):
    """Return (author, title, extension)"""
    author, title, extension = match.group(1), match.group(2), match.group(3)
    title = title[:-2] if title.endswith("_", 0, -1) else title
    return author, title, extension


def compose_new_filenames(matches):
    filename_parts = [get_filename_parts(m) for m in matches if m]
    return ["{0} - {1}.{2}".format(a, t, e) for a, t, e in filename_parts]


def build_filename_tuples(args):
    files = common.get_files()
    if args.normalize:
        news = [utils.normalize(f) for f in files]
        return list(zip(files, news))
    matches = get_matche_results(files)
    olds = get_old_filenames(files, matches)
    news = compose_new_filenames(matches)
    return list(zip(olds, news))


def main(args):
    filename_tuples = build_filename_tuples(args)
    sequence = [
        common.list_up,
        common.check_new_existence,
        common.require_confirm,
        common.execute_rename,
        common.done]
    return reduce(lambda acc, f: f(acc), sequence, filename_tuples)
