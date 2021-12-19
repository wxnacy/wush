#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import os
import random

# 默认配置目录
CONFIG_USER_ROOT = 'tests/data/config' # os.path.join(os.getenv("HOME"), '.wapi')
CONFIG_USER_ROOT = os.path.join(os.getenv("HOME"), '.wush')
# 默认配置文件
CONFIG_USER_PATH = os.path.join(CONFIG_USER_ROOT, 'config.yml')

CONFIG_ROOT = CONFIG_USER_ROOT
CONFIG_PATH = os.path.join(CONFIG_ROOT, 'config.yml')
ENV_PATH = os.path.join(CONFIG_ROOT, 'env.yml')
REQUEST_PATH = os.path.join(CONFIG_ROOT, 'request.yml')

DEFAULT_SPACE_NAME = 'default'
DEFAULT_MODULE_NAME = 'default'

#  FUNC_NAME_GET_CURRENT_SPACE_NAME = 'get_current_space_name'

#  DEFAULT_NAME_MODULE_ROOT = 'module_root'

# 默认配置
DEFAULT_CONFIG = {
    'module_root': 'module',
    'env_root': 'env',
    'body_root': 'body',
    'data_root': '~/.wapi/data',
    'function_moduls': []
}

# request 请求方式
METHODS = ('GET', 'OPTIONS', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE')

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

