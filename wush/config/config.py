#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
配置模块
"""
import os
import yaml

from wush.config.models import ConfigModel
from wush.common.config_value import ConfigValue
from wush.common.loggers import get_logger

class Config(object):
    logger = get_logger('Config')

    _config = None
    _config_dir = None

    def __init__(self, *args, **kwargs):
        self._config_dir = None
        self._config = None

    @classmethod
    def read_yml(cls, filepath):
        """读取 yml 文件"""
        with open(conf_file, 'r') as f:
            return yaml.safe_load(f)

    @classmethod
    def load(cls, conf_file):
        """通过文件加载"""
        # 去读 yml 文件
        data = cls.read_yml(conf_file)

        ins = cls.loads(data)
        # 获取配置目录
        ins._config_dir = os.path.dirname(conf_file)
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

        return ins

    def get_request(self, module_name, request_name):
        """获取请求模型"""
        req = self._config.get_module(module_name).get_request(request_name)
        env = self._config.env.to_dict()
        self.logger.info('config env {}'.format(env))

        # 将请求模型做环境变量格式化处理并返回
        return ConfigValue(req).set_env(**env).format()

if __name__ == "__main__":
    filepath = 'tests/data/config/config.yml'
    config = Config.load(filepath)
    with open('tests/data/config/config.yml', 'r') as f:
        data = yaml.safe_load(f)
    config = ConfigModel(**data)
    #  print(config.modules)
    import json
    print(json.dumps(config.to_dict(), indent=4))
    #  print('test')

