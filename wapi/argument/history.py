#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""

from .decorates import argparser_register
from .parse import ArgumentParser

@argparser_register()
class HistoryArgumentParser(ArgumentParser):
    cmd = 'history'

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        return item

