#!/usr/bin/env python
#vim: fileencoding=utf-8

from __future__ import print_function, division, unicode_literals
import site


input = getattr(site.builtins, "raw_input", input)


def decode(string):
    attrs = dir(string)
    isdecodable = "decode" in attrs
    isencodable = "encode" in attrs
    isstr = isinstance(string, str)
    if isdecodable and (isencodable is isstr):
        return string.decode("utf8")
    return string
