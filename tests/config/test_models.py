#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com

from wush.config.config import Config
from wush.config.models import ConfigModel
from wush.config.models import ModuleModel
from wush.config.models import RequestModel

test_config_path = 'tests/data/config/config.yml'

def test_format():
    config = Config.load(test_config_path)
    config = config._config

    assert type(config.modules) == list
    module = config.modules[0]
    assert isinstance(module, ModuleModel)

    assert config.get_module('678') == None
    module = config.get_module('wush')
    assert module.name == 'wush'
    assert type(module.requests) == list
    request = module.requests[0]
    assert isinstance(request, RequestModel)
    assert request.name == 'test_get'
    assert request.path == '/test'

    assert module.get_request('65432') == None
    req = module.get_request('test_get')
    assert req.url == 'http://localhost:6060/api/test'
    assert req.domain == 'localhost:6060'
    assert req.path == '/test'
