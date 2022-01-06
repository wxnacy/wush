#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
配置模块
"""
import os
import yaml
import copy

from wush.common.config_value import ConfigValue
from wush.common.constants import Constants
from wush.common.loggers import get_logger
from wush.common.utils import load_module
from wush.config.models import ConfigModel
from wush.config.models import EnvModel
from wush.config.function import load_function

__all__ = ['load_config']

class Config(object):
    logger = get_logger('Config')

    _config = None
    _function = None
    module_name = None
    space_name = None
    builtin_env = EnvModel()

    @classmethod
    def read_yml(cls, filepath):
        """读取 yml 文件"""
        with open(filepath, 'r') as f:
            return yaml.safe_load(f)

    @classmethod
    def load(cls, conf_file):
        """通过文件加载"""
        # 去读 yml 文件
        data = cls.read_yml(conf_file) or {}

        # 格式化 modules_include 地址
        config_dir = os.path.dirname(conf_file)
        full_modules_include = []
        for path in data.get("modules_include", []):
            path = os.path.join(config_dir, path)
            full_modules_include.append(path)
        data['modules_include'] = full_modules_include

        ins = cls.loads(data)
        # 获取配置目录
        #  ins._config_dir = os.path.dirname(conf_file)
        return ins

    @classmethod
    def loads(cls, data):
        """通过 dict 数据加载"""
        ins = cls()
        ins._config = ConfigModel(**data)

        # 对模块地址进行解析
        if not ins._config.modules:
            ins._config.modules = []
        for module_path in ins._config.iter_module_path():
            module = cls.read_yml(module_path)
            ins._config.modules.append(module)

        # 格式化模型
        ins._config.format()
        # 加载插件模块
        for module_name in ins._config.function_modules:
            load_module(module_name)

        # 加载方法
        ins._function = load_function()

        for key in ConfigModel.__all__:
            setattr(ins, key, getattr(ins._config, key))

        return ins

    def add_env(self, key, value):
        """添加环境变量"""
        setattr(self._config.env, key, value)

    @property
    def env(self):
        return self._config.env.to_dict()

    @property
    def function(self):
        return self._function

    def get_modules(self):
        """获取模块列表"""
        return self._config.modules

    def get_requests(self, module_name):
        """获取请求列表"""
        return self._config.get_module(module_name).requests

    def get_request(self, module_name, request_name, set_env=True, environs=None):
        """获取请求模型
        :param bool set_env: 是否设置环境变量
        :param dict environs: 编辑变量
        """
        req = self._config.get_module(module_name).get_request(request_name)
        req = copy.deepcopy(req)
        env = self._config.env.to_dict()
        if isinstance(environs, dict):
            env.update(environs)
        self.logger.info('config env {}'.format(env))

        # 将请求模型做环境变量格式化处理并返回
        if set_env:
            req = ConfigValue(req).set_env(**env).set_functions(
                **self.function.get_functions()).format()
        req.format()
        return req

_config = None

def _get_config_path(config_path=None):
    """
    获取配置地址
    """
    if config_path:
        Config.logger.info('配置文件: 用户指定 {}'.format(config_path))
        return config_path
    if os.path.exists(Constants.CONFIG_PATH):
        Config.logger.info('配置文件: 默认 {}'.format(Constants.CONFIG_PATH))
        return Constants.CONFIG_PATH

    config_path = Constants.get_sys_config_path()
    Config.logger.info('配置文件: 系统 {}'.format(config_path))
    return config_path

def load_config(config_path = None):
    """加载配置
    :param str config_path: 配置文件路径

    1、优先使用用户指定配置文件
    2、否则使用默认配置文件路径
    3、否则使用初始化的配置

    """
    global _config
    if not _config:
        config_path = _get_config_path(config_path)
        _config = Config.load(config_path)

    return _config

if __name__ == "__main__":
    config = load_config()
