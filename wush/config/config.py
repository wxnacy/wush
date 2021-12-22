#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
配置模块
"""
import os
import yaml

from wush.config.models import ConfigModel
from wush.config.models import EnvModel
from wush.common.config_value import ConfigValue
from wush.common.constants import Constants
from wush.config.function import load_super_function
from wush.common.loggers import get_logger

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
        for module_path in ins._config.iter_module_path():
            module = cls.read_yml(module_path)
            ins._config.modules.append(module)

        # 格式化模型
        ins._config.format()

        # 加载方法
        ins._function = load_super_function()

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

    def get_request(self, module_name, request_name):
        """获取请求模型"""
        req = self._config.get_module(module_name).get_request(request_name)
        env = self._config.env.to_dict()
        self.logger.info('config env {}'.format(env))

        # 将请求模型做环境变量格式化处理并返回
        req = ConfigValue(req).set_env(**env).format()
        req.format()
        return req

_config = None

def load_config(config_path = None):
    """加载配置
    :param str config_path: 配置文件路径

    1、优先使用用户指定配置文件
    2、否则使用默认配置文件路径
    3、否则使用初始化的配置

    """
    global _config
    if not _config:
        if config_path:
            _config = Config.load(config_path)
        else:
            if os.path.exists(Constants.CONFIG_PATH):
                _config = Config.load(Constants.CONFIG_PATH)
            else:
                _config = Config.loads(yaml.safe_load(
                    Constants.INIT_CONIFG_YML))

    return _config

if __name__ == "__main__":
    config = load_config()
