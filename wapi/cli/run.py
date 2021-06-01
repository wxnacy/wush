#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import sys

from wapi.wapi import Wapi


def run():
    import sys
    import os
    args = sys.argv[1:]
    service_name = args[0]
    request_name = args[1]

    client = Wapi()
    client.init_config(service_name = service_name,
        request_name = request_name)

    res = client.request()
    print("Status:")
    print(res.status_code)
    try:
        import json
        print("Format:")
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))
    except:
        print('Content:')
        print(res.content)
        print('解析 json 失败')
    print(client.version)
    #  client.save()
    #  client.open()

if __name__ == "__main__":
    run()

