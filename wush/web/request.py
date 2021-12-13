#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

import requests

from wpy.base import BaseEnum
from wpy.base import BaseObject

from wush.web.curl_utils import cUrl
from wush.web.response import ResponseClient

class Method(BaseEnum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'
    HEAD = 'HEAD'
    OPTIONS = 'OPTIONS'
    PATCH = 'PATCH'


class RequestBuilder(BaseObject):
    """请求构造器"""
    method = Method.GET.value           # 请求方式
    url = None              # 地址
    params = None           # get 请求参数
    json = None             # post 请求参数
    body = None             # body 请求参数
    headers = {}            # headers 请求参数
    cookies = {}            # cookies 请求参数

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.method:
            self.method = Method.GET.value

    @classmethod
    def load_curl(cls, curl_file):
        """加载 curl 的本文文件"""
        params = cUrl.dump(curl_file)
        return cls(**params)

    def add_headers(self, **kwargs):
        """添加 headers"""
        self.headers.update(kwargs)

    def add_cookies(self, **kwargs):
        """添加 cookies"""
        self.cookies.update(kwargs)


class RequestClient(object):
    """请求客户端"""

    def __init__(self, builder: RequestBuilder):
        self.builder = builder

    def request(self):
        """发送请求"""
        params = self.builder.to_dict()
        res = requests.request(**params)
        return ResponseClient(res)

def main():
    url = 'http://localhost:8093/myvideos/2729/progress'
    #  url = 'http://localhost:8093/myvideos/?type=process_task'
    builder = RequestBuilder(method='get', url = url)
    client = RequestClient(builder)
    res = client.request()
    if res.is_json():
        print(res.json())
    print(res.response.headers['Content-Type'])
    print(res.response.url)
    print(res.ok)
    print(type(res.content))

if __name__ == "__main__":
    main()
