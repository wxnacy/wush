#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import os
import random

# 默认配置目录
CONFIG_USER_ROOT = 'tests/data/config' # os.path.join(os.getenv("HOME"), '.wapi')
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

    @classmethod
    def build_tmpfile(cls, prefix):
        """创建临时文件"""
        return os.path.join(cls.TMPDIR, f'{prefix}.{random.randint(1, 90000)}')

