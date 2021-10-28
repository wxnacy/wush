#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
models
"""
import json
import sys
import os
import requests

from lfsdb import FSModel
from lfsdb import FSColumn

from wush.common import constants
from wush.common.config_value import ConfigValue
from wush.common.cookie import Cookie
from wush.common.files import FileUtils
from wush.common.loggers import create_logger

class BaseModel(object):

    @classmethod
    def _format_str(cls, value):
        if not isinstance(value, str):
            return value

        if value.startswith('@'):
            with open(value[1:], 'r') as f:
                data = []
                for line in f:
                    data.append(line.strip('\n'))
                content = ''.join(data)
                if content.startswith('{') and content.endswith('}'):
                    return json.loads(content)
                return content
        return value

    @classmethod
    def _set_item_attr(cls, item, k, v):
        if hasattr(item, k):
            value = ConfigValue(v).set_env(**item.env).set_functions(
                    **item.functions).format()
            setattr(item, k, value)

    def __str__(self):
        return str(self.__dict__)

    def pretty_str(self):
        data = self.dict()
        functions = data.get("functions")
        if functions:
            for k, v in functions.items():
                functions[k] = k
        return json.dumps(data, indent=4)

    def dict(self):
        data = dict(self.__dict__)
        data.pop('_config', None)
        data.pop('logger', None)
        return data

    def format(self):
        for k, v in self._config.items():
            self._set_item_attr(self, k, v)

    def add_attr(self, k, v):
        """增加属性"""
        if not v:
            return

        if not hasattr(self, k):
            setattr(self, k, v)
            return

        if isinstance(v, dict):
            val = getattr(self, k) or {}
            val.update(v)
            setattr(self, k, val)
            return

        setattr(self, k, v)

    def add_attrs(self, **kwargs):
        for k, v in kwargs.items():
            self.add_attr(k, v)

class ModuleModel(BaseModel):
    logger = create_logger('ModuleModel')
    parent = ''
    module = ''
    protocol = 'http'
    cookie_domains = []
    cookies = {}
    headers = {}
    env = {}
    url_prefix = ''
    requests = []
    _config = {}

    @classmethod
    def load(cls, config):
        item = cls()
        item._config = config
        item.add_attrs(**config)
        item._config.pop('requests', None)
        item.format()
        return item

    @classmethod
    def _merge_config(cls, parent_config, sub_config):
        """合并配置"""
        for k, v in sub_config.items():
            if isinstance(v, dict):
                pv = parent_config.get(k) or {}
                pv.update(v)
                parent_config[k] = pv
            else:
                parent_config[k] = v
        return parent_config

    def format(self):
        for k, v in self._config.items():
            self._set_item_attr(self, k, v)

        # 获取浏览器的 cookies
        if self.cookie_domains:
            total_cookies = self._config.get("cookies") or {}
            for domain in self.cookie_domains:
                _cookies = Cookie.get_cookie(domain) or {}
                total_cookies.update(_cookies)
            self._config['cookies'] = total_cookies

    def get_request(self, name, **kwargs):
        for item in self.requests:
            if item.get("name") == name:
                item = self._merge_config(dict(self._config), item)

                req_model = RequestModel.load(item)
                # 加载参数中的变量
                for k in ('env', 'params', 'json', 'data', 'headers', 'cookies'):
                    v = kwargs.get(k)
                    req_model.add_attr(k, v)
                return req_model

class RequestModel(BaseModel):
    logger = create_logger('RequestModel')
    _config = {}
    module = ''
    domain = ''
    url_prefix = ''
    cookies = {}
    headers = {}
    env = {}
    functions = {}

    protocol = 'http'
    name = ''
    title = ''
    path = ''
    method = 'get'
    data = ''
    json = {}
    params = {}
    filters = []

    url = ''

    @classmethod
    def load(cls, config):
        item = cls()
        item._config = config
        cls.logger.info('Total cookies: %s', config.get("cookies"))
        item.add_attrs(**config)
        item.format()
        return item

    def format(self):
        for k, v in self._config.items():
            self._set_item_attr(self, k, v)
        if not self.title:
            self.title = self.name
        if not self.domain:
            self.domain = '127.0.0.1'

        self.method = self.method.upper()
        # 如果不是完整地址，拼接出完整地址
        self.url = self.path
        if not self.path.startswith('http'):
            self.url = self.url_prefix + self.path
            self.url = '{protocol}://{domain}{url}'.format(
                protocol = self.protocol,
                domain = self.domain, url = self.url)
        self.logger.info('Url: %s', self.url)

        # 处理 headers
        method_headers = self.headers.pop(self.method, None
            ) or self.headers.pop(self.method.lower(), None)
        remove_method_keys = []
        for k, v in self.headers.items():
            if k.upper() in constants.METHODS and isinstance(v, dict):
                remove_method_keys.append(k)
        for key in remove_method_keys:
            self.headers.pop(key, None)

        if isinstance(method_headers, dict):
            self.headers.update(method_headers)

class Client(FSModel):
    db = 'wush'
    table = 'client'

    port = FSColumn(int,)

class Version(FSModel):
    db = 'wush'
    table = 'version'

    version = FSColumn(str,)
    space_name = FSColumn(str,)
    module_name = FSColumn(str,)
    request_name = FSColumn(str,)
    config = FSColumn(dict,)

class Request(FSModel):
    db = 'wush'
    table = 'request'

    #  version = FSColumn(str,)
    #  space_name = FSColumn(str,)
    #  module_name = FSColumn(str,)
    #  request_name = FSColumn(str,)
    #  config = FSColumn(dict,)

class Response(FSModel):
    db = 'wush'
    table = 'response'

    content = FSColumn(str,)
    json = FSColumn(dict,)
    headers = FSColumn(dict,)
