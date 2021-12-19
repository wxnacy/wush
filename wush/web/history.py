#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
请求历史
"""


from lfsdb import FSModel
from lfsdb import FSColumn

from wush.web.response import ResponseClient

class HistoryModel(FSModel):
    db = 'wush'
    table = 'history'

    version = FSColumn(str)
    request_builder = FSColumn(dict)
    response = FSColumn(dict)

class History(object):

    @classmethod
    def save(cls, response_client: ResponseClient):

        h = HistoryModel()
        h.version = response_client.request_builder.version
        h._id = h.version
        h.request_builder = response_client.request_builder.to_dict()
        res = {
                'json': response_client.json()
                }
        h.response = res
        h.save()
