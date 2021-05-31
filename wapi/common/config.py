#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: 371032668@qq.com
"""

"""

import yaml

from enum import Enum
from wapi.common import constants

class ConfigName(Enum):
    COOKIE_PATH = 'cookie_path'

class Config():
    env_path = ''
    request_path = ''

    @classmethod
    def load(cls, filepath):
        item = cls()
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)

        for k, v in data.items():
            setattr(item, k, v)
            print(k, v)

        return item

    @classmethod
    def get_config_path(cls):
        return constants.CONFIG_USER_PATH

    def get_env_path(self):
        return self.env_path or constants.ENV_PATH

    def get_request_path(self):
        return self.request_path or constants.REQUEST_PATH

if __name__ == "__main__":
    config = Config.load(Config.get_config_path())
    print(config.cookie_filepath)
