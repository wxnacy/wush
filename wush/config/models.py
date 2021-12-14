#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
配置模型
"""

from wush.model import datatype
from wush.model.model import Model
from wush.web.enums import MethodEnum
from wush.web.enums import ProtocolEnum

class RequestModel(Model):
    name = datatype.Str()
    title = datatype.Str()
    path = datatype.Str()
    method = datatype.Str(enum = MethodEnum, default=MethodEnum.GET.value,
        upper=True)
    protocol = datatype.Str()
    domain = datatype.Str()
    cookies = datatype.Dict()
    headers = datatype.Dict()
    json = datatype.Dict()
    params = datatype.Dict()
    data = datatype.Str()
    url = datatype.Str()

class ModuleModel(Model):
    name = datatype.Str()
    protocol = datatype.Str(enum = ProtocolEnum,
            default=ProtocolEnum.HTTP.value)
    domain = datatype.Str()
    url_prefix = datatype.Str()
    cookie_domains = datatype.List()
    cookies = datatype.Dict()
    headers = datatype.Dict()
    requests = datatype.List(model=RequestModel)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__req__ = {o.name: o for o in self.requests}

    def get_request(self, name):
        """获取 request 模型"""
        req = self.__req__.get(name)
        if req:
            # 继承 module 的字段
            inherit_keys = ('protocol', 'domain', 'cookies', 'headers')
            for key in inherit_keys:
                super_value = getattr(self, key)
                if not getattr(req, key):
                    setattr(req, key, super_value)
                else:
                    if isinstance(super_value, dict):
                        super_value = dict(super_value)
                        super_value.update(getattr(req, key))
                        setattr(req, key, super_value)

            # 拼装 url
            if not req.url:
                req.url = f'{req.protocol}://{req.domain}' \
                    f'{self.url_prefix}{req.path}'
        return req

class ConfigModel(Model):
    """客户端全局配置模型"""
    modules = datatype.List(model = ModuleModel)
    env = datatype.Dict()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.modules)
        self.__mod__ = {o.name: o for o in self.modules}

    def get_module(self, name):
        """获取模块"""
        module = self.__mod__.get(name)
        return module
