#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

from wush.web.request import RequestClient
from wush.web.request import RequestBuilder



def main():
    builder = RequestBuilder(method='get', url = 'https://ipconfig.io/json')
    client = RequestClient(builder)
    res = client.request()
    print(res.json())
