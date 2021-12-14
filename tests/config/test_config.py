#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com

from wush.config.config import Config
from wush.config.models import ConfigModel
from wush.config.models import ModuleModel
from wush.config.models import RequestModel

test_config_path = 'tests/data/config/config.yml'

test_config = Config.load(test_config_path)
module_name = 'wush'
request_name = 'test_get'

def test_load():
    test_config._config_dir == 'tests/data/config'


def test_get_request():
    req = test_config.get_request(module_name, request_name)
    assert isinstance(req, RequestModel)
    assert req.url == 'http://localhost:6060/api/test'
    assert req.domain == 'localhost:6060'
