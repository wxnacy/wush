#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com

import os
import pytest
from wush.config.models import AutoFieldModel
from wush.config.config import Config
from wush.config.models import ConfigModel
from wush.config.models import ModuleModel
from wush.config.models import RequestModel
from wush.config.models import FieldModel


def test_field_model():
    field = FieldModel(_data_type = '')
    assert field.data_type == str

    field = FieldModel(_value = 1)
    assert field.data_type == int
    assert field.value == 1

    field = FieldModel(_doc="test", _value="1", _data_type = int)
    assert field.doc == 'test'
    assert field.value == 1
    assert field.data_type == int

    field = FieldModel(_value=1, _data_type = str)
    assert field.value == '1'
    assert field.data_type == str

    field = FieldModel(_value=1, _data_type = 'str')
    assert field.value == '1'
    assert field.data_type == str

    field = FieldModel(_value='["a", "b"]', _data_type = str)
    assert field.value == '["a", "b"]'

    field = FieldModel(_value='["a", "b"]', _data_type = list)
    assert field.value == ["a", "b"]

    field = FieldModel(_value='{"name": "value"}', _data_type = 'dict')
    assert field.value == {"name": "value"}

    with pytest.raises(ValueError):
        field = FieldModel(_value='{"name": "value"}s', _data_type = 'dict')


def test_auto_field():
    data = { "json": {
        "name": "wxnacy",
        "age": { "_value": "1", "_data_type": int },
        "page": { "_value": "1", "_data_type": 'int' }
        } }

    af = AutoFieldModel(**data['json'])
    assert af.name.value == 'wxnacy'
    assert af.age.value == 1
    assert af.page.value == 1

    af.id = 1
    assert af.id.value == 1

    af.pagesize = { "_value": 10 }
    assert af.pagesize.value == 10

    dict_data = af.dict()
    assert dict_data.get("name") == 'wxnacy'
    assert dict_data.get("age") == 1
    assert dict_data.get("page") == 1
    assert dict_data.get("id") == 1
    assert dict_data.get("pagesize") == 10

test_config_path = 'tests/data/config/config.yml'
config = Config.load(test_config_path)
_config = config._config

def test_config_model():
    item = ConfigModel(
            env = { "name": "wxnacy" },
            function_modules = ['${HOME}/test'],
    )
    assert item.env.name == 'wxnacy'
    assert item.function_modules[0] == os.path.join(os.getenv("HOME"), 'test')

    config = Config.load(test_config_path)
    config = config._config

    assert type(config.modules) == list
    module = config.modules[0]
    assert isinstance(module, ModuleModel)

    assert config.get_module('678') == None

    module = config.get_module('wush')
    assert module.name == 'wush'
    assert type(module.requests) == list
    assert module.cookies.get("config_name") == 'test'
    assert module.cookies.get("module_name") == 'test'
    assert len(module.cookie_domains) == 2

    request = module.requests[0]
    assert isinstance(request, RequestModel)
    assert request.name == 'test_get'
    assert request.path == '/test'

    assert module.get_request('65432') == None
    req = module.get_request('test_get')
    assert req.path == '/test'
    assert req.url == 'http://localhost:${WUSH_PORT}/api/test'
    #  assert req.url == 'http://localhost:6060/api/test'
    #  assert req.params.id == 12
    #  assert req.params.name == os.getenv("HOME")

def test_module_model():
    with pytest.raises(ValueError):
        ModuleModel(name = 'test', protocol='test')

def test_request_model():
    with pytest.raises(ValueError):
        RequestModel(name = 'test', protocol='test')

    with pytest.raises(ValueError):
        RequestModel(name = 'test', method='test')

    item = RequestModel(name = 'test', url='test')
    assert item.url == 'test'

    item.add_params(name = 'test')
    assert item.params.name.value == 'test'

    item.add_json(name = 'test')
    assert item.json_data.name.value == 'test'

#  def test_get_request():
    #  request = config.get_request('wush', 'test_get')
    #  assert isinstance(request, RequestModel)

    #  assert request.name == 'test_get'
    #  assert request.path == '/test'
    #  req_dict = request.dict()
    #  assert req_dict.get("params") == { "id": 12, 'home': os.getenv("HOME") }
    #  assert req_dict.get("json") == {}

    #  request = config.get_request('wush', 'test_post')
    #  assert request.name == 'test_post'
    #  req_dict = request.dict()
    #  assert req_dict.get("json") == { "id": 12 }
    #  assert req_dict.get("params") == {}
