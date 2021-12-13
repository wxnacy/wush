#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
配置模块
"""
import yaml

from wush.config.models import ConfigModel

class Config(object):
    _config = None

    @classmethod
    def load(cls, conf_file):
        """通过文件加载"""
        with open(conf_file, 'r') as f:
            data = yaml.safe_load(f)
        ins = cls()
        ins._config = ConfigModel(**data)
        return ins

if __name__ == "__main__":
    filepath = 'tests/data/config/config.yml'
    config = Config.load(filepath)
    with open('tests/data/config/config.yml', 'r') as f:
        data = yaml.safe_load(f)
    config = ConfigModel(**data)
    import json
    print(json.dumps(config.to_dict(), indent=4))

