#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""

from .decorates import argparser_register
from .enum import Action
from .parse import ArgumentParser

@argparser_register()
class RunArgumentParser(ArgumentParser):
    cmd = 'run'

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--config')
        item.add_argument('--module')
        item.add_argument('--space')
        item.add_argument('--name')
        item.add_argument('--params', action = Action.APPEND.value)
        item.add_argument('--json', action = Action.APPEND.value)
        return item

