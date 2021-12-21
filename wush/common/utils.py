#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
工具模块
"""

import json
import os
import importlib
import subprocess

from collections import defaultdict

from wush.common.exceptions import JsonException

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
    """
    搜索
    :param list datas: 单词列表
    :param str word: 搜索的单词
    :results list 搜索结果，按照匹配位置排序
    """
    patten = defaultdict(int)
    for o in datas:
        patten[o] = -1
        p = o.lower()
        if word not in p:
            continue
        patten[o] = p.index(word)
    res = list(filter(lambda x: patten[x] > -1, datas))
    res.sort(key = lambda x: patten[x])
    return res

def list_key_val_to_dict(data):
    """
    键值对列表转为字典
    :param data: ['name=wxnacy', 'key=True', 'test']
    :returns { 'name': 'wxnacy', 'key': 'True'  }
    """
    res = {}
    for item in data:
        if '=' in item:
            k, v = item.split('=')
            res[k] = v
    return res

def run_shell(command):
    """运行 shell 语句"""
    res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
        stderr = subprocess.PIPE)
    return res.communicate()

def load_module(module_name):
    """加载模块"""
    views_module = importlib.import_module(module_name)
    return views_module
