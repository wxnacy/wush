#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

from wapi.common.functions import get_super_function
from wapi.common import constants

super_function = get_super_function()

def test_random_int():
    res = super_function.random_int(2)
    assert len(res), 2

def test_get_current_space_name():
    res = super_function.get_current_space_name()
    assert res, constants.DEFAULT_SPACE_NAME
