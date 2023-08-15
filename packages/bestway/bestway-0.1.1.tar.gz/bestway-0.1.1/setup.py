#!/usr/bin/env python
# -*- coding: utf-8 -*-
# <bestway - The best way to craft exit codes>
# Copyright (C) <2023>  Ð4√¡η¢Ч <d4v1ncy@protonmail.ch>
# This is free and unencumbered software released into the public domain.

# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.

# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

# For more information, please refer to <https://unlicense.org>
from os.path import join, dirname, abspath
from setuptools import setup, find_packages


def read_readme():
    with open(join(abspath(dirname(__file__)), 'README.rst')) as fd:
        return fd.read()


if __name__ == "__main__":
    setup(
        name="bestway",
        version='0.1.1',
        description=__doc__,
        long_description=read_readme(),
        url="http://github.com/d4v1ncy/bestway",
        author="Ð4√¡η¢Ч",
        author_email="d4v1ncy@protonmail.ch",
        include_package_data=True,
        packages=find_packages(exclude=["*test*"]),
        long_description_content_type='text/x-rst',
        classifiers=[
            "Development Status :: 1 - Planning",
            "License :: OSI Approved :: The Unlicense (Unlicense)",
            "Operating System :: POSIX",
            "Programming Language :: Python :: 3",
        ],
    )
