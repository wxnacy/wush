#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
配置模型
"""

from wpy.base import BaseObject

from wush.common.base import BaseModel
from wush.common.base import ModelColumn
from wush.common.base import List




class RequestModel(BaseModel):
    domain = ''
    url_prefix = ''
    cookies = {}
    headers = {}

    protocol = 'http'
    name = ''
    title = ''
    path = ''
    method = 'get'
    data = ''
    json = {}
    params = {}

class ModuleModel(BaseModel):
    name = ModelColumn(str)
    protocol = 'http'
    url_prefix = ''
    cookie_domains =[]
    cookies = {}
    headers = {}
    requests = ModelColumn(List(RequestModel))

class ConfigModel(BaseModel):
    modules = ModelColumn(List(ModuleModel), default=[])
    env = ModelColumn(dict, default={})
    test = ModelColumn(dict, default={})
