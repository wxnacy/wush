#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
Wush
"""

import sys
import yaml
import os
import requests
import json
import cgi
import traceback

from datetime import datetime
from wush.common import constants
from wush.common import utils
from wush.common.files import FileUtils
from wush.common.loggers import create_logger
from wush.common.cookie import Cookie
from wush.common.config import Config
from wush.common.exceptions import RequestException

from wush.models import ModuleModel
from .models import Client
from .models import Version
from .models import Request
from .models import Response

class Wapi():
    logger = create_logger('Wush')
    module_name = ''
    request_name = ''
    space_name = ''
    config_root = ''
    _config = None
    _request = None
    _url = None
    _response = None
    is_dynamic_space = True

    def __init__(self, name=None, is_dynamic_space = True, **kw):
        if not name:
            name = __name__
        self.name = name
        self.is_dynamic_space = is_dynamic_space
        self.version = self.create_id()
        self._id = self.version
        self.config_root = Config.get_default_root()
        self.init_config(**kw)

    def reload_by_version(self, version):
        """通过版本号重新加载"""
        self.version = version
        #  data = FileUtils.read_dict(self.version_path)
        data = Version.find_one_by_id(version).to_dict()
        self.init_config(**data)

    @classmethod
    def create_id(cls):
        return datetime.now().strftime('%Y%m%d%H%M%S_%s')

    @property
    def config(self):
        """获取配置"""
        return self._config

    def _change_config(self, config_root=None, config=None):
        if self._config and not config_root and not config:
            return

        if config_root:
            self.config_root = config_root

        # 优先使用传入的 config
        if isinstance(config, dict):
            self._config = Config.load(config)

        # 在使用地址获取配置
        if not self._config and self.config_root:
            self._config = Config.load(self.config_root)

    def init_config(self,**kw):
        """初始化配置"""
        config = kw.pop('config', None)
        # config 地址
        config_root = kw.pop('config_root', None)

        # 改变配置
        self._change_config(config_root, config)

        self.logger.info('init_config kwargs %s', kw)
        for k, v in kw.items():
            if v:
                setattr(self, k, v)

        # 配置 space_name
        if not self.space_name or self.is_dynamic_space:
            self.logger.info('wush %s', self.name)
            current_space_name = self.config.get_function().get_current_space_name()
            self.logger.info('current_space_name %s', current_space_name)
            self.space_name = current_space_name

        self._config.set_space_name(self.space_name)
        self.logger.info("Space: %s", self.space_name)

        # 设置默认 module
        if not self.module_name:
            self.module_name = self.config.get_default_module_name()

        self._init_environ()
        self._build()

    def _init_environ(self):
        '''初始化环境变量'''
        current_body_name = self.config.get_current_body_name(
                self.space_name, self.module_name,self.request_name)
        current_body_path = self.config.get_body_path(current_body_name)
        self.config.env.add(**dict(
            body_path = current_body_path
        ))

    def build(self, **kwargs):
        """
        构建请求
        :param kwargs:
        """
        for k in ('space_name', 'module_name', 'request_name'):
            val = kwargs.pop(k, None)
            if val:
                setattr(self, k, val)

        self._build(**kwargs)
        return self

    def _build(self, **kwargs):
        """获取 request
        :param dict kwargs:
            `env` 环境变量
        """
        if not self.request_name or not self.module_name:
            return
        module = self.config.get_module(self.module_name)
        request = module.get_request(self.request_name, **kwargs)
        if not request:
            return
        self._request = request
        self.logger.info('RequestModel: %s', request)
        self._url = request.url
        self._request_data = { }
        # 注入 request 必要的参数
        for k in ('method', 'url'):
            self._request_data[k] = getattr(self._request, k)
        # 注入 request 必要的参数
        for name in ('json', 'data', 'headers', 'cookies', 'params'):
            value =  getattr(self._request, name)
            if value:
                self._request_data[name] = value
        self.logger.info('Request data: %s', self._request_data)

    def request(self, **kwargs):
        self.version = self.create_id()
        if kwargs:
            self.build(**kwargs)

        res = requests.request(**self._request_data)

        self.response_content = res.content
        self._response = res
        self.logger.info('Response')
        response_data = {}
        response_data['headers'] = dict(res.headers)
        self.logger.info(json.dumps(response_data, indent=4))
        return res

    @property
    def url(self):
        return self._url

    @property
    def response(self):
        return self._response

    def print_response(self):
        """打印返回结果"""
        print('Space:', self.space_name)
        print('Module:', self.module_name)
        print('Name:', self.request_name)
        print("Status:", self._response.status_code)
        try:
            data = self._response.json()
            try:
                data = utils.filter_json(data, self._request.filters)
            except Exception as e:
                pass
            print("Format:")
            print(json.dumps(data, indent=4, ensure_ascii=False))
        except:
            print('Content:')
            print(self._response.content)
            print('解析 json 失败')

    def get_pertty_response_content(self):
        """获取好看的 response content 内容"""
        try:
            data = self._response.json()
            try:
                data = utils.filter_json(data, self._request.filters)
            except:
                self.logger.error(traceback.format_exc())
            return json.dumps(data, indent=4, ensure_ascii=False)
        except:
            self.logger.error(traceback.format_exc())
            return self._response.content

    @property
    def response_path(self):
        """结果存储地址"""
        filename = '{}-{}'.format(self.module_name, self.request_name)
        if self._response:
            headers = dict(self._response.headers)
            content_type = headers.get("content-type") or ''
            # 处理office文件的报错
            if 'office' in content_type:
                content_disposition = headers.get("content-disposition")
                _, params = cgi.parse_header(content_disposition)
                filename = params.get("filename")

        path = os.path.join(self.config.response_root, '{}-{}'.format(
            self.version, filename))

        self.logger.info('response_path %s', path)
        return path

    def save(self):
        """保存请求配置"""
        self._save_version()
        self._save_request()
        res = Response(_id = self.version)
        try:
            res.json = json.loads(self.response_content)
        except Exception as e:
            print(e)
            res.content = self.response_content
        res.headers = dict(self.response.headers)
        res.save()

    def _save_version(self):
        data = {
            "version": self.version,
            "space_name": self.space_name,
            "module_name": self.module_name,
            "request_name": self.request_name,
            "config": self.config.dict(),
        }
        v = Version(_id = data['version'], **data)
        v.save()

    def _save_request(self):
        r = Request(_id = self.version, **self._request_data)
        r.save()

    def read(self):
        data = {
            "version": Version.find_one_by_id(self.version).to_dict(),
            "request": Request.find_one_by_id(self.version).to_dict(),
            "response": Response.find_one_by_id(self.version).to_dict(),
        }
        return data
