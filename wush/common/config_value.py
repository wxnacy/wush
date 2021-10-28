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

from functools import singledispatch

from wush.common.files import FileUtils
from wush.common.loggers import create_logger

class ConfigValue():
    logger = create_logger('ConfigValue')

    def __init__(self, value):
        self.value = value

        self.REG_ENV = r'(\${.*?})'
        self.REG_PARSE = r'(^\b(json|yml|xml)\b@.*?)'
        self.env = dict(os.environ)
        self.functions = {}

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

        #  self.logger.info('ConfigValue env %s', self.env)

        #  格式化响应格式数据
        for t in (str, list, dict):
            if isinstance(self.value, t):
                func_name = '_format_' + t.__name__
                return getattr(self, func_name)(self.value)
        return self.value

    @singledispatch
    def _format(self, obj):
        self.logger.info('type %s', type(obj))
        return obj

    @_format.register(dict)
    def _(self, value):
        """格式化字典"""
        return self._format_dict(dict)

    @_format.register(list)
    def _(self, lines):
        """格式化数组"""
        self.logger.info('-' * 200)
        return self._format_list(lines)

    @_format.register(str)
    def _(self, text):
        """格式化字符窜"""
        self.logger.info('-' * 200)
        return self._format_str(text)

    def _format_dict(self, value):
        """格式化字典"""
        for v_k, v_v in value.items():
            value[v_k] = ConfigValue(v_v).set_env(**self.env
                    ).set_functions(**self.functions).format()
        return value

    def _format_list(self, lines):
        """格式化数组"""
        for i in range(len(lines)):
            lines[i] = ConfigValue(lines[i]).set_env(**self.env
                    ).set_functions(**self.functions).format()
        return lines

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

        parse_type = self._get_parse_type(text)
        if parse_type:
            text = text[len(parse_type) + 1:]
            if self._is_file(text):
                if parse_type == 'json':
                    return FileUtils.read_dict(text)
            else:
                if parse_type == 'json':
                    return json.loads(text)

        return text

    def _get_parse_type(self, text):
        """获取解析类型"""
        lines = re.findall(self.REG_PARSE, text)
        if not lines:
            return None
        return lines[0][-1]

    def _format_file_content(self, filepath):
        '''格式化文件内容'''
        if filepath.endswith('.json') or filepath.endswith('.yml'):
            return FileUtils.read_dict(filepath)

        with open(filepath, 'r') as f:
            lines = f.readlines()
            if not lines:
                return ''
            if lines[0].startswith('{') and lines[-1].endswith('}'):
                return FileUtils.read_dict(filepath)
            return ''.join(lines)

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

        self.logger.info('environ_names %s', self.environ_names)

        for k in self.environ_names:
            # 处理函数的执行和替换
            orgl = '${' + k + '}'
            if '(' in k and ')' in k:
                k = k.strip(')').strip(' ')
                func_name, args_str = k.split('(')
                func = self.functions.get(func_name)
                self.logger.info('func_name %s %s', func_name, func)

                if not func:
                    continue
                if not args_str:
                    args_str = '()'
                else:
                    args_str = '({},)'.format(args_str)
                args = eval(args_str)
                repl = func(*args)
                repl = str(repl)
                text = text.replace(orgl, repl)
            else:
                text = text.replace(orgl, self.env.get(k) or '')
        return text

