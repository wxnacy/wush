#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import json
import os

from flask import Flask
from flask import request

from wush.common.functions import random_int
from wush.common.loggers import create_logger
from wush.wush import Wapi

#  import logging
#  log = logging.getLogger('werkzeug')
#  log.setLevel(logging.ERROR)

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
    }
    return res

PORT = 12000 + int(random_int(3, 1))
os.environ['WUSH_WEB_PORT'] = str(PORT)

def run_server(wapi, port=None):
    global client
    #  app.logger.disabled = True
    #  app.logger.setLevel("ERROR")
    #  log = logging.getLogger('werkzeug')
    #  logger.disabled = True
    client = wapi
    if not port:
        port = PORT
    app.run(host = '0.0.0.0', port=port)

if __name__ == "__main__":
    run_server()
