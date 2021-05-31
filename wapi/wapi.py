#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
Wapi
"""

import sys
import yaml
import os
import requests
import json

from datetime import datetime
from common import utils
from common.loggers import create_logger
from common.cookie import Cookie

from api.models import ServiceModel

class Wapi():
    logger = create_logger('Wapi')

    def __init__(self, *args, **kwargs):
        self.version = datetime.now().strftime('%Y%m%d%H%M%S.%s')
        #  self.params_temp_filepath = 'tmp/{}.params.{}.json'.format()

    def init_config(self,**kw):
        for k, v in kw.items():
            if v:
                print(k, v)
                setattr(self, k, v)
        self.init_common_info()

    def init_common_info(self):
        # 临时数据保存目录
        self.save_root = '{}/tmp/api'.format(os.getenv("YDWORK_HOME"))
        if not os.path.exists(self.save_root):
            os.makedirs(self.save_root)

        # 公共地址
        self.common_save_path = (
            '{root}/{version}-{{ftype}}-{service}-{request}.json'
        ).format(root = self.save_root, version = self.version,
            service = self.service_name, request = self.request_name)
        # 返回数据地址
        self.response_path = self.common_save_path.format(ftype = 'response')
        # 请求数据地址
        self.request_path = self.common_save_path.format(ftype = 'request')

    def _init_environ(self):
        '''初始化环境变量'''
        # 参数文件地址
        #  os.environ['PARAMS_FILEPATH'] = (
            #  'config/api/params/{}/{}/{}/{}.json'.format(
                #  utils.CLUSTER, utils.TARGET, self.service_name,
                #  self.request_name
            #  )
        #  )
        #  self.logger.info('PARAMS_FILEPATH %s', os.getenv('PARAMS_FILEPATH'))

    def get_request(self, service_name, request_name):
        self.service_name = service_name
        self.request_name = request_name
        print(self.service_name, self.request_name)
        self._init_environ()
        with open('config/api/api.yml'.format(service_name), 'r') as f:
            api_config = yaml.safe_load(f)
        with open('config/api/{}.yml'.format(service_name), 'r') as f:
            service_config = yaml.safe_load(f)
        env_config = {}
        #  with open('config/api/params/{}/{}/env.yml'.format(utils.CLUSTER,
            #  utils.TARGET), 'r') as f:
            #  env_config = yaml.safe_load(f)
        api_config.update(service_config)
        env = api_config.get("env") or {}
        env.update(env_config)
        api_config['env'] = env
        service = ServiceModel.load(api_config)
        request = service.get_request(request_name)
        return request

    def request(self, service_name=None, request_name=None, json=None,
            params = None):
        _json = json
        # 初始化参数
        self.init_config(service_name = service_name,
            request_name = request_name)
        request_model = self.get_request(self.service_name, self.request_name)
        domain = request_model.domain
        self.logger.info('Domain: %s', domain)
        url = 'http://{domain}{url}'.format(
            domain = domain, url = request_model.url
        )

        # 获取  Cookie
        cookies = { }
        cookies.update(request_model.cookies)
        for k, v in cookies.items():
            self.logger.info('Cookie %s: %s', k, v)

        kw = {
            "cookies": cookies
        }

        # 获取 json 参数
        json_data = request_model.json
        if _json:
            json_data = _json
        if json_data:
            kw['json'] = json_data

        # 获取 params 参数
        params_data = request_model.params
        if params:
            params_data = params
        if params_data:
            kw['params'] = params_data

        self.request_data = kw

        self.logger.info(request_model.pretty_str())
        self.logger.info('Url: %s', url)
        res = requests.request(request_model.method, url, **kw)
        self.response_content = res.content
        return res

    def save(self):
        """保存请求配置"""
        print(self.response_path)
        with open(self.response_path, 'w') as f:
            save_data = json.dumps(json.loads(self.response_content), indent=4, ensure_ascii=False)
            f.write(save_data.encode('utf-8'))

        with open(self.request_path, 'w') as f:
            save_data = json.dumps(self.request_data, indent=4, ensure_ascii=False)
            f.write(save_data.encode('utf-8'))

    def open(self):
        #  """打开请求信息"""
        request_url = ("http://0.0.0.0:8801/api/detail?"
            "version={}&service_name={}&request_name={}").format(
                self.version, self.service_name, self.request_name
        )
        self.logger.info('open %s', request_url)
        os.system('open -a "/Applications/Google Chrome.app" "{}"'.format(
            request_url))
        pass

