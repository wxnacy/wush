#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

from wush.common import functions
from wush.common import constants

super_function = functions.load_super_function()

def test_random_int():
    res = super_function.random_int(2)
    assert len(res) == 2

def test_get_current_space_name():
    res = super_function.get_current_space_name()
    assert res == constants.DEFAULT_SPACE_NAME

def test_run_shell():
    res, err = functions.run_shell('ls te')
    assert err == b'ls: te: No such file or directory\n'

    res, err = functions.run_shell('ls tests/common/test_functions.py')
    assert res == b'tests/common/test_functions.py\n'
