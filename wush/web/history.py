#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
请求历史
"""


from wpy.files import FileUtils

from wush.web.response import ResponseClient

class HistoryModel(object):
    db = 'wush'
    table = 'history'

    version = ''
    request = dict()
    response = dict()

class History(object):

    @classmethod
    def save(cls, response_client: ResponseClient):
        pass

        h = HistoryModel()
        h.version = response_client.request_builder.version
        h._id = h.version
        h.request = response_client.request_builder.to_dict()
        res = {
            'is_json': response_client.is_json(),
            'json': response_client.json(),
            'text': response_client.text
        }
        h.response = res
        h.save()

    @classmethod
    def read(cls, version):
        return {}
        h = HistoryModel.find_one_by_id(version)
        return h.to_dict()
