#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

import requests
import json
from datetime import datetime
from typing import (
    Dict, Any
)
from pydantic import (
   BaseModel, Field, validator
)

from wpy.functools import clock

from wush.common.constants import Constants
from wush.common.loggers import get_logger
from wush.common.run_mode import RunMode
from wush.web.curl_utils import cUrl
from wush.web.enums import MethodEnum
from wush.web.enums import RequestsParamsEnum
from wush.web.response import ResponseClient
from csarg.parser import Argument

__all__ = ['RequestBuilder']

def create_version() -> str:
    return datetime.now().strftime('%Y%m%d%H%M%S_%s')

class RequestBuilder(BaseModel):
    """请求构造器"""
    version: str = Field(title="版本号", default_factory = create_version)
    url: str = Field(..., title="地址")
    method: str = Field(MethodEnum.GET.value, title="请求方式")
    params: Dict[str, Any] = Field({}, title="地址参数")
    json_data: Dict[str, Any] = Field({}, title="json 参数", alias="json")
    body: str = Field(None, title="body 参数")
    headers: Dict[str, Any] = Field({}, title="headers 参数")
    cookies: Dict[str, Any] = Field({}, title="cookies 参数")
    run_mode: RunMode = Field(None, title="运行模式")
    argument: Argument = Field(None, title="参数解析器")

    class Config:
        arbitrary_types_allowed = True

    @validator('method')
    def check_and_format_method(cls, v: str) -> str:
        v = v.upper()
        MethodEnum.validate(v)
        return v

    @classmethod
    def load_curl(cls, curl_file):
        """加载 curl 的本文文件"""
        params = cUrl.dump(curl_file)
        ins = cls(**params)
        ins.format()
        return

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
        data['json'] = self.json_data
        return data


class RequestClient:
    """请求客户端"""
    logger = get_logger('RequestClient')

    def __init__(self, builder: RequestBuilder):
        self.builder = builder

    def request(self):
        """发送请求"""
        params = self.builder.to_requests()
        self.logger.info(f'request builder {json.dumps(params, indent=4)}')
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

