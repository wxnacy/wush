#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
配置可用的方法模块
"""

import traceback
import os
import hashlib
import json

from rich.console import Console
from rich.table import Table
from wpy.base import BaseFactory
from wpy import randoms

from wush.common.loggers import get_logger

logger = get_logger('function')

__all__ = ['FunctionFactory']

class FunctionFactory(BaseFactory):

    @classmethod
    def get_super_factory(cls):
        factory = cls.get_factory()
        _super_factory = {}
        for key, value in factory.items():
            module = value.__module__
            if module.startswith('wush'):
                _super_factory[key] = value
        return _super_factory

@FunctionFactory.register()
def random_int(length, min_int=None, max_int=None):
    """随机 int 值"""
    return randoms.random_int(length, min_int, max_int)

@FunctionFactory.register()
def random_str(length, source=None):
    """随机 int 值"""
    return randoms.random_str(length, source)

@FunctionFactory.register()
def md5(text):
    """计算 md5 摘要"""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

@FunctionFactory.register()
def get_completion_words(word_for_completion):
    """获取补全的单词列表"""
    return []

@FunctionFactory.register()
def handler_response(response):
    #  print('Response:')
    # 判断是否为 html 结果
    url = response.url
    if response.is_html:
        print('See in browser')
        os.system(f'open -a "/Applications/Google Chrome.app" "{url}"')
        print('')
    try:
        data = response.json()
        data = json.dumps(data, indent=4, ensure_ascii=False)
    except:
        logger.error(traceback.format_exc())
        data = response.content
    print(data)

@FunctionFactory.register()
def print_table(config):
    """打印表格
    :param dict config: 表格数据
        结构如下：
        {
            "headers": [
                { "display": "列名", 'width': '列宽度，非必传' }
            ],
            "items": [
                ('列数据, 长度需要和 headers 长度保持一致')
            ]
        }
    """
    console = Console()
    headers = config.get("headers") or []
    table = Table(show_header=True, show_lines=True,
        header_style="bold magenta")
    for header in headers:
        name = header.pop("display", '未命名')
        table.add_column(name, **header)
    items = config.get("items", [])
    for item in items:
        table.add_row(*item)
    console.print(table)
    after_table = config.get("after_table")
    if after_table:
        console.print(after_table)

class Function(object):
    get_completion_words = None
    random_int = None
    random_str = None
    handler_response = None
    test = None

    _functions = {}

    def __init__(self, functions):
        self._functions = functions
        for name, func in functions.items():
            if isinstance(func, str):
                raise Exception('func {} can not be str'.format(name))
            setattr(self, name, func)

    def add_function(self, func):
        """添加方法"""
        setattr(self, func.__name__, func)
        self._functions[func.__name__] = func

    def get_functions(self):
        """获取方法字段"""
        return self._functions

_super_function = None

def load_super_function():
    """加载 super function"""
    global _super_function
    if not _super_function:
        _super_function = Function(FunctionFactory.get_super_factory())
    return _super_function


_function = None
def load_function():
    """加载全部 function"""
    global _function
    if not _function:
        _function = Function(FunctionFactory.get_factory())
    return _function

if __name__ == "__main__":
    load_super_function()
