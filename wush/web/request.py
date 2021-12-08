#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

class RequestClient(object):

    def __init__(self, builder: RequestBuilder):
        pass

    def request(self):
        pass


class RequestBuilder(object):
    """请求构造器"""
    method = None           # 请求方式
    url = None              # 地址
    params = None           # get 请求参数
    json = None             # post 请求参数
    headers = {}             # post 请求参数
    cookies = {}             # post 请求参数

    @classmethod
    def build_by_curl(cls, curl):
        """通过 curl 命令构造"""

    def requests(self):
        return
