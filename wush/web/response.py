#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""

"""

import json

from wpy.base import BaseEnum

class ResponseField(BaseEnum):
    HEADERS = 'headers'
    OK = 'ok'
    URL = 'url'
    CONTENT = 'content'
    TEXT = 'text'
    STATUS_CODE = 'status_code'


class ResponseClient(object):
    """返回客户端"""
    content = None
    text = None
    status_code = None
    url = None
    ok = None
    headers = None

    def __init__(self, response):
        self.response = response
        for key in ResponseField.values():
            setattr(self, key, getattr(self.response, key))

    @property
    def content_type(self):
        return self.headers['Content-Type']

    def is_json(self):
        if self.content_type in ('application/json'):
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

