#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import json
import os
import re
import subprocess
import yaml
import random

from common.loggers import create_logger

class ConfigValue():
    logger = create_logger('ConfigValue')

    def __init__(self, value):
        self.value = value

        self.REG_ENV = r'(\${.*?})'
        self.env = dict(os.environ)
        self.functions = {'random': random.random}

    def set_env(self, **data):
        self.env.update(data)
        return self

    def set_functions(self, **data):
        self.functions.update(data)
        return self

    def format(self):
        '''输出格式化信息'''

        if not self.value:
            # 为空，返回
            return self.value

        # 格式化响应格式数据
        for t in (str,):
            if isinstance(self.value, t):
                func_name = '_format_' + t.__name__
                return getattr(self, func_name)(self.value)

        return self.value

    def _format_str(self, text):
        '''格式化字符串'''
        if self._has_environs(text):
            text = self._format_environ(text)
        if text.startswith('@'):
            text = text[1:]
            self.logger.debug(text)
            if text.startswith('{') and text.endswith('}'):
                return json.loads(text)
            if text.startswith('[') and text.endswith(']'):
                return json.loads(text)

            if not self._is_file(text):
                raise ValueError(u'{} 文件路径不存在'.format(text))

            return self._format_file_content(text)

        return text

    def _format_file_content(self, filepath):
        '''格式化文件内容'''
        with open(filepath, 'r') as f:
            if filepath.endswith(".json"):
                lines = f.readlines()
                return json.loads(''.join(lines))
            if filepath.endswith(".yml"):
                return yaml.load(f)

    def _is_file(self, filepath):
        '''是否为文件'''
        return os.path.exists(filepath)

    def _has_environs(self, text):
        '''是否有环境变量'''
        if not isinstance(text, str):
            return False
        lines = re.findall(self.REG_ENV, text)
        self.environ_names = [o[2:-1] for o in lines]
        return True if self.environ_names else False

    def _format_environ(self, text):
        '''格式化环境变量'''
        if not self.environ_names:
            return text

        for k in self.environ_names:
            print(k)
            orgl = '${' + k + '}'
            if k.endswith('()'):
                func_name = self.functions.get(k.strip('()'))
                repl = func_name() if func_name else ''
                repl = str(repl)
                text = text.replace(orgl, repl)
            else:
                text = text.replace(orgl, self.env.get(k) or '')
        return text

