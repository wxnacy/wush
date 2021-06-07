#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import yaml
import os

from enum import Enum
from wapi.common import constants
from wapi.common.functions import load_module
from wapi.common.functions import super_function
from wapi.common.functions import Function
from wapi.common.loggers import create_logger
from wapi.common.decorates import env_functions

class Env():
    # 参数地址
    body_path = ''

    def __init__(self, **kw):
        self.add(**kw)

    def add(self, **kw):
        """添加环境变量"""
        for k, v in kw.items():
            setattr(self, k, v)

    def dict(self):
        data = self.__dict__
        return data

class Config():
    logger = create_logger('Config')

    env_root = ''
    body_root = ''
    module_root = ''
    function_modules = []

    function  = None
    _env = Env()

    @classmethod
    def load(cls, filepath):
        cls.logger.info('Config load path: %s', filepath)
        item = cls()
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)

        if data:
            for k, v in data.items():
                setattr(item, k, v)

        # 格式化各个 root 配置
        for _root in ('env_root', 'module_root', 'body_root'):
            setattr(item, _root, cls.fmt_path(getattr(item, _root)))

        item._load_functions()
        return item

    def _load_functions(self):
        """加载方法"""
        self.logger.info('Config functions %s', self.function_modules)
        for module_name in self.function_modules:
            load_module(module_name)

        f = Function()
        self.function = f

    def get_env(self):
        """获取 env 信息"""
        return self._env

    def get_env_path(self, space_name=None):
        """获取 env 配置地址"""
        if not space_name:
            space_name = super_function.get_current_space_name()
        return os.path.join(self.env_root, '{}.yml'.format(space_name))

    def get_module_path(self, module_name=None):
        """获取 request 配置地址"""
        if not module_name:
            module_name = self.get_default_module_name()
        return os.path.join(self.module_root, '{}.yml'.format(module_name))

    def get_body_path(self, body_name):
        """获取 body 配置地址"""
        return os.path.join(self.body_root, body_name)

    def get_function(self):
        return self.function

    @classmethod
    def get_config_path(cls):
        return constants.CONFIG_PATH

    @classmethod
    def get_config_root(cls):
        return constants.CONFIG_PATH

    @classmethod
    def fmt_path(cls, path):
        if not path:
            return path
        if os.path.isabs(path):
            return path
        return os.path.join(constants.CONFIG_ROOT, path)

    @classmethod
    def get_current_body_name(cls, space_name, module_name, request_name):
        """获取当前 body 文件名称"""
        body_name = '{}_{}_{}'.format(space_name, module_name, request_name)
        return body_name

    @classmethod
    def get_current_env_name(self, space_name):
        """获取当前 env 文件名称"""
        return space_name

    @classmethod
    def get_default_module_name(cls):
        """获取默认 module 名称"""
        return constants.DEFAULT_MODULE_NAME

    @classmethod
    def get_default_config(cls):
        """获取默认配置"""
        return constants.DEFAULT_CONFIG

global_config = Config.load(Config.get_config_path())
