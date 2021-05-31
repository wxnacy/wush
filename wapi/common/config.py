#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: 371032668@qq.com
"""

"""

import yaml

from enum import Enum

class ConfigName(Enum):
    COOKIE_FILEPATH = 'cookie_filepath'

class Config():
    @classmethod
    def load(cls, filepath):
        item = cls()
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)

        for k, v in data.items():
            setattr(item, k, v)
            print(k, v)

        return item


if __name__ == "__main__":
    config = Config.load('/Users/wenxiaoning/.config/wapi/config.yml')
    print(config.cookie_filepath)


