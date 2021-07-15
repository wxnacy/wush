#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import json

from flask import Flask
from flask import request

from wapi.common.loggers import create_logger
from wapi.wapi import Wapi

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
    data.pop('version', None)
    return data

@app.route('/test', methods=['post', 'get'])
def test():
    res = {
        "args": request.args,
        "json": request.json,
        "data": str(request.data),
        "headers": dict(request.headers),
    }
    return res

PORT = 12345

def run_server(wapi, port):
    global client
    #  app.logger.disabled = True
    #  app.logger.setLevel("ERROR")
    #  log = logging.getLogger('werkzeug')
    #  logger.disabled = True
    client = wapi
    app.run(host = '0.0.0.0', port=port)

if __name__ == "__main__":
    run_server()
