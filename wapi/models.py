#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
models
"""
import json
import sys

from common.config_value import ConfigValue

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
            value = ConfigValue(v).set_env(**item.env).format()
            if isinstance(value, dict):
                for v_k, v_v in value.items():
                    value[v_k] = ConfigValue(v_v).set_env(**item.env).format()
            setattr(item, k, value)

    def __str__(self):
        return str(self.__dict__)

    def pretty_str(self):
        data = self.dict()
        return json.dumps(data, indent=4)

    def dict(self):
        data = dict(self.__dict__)
        data.pop('_config', None)
        return data

    def format(self):
        for k, v in self._config.items():
            self._set_item_attr(self, k, v)


class ServiceModel(BaseModel):
    service = ''
    cookies = {}
    env = {}
    url_prefix = ''
    requests = []
    _config = {}

    @classmethod
    def load(cls, config):
        item = cls()
        item._config = config
        for k, v in config.items():
            setattr(item, k, v)
        reqs = []
        config.pop('requests', None)
        # 装载 requests
        for req_item in item.requests:
            req_item.update(config)
            reqs.append(req_item)
        item.requests = reqs
        item.format()
        return item

    def get_request(self, name):
        for item in self.requests:
            if item.get("name") == name:
                req_model = RequestModel.load(item)
                req_model.format()
                return req_model

class RequestModel(BaseModel):
    _config = {}
    service = ''
    domain = ''
    url_prefix = ''
    cookies = {}
    env = {}

    name = ''
    title = ''
    url = ''
    method = 'get'
    data = {}
    json = {}
    params = {}

    @classmethod
    def load(cls, config):
        item = cls()
        item._config = config
        for k, v in config.items():
            setattr(item, k, v)
        return item

    def format(self):
        for k, v in self._config.items():
            self._set_item_attr(self, k, v)
        self.url = self.url_prefix + self.url

