#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
常量模块
"""

import os
import random

class Constants(object):
    TMPDIR = '/tmp/wush'
    BASETYPE_MAP = {
        'str': str,
        'string': str,
        'int': int,
        'list': list,
        'dict': dict,
        'float': float,
    }
    CONFIG_PATH = os.path.join(os.path.expanduser('~/.wush'), 'config.yml')
    HISTORY_PATH = os.path.expanduser('~/.wush_history')
    SERVER_PORT = '6060'

    @classmethod
    def build_tmpfile(cls, prefix):
        """创建临时文件"""
        return os.path.join(cls.TMPDIR, f'{prefix}.{random.randint(1, 90000)}')

    @classmethod
    def str_to_basetype(cls, text):
        """字符串转为基础类型"""
        if text not in cls.BASETYPE_MAP:
            raise ValueError(f'{text} is not basetype')
        return cls.BASETYPE_MAP[text]

