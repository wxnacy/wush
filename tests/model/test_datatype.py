#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
datatype 测试用例
"""
import pytest

from wush.model import datatype

from wpy.base import BaseEnum

class TestEnum(BaseEnum):
    TEST1 = 'test1'
    TEST2 = 'test2'

class User(object):
    name = None

    def __init__(self, name=None):
        self.name = name


def test_init():

    with pytest.raises(ValueError) as e:
        datatype.Str(enum = object)
        assert str(e) == 'enum must be wpy.base.BaseEnum'

    # 测试 Object 没有设置默认值的情况
    assert datatype.Object().value() == None

    dt = datatype.Object(model=User)
    assert dt.value().name == None
    u = User(name = 'user')
    dt = datatype.Object(model=User, default=u)
    assert dt.value().name == u.name

def test_valid():

    value = ''
    dt = datatype.Dict()
    dt.set_value(value)
    with pytest.raises(ValueError) as excinfo:
        dt.valid()
        assert str(excinfo) == f"{value} is not be {dt._type}"

    dt = datatype.Str(enum = TestEnum)
    dt.set_value(value)
    with pytest.raises(ValueError) as e:
        dt.valid()
        assert str(e) == f'{value} is not {TestEnum}'

    dt = datatype.Object(model = User)
    dt.set_value(value)
    with pytest.raises(ValueError) as e:
        dt.valid()
        assert str(e) == f'{value} can not to {User}'

def test_value():
    dt = datatype.Str()
    assert dt.value() == ''

    value = { "name": "wxnacy" }
    dt = datatype.Object(model = User)
    dt.set_value(value)
    val = dt.value()
    assert isinstance(val, User)
    assert val.name == 'wxnacy'

    value = [{ "name": "wxnacy" }]
    dt = datatype.List(model = User)
    dt.set_value(value)
    val = dt.value()
    assert isinstance(val, list)
    assert val[0].name == 'wxnacy'

def test_convert():

    dt = datatype.Str(convert=True)
    dt.set_value(1)
    assert dt.value() == "1"

    dt = datatype.Int(convert=True)
    dt.set_value("1")
    assert dt.value() == 1

def test_get_base_datatype():
    assert datatype.DataType.get_base_datatype(str) == datatype.Str
    assert datatype.DataType.get_base_datatype(int) == datatype.Int

    with pytest.raises(ValueError) as e:
        datatype.DataType.get_base_datatype(User)
        assert str(e) == 'User is not basetype'
