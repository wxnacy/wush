#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import yaml
import os

from enum import Enum
from wapi.common import constants
from wapi.common import utils
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
            if k.isupper():
                os.environ[k] = v

    def dict(self):
        data = self.__dict__
        return data

class Config():
    logger = create_logger('Config')

    _root = None
    env_root = ''
    body_root = ''
    module_root = ''
    response_root = ''
    function_modules = []

    function  = None
    _env = Env()

    def __init__(self, ):
        """初始化"""
        self._root = self.get_default_root()
        default_config = self.get_default_config()
        for k, v in default_config.items():
            self._setattr(k, v)

    def _setattr(self, k, v):
        """设置属性"""
        if k == 'response_root':
            v = utils.fmt_path(v)
        elif k == 'env':
            k = '_env'
            v = Env(**v)
        setattr(self, k, v)

    @classmethod
    def load(cls, fileroot):
        """
        加载配置
        :param fileroot: 如果是地址则获取内容，如果是数据则直接加载
        """
        cls.logger.info('Config load path: %s', fileroot)
        item = cls()
        data = {}
        if isinstance(fileroot, dict):
            data = dict(fileroot)
        else:
            item._root = fileroot
            filepath = os.path.join(fileroot, 'wapi.yml')
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)

        if data:
            for k, v in data.items():
                item._setattr(k, v)

        # 格式化各个 root 配置
        for _root in ('env_root', 'module_root', 'body_root'):
            item._setattr(_root, item.fmt_path(getattr(item, _root)))

        item._load_functions()

        # 创建保持地址
        if not os.path.exists(item.response_root):
            os.makedirs(item.response_root)

        return item

    @property
    def env(self):
        """获取 env 信息"""
        return self._env

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

    def get_modules(self):
        """获取模块名称列表"""
        return list(filter(lambda x: not x.startswith('.'), [
            o.replace('.yml', '') for o in os.listdir(self.module_root)]))

    def get_requests(self, module_name):
        """获取请求名称列表"""
        path = self.get_module_path(module_name)
        data = {}
        with open(path, 'r') as f:
            data = yaml.safe_load(f)

        #  return list(filter(lambda x: not x.startswith('.'), [
            #  o.get("name") for o in data.get("requests") or []]))
        return data.get("requests") or []

    def get_function(self):
        return self.function

    @classmethod
    def get_default_root(cls):
        return constants.CONFIG_ROOT

    def fmt_path(self, path):
        if not path:
            return path
        if os.path.isabs(path):
            return path
        return os.path.join(self._root, path)

    @classmethod
    def get_current_body_name(cls, space_name, module_name, request_name):
        """获取当前 body 文件名称"""
        body_name = '{space}_{module}_{request}'.format(
            space = space_name, module=module_name, request = request_name)
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

global_config = Config.load(Config.get_default_root())
