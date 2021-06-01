#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import random
import importlib
import inspect
import sys
import os

from wapi.common.decorates import env_func_register

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

def load_module(path):
    #  dirname = os.path.dirname(path)
    #  print(dirname)
    #  if dirname not in sys.path:
        #  sys.path.append(dirname)
    #  module_name = os.path.basename(path)
    #  print(module_name)
    #  module_name = module_name[0:-3]
    module_name = path
    views_module = importlib.import_module(module_name)
    for name, obj in inspect.getmembers(views_module):
        print(name, obj)
    from wapi.common.decorates import env_functions
    print(env_functions)

if __name__ == "__main__":
    print(random_int(5, 4, 9))
    print(random_str(5))
    print(load_module('/Users/wenxiaoning/Projects/ydwork/apis/functions.py'))



