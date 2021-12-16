#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
datatype 测试用例
"""
import pytest

from wush.model import datatype
from wush.model import Model

class User(Model):
    name = datatype.Str(default='wxnacy')

class Book(Model):
    AUTO_FORMAT = True
    DB = 'table'

    name = datatype.Str(default='wxnacy')
    age = None

class Field(Model):
    doc = datatype.Str()
    _type = datatype.Object()
    value = datatype.Object()

class Json(Model):
    DEFAULT_FIELD_MODEL = Field


def test_init():

    u = User()
    assert u.name == None
    u.format()
    assert u.name == 'wxnacy'

    b = Book()
    assert b.name == 'wxnacy'

def test_to_dict():
    b = Book()
    b.age = 1
    b.NAME = 'w'
    b.DB = 'w'
    data = b.to_dict()
    assert 'AUTO_FORMAT' not in data
    assert 'age' not in data
    assert len(data) == 1

    import json
    data = json.loads(b.to_json())
    assert 'AUTO_FORMAT' not in data
    assert 'age' not in data
    assert len(data) == 1

    m = Json()
    m.name = { "value": "wxnacy", "_type": str }
    m.format()
    data = m.to_dict()
    assert data['name']['value'] == 'wxnacy'
    assert data['name']['_type'] == str


def test_format():
    u = User()
    u.name = 1
    with pytest.raises(ValueError):
        u.format()

def test_default_field_model():
    m = Json()
    m.name = { "value": "wxnacy", "_type": str }
    m.format()
    assert m.name.value == 'wxnacy'
    assert m.name._type == str

