#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import os
import json
import yaml

class FileUtils:

    @classmethod
    def read_dict(cls, filepath):
        """
        读取字典数据
        :param str filepath: 文件地址
        """
        with open(filepath, 'r') as f:
            if filepath.endswith('.yml'):
                return yaml.safe_load(f)
            lines = f.readlines()
        return json.loads(''.join(lines))

    @classmethod
    def save_yml(cls, filepath, data):
        """保存成 yml 格式文件"""
        filepath = os.path.expanduser(filepath)
        with open(filepath, 'w') as f:
            yaml.dump(data, f)
