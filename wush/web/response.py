#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

import json
from typing import MutableMapping, Any, Dict, Callable
from requests.cookies import RequestsCookieJar
from requests import Response

from wpy.base import BaseEnum
from wpy.base import BaseObject

from wush.web.enums import HeaderEnum
from wush.web.enums import ContentTypeEnum
from .models import RequestBuilder

__all__ = ['ResponseClient']

class ResponseField(BaseEnum):
    HEADERS = 'headers'
    COOKIES = 'cookies'
    OK = 'ok'
    URL = 'url'
    CONTENT = 'content'
    TEXT = 'text'
    STATUS_CODE = 'status_code'


class ResponseClient(BaseObject):
    """返回客户端"""
    request_builder: RequestBuilder
    content: bytes
    text: str
    status_code: int
    url: str
    ok: bool = None
    headers: MutableMapping[str, str] = None
    cookies: RequestsCookieJar = None
    response: Response

    def __init__(self, request_builder: RequestBuilder, response: Response):
        self.request_builder = request_builder
        self.response = response
        for key in ResponseField.values():
            setattr(self, key, getattr(self.response, key))

    @property
    def content_type(self) -> str:
        return self.headers[HeaderEnum.CONTENT_TYPE.value]

    @property
    def location(self) -> str:
        return self.headers[HeaderEnum.LOCATION.value]

    @property
    def is_html(self) -> bool:
        return ContentTypeEnum.TEXT_HTML.value in self.content_type

    @property
    def is_json(self) -> bool:
        """判断结果是否为 json 格式"""
        if ContentTypeEnum.APPLICATION_JSON.value in self.content_type:
            return True
        return False

    def json(self, **kwargs) -> Any:
        return self.response.json(**kwargs)

    def save(self, savepath: str=None):
        """保存"""
        if self.is_json:
            with open(savepath, 'w') as f:
                f.write(json.dumps(self.json(), indent=4))
        else:
            with open(savepath, 'wb') as f:
                f.write(self.content)

    def print(self):
        if self.is_json:
            print(json.dumps(self.json(), indent=4))
        else:
            print(self.text)


class ResponseHandler(BaseObject):

    _factory: Dict[str, Callable[[ResponseClient], Any]] = {}

    @classmethod
    def register(cls, module: str, name: str) -> Callable[[Callable], Any]:
        def decorate(func):
            key = f"{module}-{name}"
            cls._factory[key] = func
            return func
        return decorate

    @classmethod
    def get_handler(cls, module: str, name: str
            ) -> Callable[[ResponseClient], Any]:
        """获取处理结果的方法
        """
        key = f"{module}-{name}"
        return cls._factory.get(key)
