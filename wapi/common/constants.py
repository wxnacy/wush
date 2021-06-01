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
ENV_PATH_FMT = os.path.join(CONFIG_ROOT, 'env-{}.yml')
REQUEST_PATH = os.path.join(CONFIG_ROOT, 'request.yml')
REQUEST_PATH_FMT = os.path.join(CONFIG_ROOT, 'request-{}.yml')
