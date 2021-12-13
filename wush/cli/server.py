#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import json
import os
import sys

from flask import Flask
from flask import request

from wush.common.functions import random_int
from wush.common.loggers import create_logger
from wush.wush import Wapi
from wush.web.utils import telnet

app = Flask(__name__)
client = None

logger = create_logger(__name__)

@app.route('/api/version/<string:version>')
def detail(version):
    client.reload_by_version(version)
    res = client.read()
    data = res
    return data

@app.route('/api/version/<string:version>/<string:type>')
def detail_type(version, type):
    client.reload_by_version(version)
    res = client.read()
    return res.get(type, {})

@app.route('/test', methods=['post', 'get'])
def test():
    res = {
        "args": request.args,
        "json": request.json,
        "data": str(request.data),
        "headers": dict(request.headers),
        "cookies": dict(request.cookies)
    }
    return res

#  PORT = 12000 + int(random_int(3, 1))
PORT = 6060
os.environ['WUSH_WEB_PORT'] = str(PORT)

def run_server(wapi, port=None):
    #  global client

    # 刷新缓冲区
    sys.stdout.flush()
    sys.stderr.flush()

    # 重定向标准输入、输出、错误的描述符
    # dup2函数原子化地关闭和复制文件描述符，重定向到/dev/nul，即丢弃所有输入输出
    with open('/dev/null') as read_null, \
            open('/dev/null', 'w') as write_null:
        os.dup2(read_null.fileno(), sys.stdin.fileno())
        os.dup2(write_null.fileno(), sys.stdout.fileno())
        os.dup2(write_null.fileno(), sys.stderr.fileno())

    #  client = wapi
    if not port:
        port = PORT


    # 如果端口还没有启动，则启动服务
    if not telnet('0.0.0.0', port):
        app.run(host = '0.0.0.0', port=port)

if __name__ == "__main__":
    run_server()
