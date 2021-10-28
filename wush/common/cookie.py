#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import sys
import json

from wush.common.files import FileUtils

chrome = None
try:
    import browsercookie
    chrome = browsercookie.chrome()
except :
    print('can not import browsercookie')
    pass

class Cookie():

    @classmethod
    def get_cookie(cls, domain):
        res = {}
        if not chrome:
            return res
        try:
            for k, v in chrome._cookies.items():
                if domain == k:
                    cookies = v.get("/")
                    for ck, cv in cookies.items():
                        res[ck] = cv.value
        except Exception as e:
            print(e)
        return res

    @classmethod
    def get_cookie_and_save(cls, domain, filepath):
        file_data = FileUtils.read_dict(filepath)
        res = cls.get_cookie(domain)
        if res:
            with open(filepath, 'w') as wf:
                file_data[domain] = res
                wf.write(json.dumps(file_data, indent=4))
        return file_data.get(domain, {})

    @classmethod
    def get_cookie_from_path(cls, domain, filepath):
        file_data = FileUtils.read_dict(filepath)
        return file_data.get(domain, {})

