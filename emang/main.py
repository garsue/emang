#!/usr/bin/env python
#vim: fileencoding=utf-8

import argparse

from . import autorename


def invalid_command():
    return print("No such command")


def dispatch(command):
    commands = {"autorename": autorename.main}
    return commands.get(command, invalid_command)


def main():
    parser = argparse.ArgumentParser(description="Manage E-comic files.")
    parser.add_argument("command", metavar="COMMAND", type=str,
            help="Subcommand")
    args = parser.parse_args()
    execute_command = dispatch(args.command)
    execute_command()
    return
