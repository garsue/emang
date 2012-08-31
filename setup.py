#!/usr/bin/env python
#vim: fileencoding=utf-8

from setuptools import setup, find_packages


setup(
        name="emang",
        version="1.3",
        packages=find_packages(),
        entry_points={"console_scripts": ["emang = emang.main:main"]},
        test_suite="test",
        )
