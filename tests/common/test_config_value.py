#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

from wapi.common.config_value import ConfigValue

from wapi.common.functions import FunctionFactory

@FunctionFactory.register()
def test(a=None, b=None):
    return a, b

env_functions = FunctionFactory.get_factory()

def test_format_environ():
    """测试格式化环境变量"""
    text = '${test_wapi_name}'
    name = 'wxnacy'
    assert name == ConfigValue(text).set_env(test_wapi_name = name).format()

    text = '${test(3, "wxnacy")}'
    res = ConfigValue(text).set_functions(**env_functions).format()
    assert res == "(3, 'wxnacy')"

    text = '${test(3)}'
    res = ConfigValue(text).set_functions(**env_functions).format()
    assert res == '(3, None)'

    text = '${test()}'
    res = ConfigValue(text).set_functions(**env_functions).format()
    assert res == '(None, None)'
