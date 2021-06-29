#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
models
"""
import json
import sys
import os

from wapi.common import constants
from wapi.common.config_value import ConfigValue
from wapi.common.config import Config
from wapi.common.config import global_config
from wapi.common.cookie import Cookie
from wapi.common.files import FileUtils
from wapi.common.loggers import create_logger
import requests

class BaseModel():

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
        # 获取父配置信息
        parent = config.get("parent")
        if parent:
            parent_path = global_config.get_module_path(parent)
            parent_config = FileUtils.read_dict(parent_path) or {}
            cls._merge_config(parent_config, config)
            config = parent_config
        item._config = config
        for k, v in config.items():
            setattr(item, k, v)
        reqs = []
        #  config.pop('requests', None)
        item.format()
        # 装载 requests
        #  for req_item in item.requests:
            #  # 合并 module 设置
            #  req_item = cls._merge_config(dict(item._config), req_item)
            #  reqs.append(req_item)
        #  item.requests = reqs
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

    def get_request(self, name):
        for item in self.requests:
            #  self.logger.info(item.get("name"))
            if item.get("name") == name:
                item = self._merge_config(dict(self._config), item)
                req_model = RequestModel.load(item)
                req_model.format()
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
        for k, v in config.items():
            setattr(item, k, v)
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


