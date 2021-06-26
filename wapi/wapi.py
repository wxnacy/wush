#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
Wapi
"""

import sys
import yaml
import os
import requests
import json
import cgi

from datetime import datetime
from wapi.common import constants
from wapi.common import utils
from wapi.common.files import FileUtils
from wapi.common.loggers import create_logger
from wapi.common.cookie import Cookie
from wapi.common.config import Config
from wapi.common.decorates import env_functions
from wapi.common.exceptions import RequestException
from wapi.common.functions import super_function

from wapi.models import ModuleModel

class Wapi():
    logger = create_logger('Wapi')
    module_name = ''
    request_name = ''
    space_name = ''
    _config = None
    request = None
    response = None

    def __init__(self, **kw):
        self.version = datetime.now().strftime('%Y%m%d%H%M%S.%s')
        self.init_config(**kw)

    @property
    def config(self):
        """获取配置"""
        return self._config

    def init_config(self,**kw):
        """初始化配置"""
        config = kw.pop('config', None)
        # config 地址
        config_root = kw.pop('config_root', None)
        if not config_root:
            config_root = Config.get_default_root()

        # 优先使用传入的 config
        if isinstance(config, dict):
            self._config = Config.load(config)

        # 在使用地址获取配置
        if not self._config and config_root:
            self._config = Config.load(config_root)

        for k, v in kw.items():
            if v:
                setattr(self, k, v)
        self.logger.info('current_space_name %s',
            self.config.get_function().get_current_space_name())
        if not self.space_name:
            self.space_name = self.config.get_function().get_current_space_name()
        if not self.module_name:
            self.module_name = self.config.get_default_module_name()

        self._init_environ()
        #  self._init_common_info()

    #  def _init_common_info(self):
        #  # 临时数据保存目录
        #  self.save_root = '{}/tmp/api'.format(os.getenv("YDWORK_HOME"))
        #  if not os.path.exists(self.save_root):
            #  os.makedirs(self.save_root)

        #  # 公共地址
        #  self.common_save_path = (
            #  '{root}/{version}-{{ftype}}-{service}-{request}.json'
        #  ).format(root = self.save_root, version = self.version,
            #  service = self.service_name, request = self.request_name)
        #  # 返回数据地址
        #  self.response_path = os.path.join(self.config.response_root, )
        #  # 请求数据地址
        #  self.request_path = self.common_save_path.format(ftype = 'request')

    def _init_environ(self):
        '''初始化环境变量'''
        current_body_name = self.config.get_current_body_name(
                self.space_name, self.module_name,self.request_name)
        current_body_path = self.config.get_body_path(current_body_name)
        self.config.get_env().add(**dict(
            body_path = current_body_path
        ))


    def _get_request(self, **kwargs):
        """获取 request
        :param dict kwargs:
            `env` 环境变量
        """
        # 如果 module 还没有赋值，给默认值
        if not self.module_name:
            self.module_name = self.config.get_default_module_name()
        # 获取 request 信息
        self.logger.info('Module: %s', self.module_name)
        request_path = self.config.get_module_path(self.module_name)
        self.logger.info('Request path: %s', request_path)
        if not os.path.exists(request_path):
            raise RequestException('can not found request config {}'.format(
                request_path))
        module_config = FileUtils.read_dict(request_path)
        # 获取 env 信息
        env_config = module_config.get("env") or {}
        env_config.update(self.config.get_env().dict())
        env_path = self.config.get_env_path(self.space_name)
        self.logger.info('env_path %s', env_path)
        if os.path.exists(env_path):
            env_config.update(FileUtils.read_dict(env_path) or {})
        module_config['functions'] = env_functions
        module_config['env'] = env_config

        # 加载 kwargs 参数中的配置
        for k in ('env',):
            v = kwargs.get(k)
            if isinstance(v, dict):
                module_val = module_config.get(k) or {}
                module_val.update(v)
                module_config[k] = module_val

        # 加载并获取 request
        module = ModuleModel.load(module_config)
        request = module.get_request(self.request_name)
        return request

    def request(self, **kwargs):
        self.request = self._get_request(**kwargs)
        # 初始化参数
        url = self.request.url
        request_model = self.request

        kw = { }
        for name in ('json', 'data', 'headers', 'cookies', 'params'):
            value =  getattr(self.request, name)
            if value:
                kw[name] = value

        for k, v in kwargs.items():
            if isinstance(v, dict):
                conf_k = kw.get(k) or {}
                conf_k.update(v)
                kw[k] = conf_k

        self.request_data = kw
        self.logger.info('Request data: %s', self.request_data)

        self.logger.info(request_model.pretty_str())
        self.logger.info('Url: %s', url)
        res = requests.request(request_model.method, url, **kw)
        self.response_content = res.content
        self.response = res
        self.logger.info('Response')
        response_data = {}
        response_data['headers'] = dict(res.headers)
        self.logger.info(json.dumps(response_data, indent=4))
        return res

    def print_response(self):
        """打印返回结果"""
        print('Space:', self.space_name)
        print('Module:', self.module_name)
        print('Name:', self.request_name)
        print("Status:", self.response.status_code)
        try:
            data = self.response.json()
            try:
                data = utils.filter_json(data, self.request.filters)
            except Exception as e:
                pass
            print("Format:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
        except:
            print('Content:')
            print(self.response.content)
            print('解析 json 失败')

    @property
    def response_path(self):
        """结果存储地址"""
        filename = None
        if self.response:
            headers = dict(self.response.headers)
            content_type = headers.get("content-type") or ''
            # 处理office文件的报错
            if 'office' in content_type:
                content_disposition = headers.get("content-disposition")
                _, params = cgi.parse_header(content_disposition)
                filename = params.get("filename")
            else:
                filename = '{}-{}'.format(self.module_name, self.request_name)

        path = os.path.join(self.config.response_root, '{}-{}'.format(
            self.version, filename))

        self.logger.info('response_path %s', path)
        return path

    def save(self):
        """保存请求配置"""
        save_path = self.response_path
        try:
            save_data = json.dumps(json.loads(
                self.response_content), indent=4, ensure_ascii=False)
            with open(save_path, 'w') as f:
                f.write(save_data)
                #  f.write(save_data.encode('utf-8'))
        except Exception as e:
            print(e)
            with open(save_path, 'bw') as f:
                f.write(self.response_content)

    def open(self):
        #  """打开请求信息"""
        request_url = ("http://0.0.0.0:8801/api/detail?"
            "version={}&service_name={}&request_name={}").format(
                self.version, self.service_name, self.request_name
        )
        self.logger.info('open %s', request_url)
        os.system('open -a "/Applications/Google Chrome.app" "{}"'.format(
            request_url))
        pass

