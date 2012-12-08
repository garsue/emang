#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import unittest
import itertools
izip_longest = getattr(itertools, "izip_longest", None)
zip_longest = getattr(itertools, "zip_longest", izip_longest)

from mock import patch, call
from emang import main


class TestMain(unittest.TestCase):
    def test_get_args(self):
        with patch("emang.main.argparse") as mock:
            commands = [
                (
                    "autorename",
                    "rename automatically",
                    "autorename_main"),
                (
                    "manual",
                    "rename manually with default editor",
                    "manual_main")]
            main.get_args(commands)
            mock_parser = mock.ArgumentParser
            mock_parser.assert_called_once_with(
                description="Manage E-comic files.")
            mock_add_subparsers = mock_parser.return_value.add_subparsers
            mock_add_subparsers.assert_called_once_with(title="subcommands")
            mock_add_parser = mock_add_subparsers.return_value.add_parser
            calls = [
                call(command_name, description=description)
                for command_name, description, _ in commands]
            mock_add_parser.assert_has_calls(calls, any_order=True)
            calls = [
                call().set_defaults(func=main_function)
                for _, _, main_function in commands]
            mock_add_parser.assert_has_calls(calls, any_order=True)

    def test_main(self):
        expects = [
            ("autorename", "rename automatically", "main"),
            ("manual", "rename manually with default editor", "main")]
        with patch("emang.main.get_args") as mock:
            main.main()
            commands = mock.call_args[0][0]
            for command, expect in zip_longest(commands, expects):
                self.assertEqual(command[0], expect[0])  # command name
                self.assertEqual(command[1], expect[1])  # description
                # function name
                self.assertEqual(command[2].__name__, expect[2])
                mock.return_value.func.assert_called_once_with()
