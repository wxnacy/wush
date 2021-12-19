#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

import json

from wpy.base import BaseEnum
from wpy.base import BaseObject

from wush.web.enums import HeaderEnum
from wush.web.enums import ContentTypeEnum

class ResponseField(BaseEnum):
    HEADERS = 'headers'
    OK = 'ok'
    URL = 'url'
    CONTENT = 'content'
    TEXT = 'text'
    STATUS_CODE = 'status_code'


class ResponseClient(BaseObject):
    """返回客户端"""
    request_builder = None
    content = None
    text = None
    status_code = None
    url = None
    ok = None
    headers = None

    def __init__(self, request_builder, response):
        self.request_builder = request_builder
        self.response = response
        for key in ResponseField.values():
            setattr(self, key, getattr(self.response, key))

    @property
    def content_type(self):
        return self.headers[HeaderEnum.CONTENT_TYPE.value]

    def is_json(self):
        """判断结果是否为 json 格式"""
        if ContentTypeEnum.APPLICATION_JSON.value in self.content_type:
            return True
        return False

    def json(self, **kwargs):
        return self.response.json(**kwargs)

    def save(self, savepath=None):
        """保存"""
        if self.is_json():
            with open(savepath, 'w') as f:
                f.write(json.dumps(self.json(), indent=4))
        else:
            with open(savepath, 'wb') as f:
                f.write(self.content)

    def print(self):
        if self.is_json():
            print(json.dumps(self.json(), indent=4))
        else:
            print(self.text)


