#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import random
import hashlib
import importlib
import sys
import os
import subprocess

from wpy.base import BaseFactory
from wpy.tools import randoms

from wapi.common import constants

class FunctionFactory(BaseFactory):
    pass

@FunctionFactory.register()
def random_int(length, min_int=None, max_int=None):
    """随机 int 值"""
    return randoms.random_int(length, min_int, max_int)

RANDOM_STR = ()

@FunctionFactory.register()
def random_str(length, source=None):
    """随机 int 值"""
    return randoms.random_str(length, source)

@FunctionFactory.register()
def md5(text):
    """计算 md5 摘要"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

@FunctionFactory.register()
def get_current_space_name():
    """获取当前 space 名称"""
    return constants.DEFAULT_SPACE_NAME

@FunctionFactory.register()
def get_completion_words(word_for_completion):
    """获取补全的单词列表"""
    return []

@FunctionFactory.register()
def request(wapi, module_name, request_name):
    return wapi.request(request_name = request_name, module_name = module_name)

@FunctionFactory.register()
def get_current_web_port():
    return os.getenv('WUSH_WEB_PORT')

def run_shell(command):
    """运行 shell 语句"""
    res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
        stderr = subprocess.PIPE)
    return res.communicate()

def load_module(module_name):
    """加载模块"""
    views_module = importlib.import_module(module_name)
    return views_module

class Function:
    get_current_space_name = None
    get_completion_words = None
    random_int = None
    random_str = None
    get_current_web_port = None
    test = None

    _functions = {}

    def __init__(self, functions):
        self._functions = functions
        for name, func in functions.items():
            if isinstance(func, str):
                raise Exception('func {} can not be str'.format(name))
            setattr(self, name, func)

    def add_function(self, func):
        setattr(self, func.__name__, func)
        self._functions[func.__name__] = func

    def get_functions(self):
        return self._functions

_function = Function(FunctionFactory.get_factory())

def get_super_function():
    return _function

super_function = get_super_function()

if __name__ == "__main__":
    print(random_int(5, 4, 9))
    print(random_str(5))
    func = get_super_function()
    print(func.random_int(2))
