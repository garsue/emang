#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, unicode_literals
import unittest
import itertools
izip_longest = getattr(itertools, "izip_longest", None)
zip_longest = getattr(itertools, "zip_longest", izip_longest)

from mock import patch, call, Mock
from emang import main


class TestMain(unittest.TestCase):
    def test_get_args(self):
        with patch("emang.main.argparse") as mock:
            setup_callback = Mock()
            setup_callbacks = [setup_callback]
            test = main.get_args(setup_callbacks)
            parser = mock.ArgumentParser
            parser.assert_called_once_with(description="Manage E-comic files.")
            add_subparsers = parser.return_value.add_subparsers
            add_subparsers.assert_called_once_with(title="subcommands")
            subparsers = add_subparsers.return_value
            setup_callback.assert_called_with(subparsers)
            self.assertEqual(test, parser.return_value.parse_args.return_value)

    def test_main(self):
        with patch(
                "emang.main.get_args"
        ) as get_args, patch(
            "emang.main.autorename.main"
        ) as autorename_main, patch(
            "emang.main.manual.main"
        ) as manual_main:
            main.main()
            setup_callbacks = get_args.call_args[0][0]
            subparsers = Mock()
            for setup_callback in setup_callbacks:
                setup_callback(subparsers)
            add_parser = subparsers.add_parser
            calls = [
                call(
                    "autorename",
                    description="rename automatically"),
                call(
                    "manual",
                    description="rename manually with default editor"),
                call(
                    "normalize",
                    description="normalize filename into NFC unicode")]
            add_parser.assert_has_calls(calls, any_order=True)
            add_argument = add_parser.return_value.add_argument
            calls = [
                # test argument
                # call(
                #     "-n", "--normalize", action="store_true", default=False,
                #     help="normalize filename into NFC unicode")
            ]
            add_argument.assert_has_calls(calls, any_order=True)
            set_defaults = add_parser.return_value.set_defaults
            calls = [call(func=autorename_main), call(func=manual_main)]
            set_defaults.assert_has_calls(calls, any_order=True)
            args = get_args.return_value
            args.func.assert_called_once_with(args)
