#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

import requests
import json
from datetime import datetime

from wpy.functools import clock

from wush.common.constants import Constants
from wush.common.loggers import get_logger
from wush.common.run_mode import RunMode
from wush.config.models import RequestModel
from wush.web.curl_utils import cUrl
from wush.web.cookie import Cookie
from wush.web.enums import MethodEnum
from wush.web.enums import RequestsParamsEnum
from wush.web.response import ResponseClient
from wush.model import Model
from wush.model import datatype


class RequestBuilder(Model):
    """请求构造器"""
    logger = get_logger('RequestBuilder')
    version = datatype.Str()
    method = datatype.Str(enum=MethodEnum, default=MethodEnum.GET.value,
        upper=True)                     # 请求方式
    url = datatype.Str()                # 地址
    params = datatype.Dict()            # get 请求参数
    json = datatype.Dict()              # post 请求参数
    body = datatype.Str()               # body 请求参数
    headers = datatype.Dict()           # headers 请求参数
    cookies = datatype.Dict()           # cookies 请求参数
    run_mode = datatype.Object(model = RunMode)             # 运行模式
    argument = datatype.Object()  # 参数解析器

    @classmethod
    def load_curl(cls, curl_file):
        """加载 curl 的本文文件"""
        params = cUrl.dump(curl_file)
        ins = cls(**params)
        ins.format()
        return

    @classmethod
    def loads_request_model(cls, request_model: RequestModel,
            with_browser_cookie=False):
        """加载 RequestModel 模型"""
        ins = cls()
        #  request_model.format()
        request_dict = request_model.to_dict()
        for key in RequestsParamsEnum.values():
            #  val = getattr(request_model, key)
            #  if key in ('params', 'json'):
                #  val = val.to_dict()
            val = request_dict.get(key)
            setattr(ins, key, val)

        request_cookies = {}
        # 对 cookie_domains 进行解析
        cookie_domains = request_model.cookie_domains
        if cookie_domains and with_browser_cookie:
            cookies  = Cookie.get_browser_cookie(*cookie_domains)
            request_cookies.update(cookies)
        request_cookies.update(ins.cookies)
        ins.cookies = request_cookies

        ins.format()
        return ins

    def add_headers(self, **kwargs):
        """添加 headers"""
        self.headers.update(kwargs)

    def add_cookies(self, **kwargs):
        """添加 cookies"""
        self.cookies.update(kwargs)

    def set_run_mode(self, mode):
        self.run_mode = RunMode(mode)

    def to_requests(self):
        """转换为 requests 参数"""
        data = {}
        for key in RequestsParamsEnum.values():
            try:
                data[key] = getattr(self, key)
            except:
                pass
        return data

    def format(self):
        self.version = datetime.now().strftime('%Y%m%d%H%M%S_%s')
        super().format()


class RequestClient(object):
    """请求客户端"""
    logger = get_logger('RequestClient')

    def __init__(self, builder: RequestBuilder):
        self.builder = builder

    def request(self):
        """发送请求"""
        params = self.builder.to_requests()
        self.logger.info('request builder %s', json.dumps(params, indent=4))
        res = self._request(**params)
        res_client = ResponseClient(self.builder, res)
        if res_client.status_code in (301, 302):
            url = res_client.location
            res = self._request(url = url)
            res_client = ResponseClient(self.builder, res)

        return res_client

    @clock(fmt = Constants.CLOCK_FMT, logger_func = logger.info)
    def _request(self, **params):
        return requests.request(**params)
