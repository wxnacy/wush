#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

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
