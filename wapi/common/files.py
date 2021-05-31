#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: 371032668@qq.com
"""

"""

import json

class FileUtils:

    @classmethod
    def read_dict(cls, filepath):
        """
        读取字典数据
        :param str filepath: 文件地址
        """
        with open(filepath, 'r') as f:
            lines = f.readlines()
        return json.loads(''.join(lines))
