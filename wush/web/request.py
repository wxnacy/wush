#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

import requests

from wush.config.models import RequestModel
from wush.web.curl_utils import cUrl
from wush.web.enums import MethodEnum
from wush.web.enums import RequestsParamsEnum
from wush.web.response import ResponseClient
from wush.model import Model
from wush.model import datatype


class RequestBuilder(Model):
    """请求构造器"""
    method = datatype.Str(enum=MethodEnum, default=MethodEnum.GET.value,
        upper=True)                     # 请求方式
    url = datatype.Str()                # 地址
    params = datatype.Dict()            # get 请求参数
    json = datatype.Dict()              # post 请求参数
    body = datatype.Str()               # body 请求参数
    headers = datatype.Dict()           # headers 请求参数
    cookies = datatype.Dict()           # cookies 请求参数

    @classmethod
    def load_curl(cls, curl_file):
        """加载 curl 的本文文件"""
        params = cUrl.dump(curl_file)
        return cls(**params)

    @classmethod
    def loads_request_model(cls, request_model: RequestModel):
        """加载 RequestModel 模型"""
        pass

    def add_headers(self, **kwargs):
        """添加 headers"""
        self.headers.update(kwargs)

    def add_cookies(self, **kwargs):
        """添加 cookies"""
        self.cookies.update(kwargs)

    def to_requests(self):
        """转换为 requests 参数"""
        data = {}
        for key in RequestsParamsEnum.values():
            try:
                data[key] = getattr(self, key)
            except:
                pass
        return data


class RequestClient(object):
    """请求客户端"""

    def __init__(self, builder: RequestBuilder):
        self.builder = builder

    def request(self):
        """发送请求"""
        res = requests.request(**self.builder.to_requests())
        return ResponseClient(res)

