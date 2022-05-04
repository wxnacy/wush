#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com

import os
from wush.common.utils import get_current_module_path
from wush.config.config import Config
from wush.config.config import _get_config_path
from wush.config.models import ConfigModel
from wush.config.models import ModuleModel
from wush.config.models import RequestModel

os.environ['WUSH_MODULE'] = get_current_module_path()

test_config_path = 'tests/data/config/config.yml'

test_config = Config.load(test_config_path)
module_name = 'wush'
request_name = 'test_get'

def test_config_init():
    _config = ConfigModel()
    #  _config.format()
    assert _config.modules == []

def test_load():
    #  assert test_config._config_dir == 'tests/data/config'
    assert len(test_config._config.modules) == 4
    assert len(test_config.get_modules()) == 4
    #  assert test_config

def test_get_request():
    req = test_config.get_request(module_name, request_name)
    assert isinstance(req, RequestModel)
    assert req.url == 'http://localhost:6666/api/test'
    assert req.domain == 'localhost:6666'

    req_dict = req.dict()
    assert req_dict.get("params") == { "id": 12, 'home': os.getenv("HOME") }
    assert req_dict.get("json") == {}

    request = test_config.get_request('wush', 'test_post')
    assert request.name == 'test_post'
    req_dict = request.dict()
    assert req_dict.get("json") == { "id": 12 }
    assert req_dict.get("params") == {}

    req = test_config.get_request('wush', 'test_get')
    assert req.path == '/test'
    #  req.format()
    #  req.params.format()
    assert req.params.id.value == 12

    req_dict = req.params.dict()
    req_dict = req.dict()['params']
    assert req_dict['id'] == 12

    test_req = test_config.get_request(module_name, 'test')
    assert test_req.json_data.id.value == 12
    assert test_req.json_data.type.value == 0
    assert test_req.json_data.name.value == ''
    assert test_req.json_data.biz_id.value == 1234
    assert test_req.json_data.is_sync.value == False
    data = test_req.dict()
    assert data['json']['id'] == 12
    assert data['json']['type'] == 0
    assert data['json']['name'] == ''
    assert data['json']['biz_id'] == 1234
    assert data['json']['is_sync'] == False

def test_get_config_path():
    import os
    #  assert _get_config_path() == os.path.join(get_current_module_path(),
            #  'config/config.yml')

    _path = 'tests/data/config/config.yml'
    assert _get_config_path(_path) == _path


if __name__ == "__main__":
    test_get_request()
