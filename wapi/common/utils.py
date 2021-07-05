#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
工具模块
"""

import json
import os

from collections import defaultdict

from wapi.common.functions import run_shell
from wapi.common.exceptions import JsonException

def filter_json(data, rules):
    """
    过滤 json 数据
    :param dict data: 过滤的数据
    :param list rules: 过滤规则，例：{"name"}

    最终拼成的命令格式如下
    echo '{"id": 1, "name": "wxnacy"}' | jq '{"name"}'
    """
    cmd_fmt = "echo '{}' | jq '{}'"
    text = json.dumps(data)
    for rule in rules:
        cmd = cmd_fmt.format(text , rule)
        content, err = run_shell(cmd)
        if err:
            raise JsonException(err)
        return json.loads(content)
    return data

def fmt_path(path):
    """格式化地址"""
    path = os.path.expanduser(path)
    return path

def search(datas, word):
    """搜索"""
    patten = {}
    for o in datas:
        patten[o] = 0
        p = o.lower()
        if word not in p:
            continue
        patten[o] += 1
        if p.startswith(word):
            patten[o] += 1
    datas = list(filter(lambda x: patten[x] > 0, datas))
    datas.sort(key = lambda x: patten[x], reverse=True)
    return datas
