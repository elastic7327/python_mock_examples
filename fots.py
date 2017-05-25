#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import urandom


def abc_urandom(length):
    return 'abc' + urandom(length)


def my_random(length):
    return urandom(length)
