#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import argparse

from . import autorename, manual


def get_args(commands):
    parser = argparse.ArgumentParser(description="Manage E-comic files.")
    subparsers = parser.add_subparsers(title="subcommands")
    for command_name, description, main_function in commands:
        subparser = subparsers.add_parser(
            command_name, description=description)
        subparser.set_defaults(func=main_function)
    return parser.parse_args()


def main():
    commands = [
        ("autorename", "rename automatically", autorename.main),
        ("manual", "rename manually with default editor", manual.main)]
    args = get_args(commands)
    args.func()
    return
