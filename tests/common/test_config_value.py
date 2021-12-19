#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

from wush.common.config_value import ConfigValue
from wush.common.functions import FunctionFactory
from wush.config.models import EnvModel

from wush.model import datatype
from wush.model.model import Model



@FunctionFactory.register()
def test(a=None, b=None):
    return a, b

env_functions = FunctionFactory.get_factory()

class User(Model):
    name = datatype.Str()
    params = datatype.Dict()
    domains = datatype.List()

def test_format_model():
    u = User()
    u.name = '${test_name}'
    u.params = { "name": "${test_name}" }
    u.domains = [u.params]

    env_dict = EnvModel(test_name = 'wxnacy').to_dict()
    print(env_dict.get('test_name'))

    fu = ConfigValue(u).set_env(**env_dict).format()
    assert fu.name == 'wxnacy'
    assert fu.params.get("name") == 'wxnacy'
    assert fu.domains[0].get("name") == 'wxnacy'

def test_format_environ():
    """测试格式化环境变量"""
    text = '${test_name}'
    name = 'wxnacy'
    assert name == ConfigValue(text).set_env(test_name = name).format()

    text = '${test(3, "wxnacy")}'
    res = ConfigValue(text).set_functions(**env_functions).format()
    assert res == "(3, 'wxnacy')"

    text = '${test(3)}'
    res = ConfigValue(text).set_functions(**env_functions).format()
    assert res == '(3, None)'

    text = '${test()}'
    res = ConfigValue(text).set_functions(**env_functions).format()
    assert res == '(None, None)'
