#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: 371032668@qq.com
"""

"""

import os
from wapi import Wapi
from wapi.common import constants
from wapi.common.config import Config

default_config = Config.get_default_config()
test_space_name = 'test_space'
test_module_name = 'test_module'
test_request_name = 'test_request'
test_config_root = './tests/data/config'

def test_init_config():
    client = Wapi(config_root = test_config_root)

    assert client.space_name == constants.DEFAULT_SPACE_NAME
    assert client.module_name == constants.DEFAULT_MODULE_NAME

    assert client.config.body_root == client.config.fmt_path(
            default_config.get("body_root"))
    assert client.config.env_root == client.config.fmt_path(
            default_config.get("env_root"))
    assert client.config.module_root == client.config.fmt_path('test_module')
    assert client.config.response_root == os.path.expanduser(
            default_config.get("response_root"))

    test_config = {
        "body_root": "test_body",
        "env_root": "test_env",
        "env_root": "test_env",
    }
    kwargs = {
        "space_name": test_space_name,
        "module_name": test_module_name,
        "request_name": test_request_name,
        "config": {

        }
    }
    client.init_config(**kwargs)
    assert client.space_name == 'default'
    assert client.module_name == kwargs['module_name']
    assert client.request_name == kwargs['request_name']

    client.is_dynamic_space = False

    kwargs = {
        "space_name": test_space_name,
    }
    client.init_config(**kwargs)
    assert client.space_name == kwargs['space_name']

def test_get_request():
    """测试 get_request"""

    client = Wapi(
        request_name = 'get_test',
        config_root = test_config_root,
    )
    request_model = client._get_request(module_name = 'default',
            request_name = 'get_test',
            env = { "name": 'env_test' })
    assert request_model.name == 'get_test'
    assert request_model.path == '/get_test'
    assert request_model.params['name'] == 'get_test'
    assert request_model.env['name'] == 'env_test'


