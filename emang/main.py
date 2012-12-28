#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import argparse

from . import autorename, manual, normalize


def get_args(setup_callbacks):
    parser = argparse.ArgumentParser(description="Manage E-comic files.")
    subparsers = parser.add_subparsers(title="subcommands")
    for setup_callback in setup_callbacks:
        setup_callback(subparsers)
    return parser.parse_args()


def main():
    def setup_autorename(subparsers):
        subparser = subparsers.add_parser(
            "autorename",
            description="rename automatically")
        subparser.set_defaults(func=autorename.main)

    def setup_manual(subparsers):
        subparser = subparsers.add_parser(
            "manual",
            description="rename manually with default editor")
        subparser.set_defaults(func=manual.main)

    def setup_normalize(subparsers):
        subparser = subparsers.add_parser(
            "normalize",
            description="normalize filename into NFC unicode")
        subparser.set_defaults(func=normalize.main)

    vars = locals().items()
    setup_callbacks = [v for k, v in vars if k.startswith("setup_")]
    args = get_args(setup_callbacks)
    args.func(args)
    return
