#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import yaml
import os

from enum import Enum
from wapi.common import constants

class ConfigName(Enum):
    COOKIE_PATH = 'cookie_path'

class Config():
    env_path = ''
    env_root = ''
    request_path = ''
    request_root = ''
    request_dict = {}
    env_dict = {}

    @classmethod
    def load(cls, filepath):
        item = cls()
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)

        if data:
            for k, v in data.items():
                setattr(item, k, v)

        # 设置 request 集合
        item.request_root = cls.fmt_path(item.request_root)
        if os.path.exists(item.request_root):
            for dirname, _, filenames in os.walk(item.request_root):
                for filename in filenames:
                    if not filename.endswith('.yml'):
                        continue
                    module_name = filename.replace('.yml', '')
                    item.request_dict[module_name] = os.path.join(dirname, filename)
        item.request_dict['default'] = constants.REQUEST_PATH

        # 设置 env 集合
        item.env_root = cls.fmt_path(item.env_root)
        if os.path.exists(item.env_root):
            for dirname, _, filenames in os.walk(item.env_root):
                for filename in filenames:
                    if not filename.endswith('.yml'):
                        continue
                    module_name = filename.replace('.yml', '')
                    item.env_dict[module_name] = os.path.join(dirname, filename)
        item.env_dict['default'] = constants.ENV_PATH

        return item

    @classmethod
    def fmt_path(cls, path):
        if not path:
            return path
        if os.path.isabs(path):
            return path
        return os.path.join(constants.CONFIG_ROOT, path)

    @classmethod
    def get_config_path(cls):
        return constants.CONFIG_PATH

    def get_env_path(self, space_name=None):
        if not space_name:
            space_name = 'default'
        return self.env_dict.get(space_name)

    def get_request_path(self, module_name=None):
        if not module_name:
            module_name = 'default'
        return self.request_dict.get(module_name)

#  config = Config.load(Config.get_config_path())

if __name__ == "__main__":
    config = Config.load(Config.get_config_path())
    print(config.cookie_filepath)
