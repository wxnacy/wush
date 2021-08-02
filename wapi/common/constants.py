#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import os

CONFIG_USER_ROOT = os.path.join(os.getenv("HOME"), '.wapi')
CONFIG_USER_PATH = os.path.join(CONFIG_USER_ROOT, 'wapi.yml')

CONFIG_ROOT = CONFIG_USER_ROOT
CONFIG_PATH = os.path.join(CONFIG_ROOT, 'wapi.yml')
ENV_PATH = os.path.join(CONFIG_ROOT, 'env.yml')
REQUEST_PATH = os.path.join(CONFIG_ROOT, 'request.yml')

DEFAULT_SPACE_NAME = 'default'
DEFAULT_MODULE_NAME = 'default'

FUNC_NAME_GET_CURRENT_SPACE_NAME = 'get_current_space_name'

DEFAULT_NAME_MODULE_ROOT = 'module_root'

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

# 参数集合
#  COMMAND_RUN_ARGS = ('config', 'module', 'name', 'space')
#  COMMAND_CONFIG_ARGS = ('root', 'module', 'space')
# 命令集合
#  COMMANDS = ('config', 'run', 'body', 'env', 'module', 'history')
#  COMMAND_CONFIG = 'config'
#  COMMAND_ENV = 'env'
#  COMMAND_RUN = 'run'

#  COMMAND_CMD_ARGS = {
    #  COMMAND_RUN: COMMAND_RUN_ARGS,
    #  COMMAND_CONFIG: COMMAND_CONFIG_ARGS,
#  }
