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

from functools import reduce


def xor(lhs: int, rhs: int) -> int:
    """XOR two numbers, designated for use within a call to
    :py:func:`~functools.reduce`"""
    return lhs ^ rhs


def fromstr(string: str) -> int:
    """converts a string to integer, designated for use within a call
    to :py:func:`sys.exit` or :py:exc:`SystemExit`"""
    if not isinstance(string, str):
        raise TypeError(
            f"{fromstr} takes a `str' as argument but got `{type(string).__name__}' instead"
        )

    return reduce(xor, list(map(ord, string))) or int(chr(53))


class Exit(SystemExit):
    """Shorthand to ``SystemExit(fromstr(y))``"""

    def __init__(self, string: str):
        super().__init__(fromstr(string))


__all__ = ['Exit', 'xor', 'fromstr']
