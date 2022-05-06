#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

from wush.common.config_value import ConfigValue
from wush.common.config_value import environ_keys
from wush.config.function import FunctionFactory
from wush.config.models import EnvModel


@FunctionFactory.register()
def test(a=None, b=None):
    return a, b

env_functions = FunctionFactory.get_factory()


def test_format_model():

    env_dict = EnvModel(test_name = 'wxnacy').to_dict()
    print(env_dict.get('test_name'))


class ObjectClass:
    name: str = "${name}"

def test_format_object():
    ins = ObjectClass()
    ins = ConfigValue(ins).set_env(name = 'test').format()
    assert ins.name == 'test'

def test_format_environ():
    """测试格式化环境变量"""
    text = '${test_name}'
    name = 'wxnacy'
    assert name == ConfigValue(text).set_env(test_name = name).format()

    #  text = '{test_name}'
    #  name = 'wxnacy'
    #  assert name == ConfigValue(text).set_env(test_name = name).format()

    text = '${test(3, "wxnacy")}'
    res = ConfigValue(text).set_functions(**env_functions).format()
    assert res == "(3, 'wxnacy')"

    #  text = '{test(3, "wxnacy")}'
    #  res = ConfigValue(text).set_functions(**env_functions).format()
    #  assert res == "(3, 'wxnacy')"

    text = '${test(3)}'
    res = ConfigValue(text).set_functions(**env_functions).format()
    assert res == '(3, None)'

    #  text = '{test(3)}'
    #  res = ConfigValue(text).set_functions(**env_functions).format()
    #  assert res == '(3, None)'

    text = '${test()}'
    res = ConfigValue(text).set_functions(**env_functions).format()
    assert res == '(None, None)'

def test_environ_keys():
    text = '${name} ${test()} ${name}'
    keys = environ_keys(text)
    assert keys == {'name', 'test()'}

    data = {
            '${name}': '${value}',
            'data': {
                "name": "${test()}"
            },
            'list': [
                '${name}',
                '${id}',
                ]
            }
    keys = environ_keys(data)
    assert keys == {'name', 'value', 'test()', 'id'}


    ins = ObjectClass()
    assert environ_keys(ins) == { 'name' }

def test_parse_type():
    text_value = {"name": "wxnacy"}
    text = 'json@${text_value}'
    data = ConfigValue(text).set_env(text_value = text_value).format()
    assert data == {"name": "wxnacy"}
