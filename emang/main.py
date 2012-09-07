#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import argparse

from . import autorename, manual


def invalid_command():
    return print("No such command")


def dispatch(command):
    commands = {"autorename": autorename.main, "manual": manual.main}
    return commands.get(command, invalid_command)


def main():
    parser = argparse.ArgumentParser(description="Manage E-comic files.")
    parser.add_argument(
        "command", metavar="COMMAND", type=str, help="Subcommand")
    args = parser.parse_args()
    execute_command = dispatch(args.command)
    execute_command()
    return
