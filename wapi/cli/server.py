#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import json

from flask import Flask
from flask import request
from wapi.common.loggers import create_logger

#  from apis.repos import Repos

app = Flask(__name__)

logger = create_logger(__name__)

@app.route('/api/detail')
def api_detail():
    args = request.args
    version = args.get("version")
    service_name = args.get("service_name")
    request_name = args.get("request_name")
    client = Repos()
    client.init_config(
        version = version,
        service_name = service_name,
        request_name = request_name
    )
    with open(client.response_path, 'r') as f:
        resp_lines = f.readlines()
        resp = json.loads(''.join(resp_lines))

    with open(client.request_path, 'r') as f:
        req_lines = f.readlines()
        req = json.loads(''.join(req_lines))

    res = {
        "request": req,
        "response": resp
    }
    return res

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

def run_server(port):
    #  app.logger.disabled = True
    #  app.logger.setLevel("ERROR")
    #  log = logging.getLogger('werkzeug')
    #  logger.disabled = True
    app.run(host = '0.0.0.0', port=port, debug=False)

if __name__ == "__main__":
    run_server()
