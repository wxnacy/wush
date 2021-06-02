#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import random
import importlib
import sys
import os

from wapi.common import constants
from wapi.common.decorates import env_func_register
from wapi.common.decorates import env_functions

@env_func_register()
def random_int(length, min_int=None, max_int=None):
    """随机 int 值"""
    if min_int is None:
        min_int = 0
    if max_int is None:
        max_int = 9

    if min_int < 0:
        raise ValueError('random_int min_int must >= 0')

    if max_int > 9:
        raise ValueError('random_int max_int must <= 9')

    if min_int >= max_int:
        raise ValueError('random_int max_int must > min_int')

    res = []
    for _ in range(length):
        n = random.randint(min_int, max_int)
        res.append(str(n))
    return ''.join(res)

RANDOM_STR = ()

@env_func_register()
def random_str(length, source=None):
    """随机 int 值"""
    if source is None:
        source = 'a-z,A-Z,0-9,!@#$%^&*()'
    res = []
    #  for _ in range(length):
        #  n = random.randint(0, max_int)
        #  res.append(str(n))
    return ''.join(res)

def load_module(module_name):
    """加载模块"""
    views_module = importlib.import_module(module_name)
    return views_module

@env_func_register()
def get_current_space_name():
    """获取当前 space 名称"""
    return constants.DEFAULT_SPACE_NAME

class Function:
    get_current_space_name = None
    random_int = None
    random_str = None

    def __init__(self):
        for name, func in env_functions.items():
            setattr(self, name, func)

_function = Function()

def get_super_function():
    return _function

super_function = get_super_function()

if __name__ == "__main__":
    print(random_int(5, 4, 9))
    print(random_str(5))
    func = get_super_function()
    print(func.random_int(2))




