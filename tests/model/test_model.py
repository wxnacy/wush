#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
datatype 测试用例
"""
import pytest

from wush.model import datatype
from wush.model import Model

class Book(Model):
    AUTO_FORMAT = True
    DB = 'table'

    name = datatype.Str(default='wxnacy')
    age = None

class User(Model):
    name = datatype.Str(default='wxnacy')
    book = datatype.Object(model=Book)


class Field(Model):
    doc = datatype.Str()
    _type = datatype.Object()
    value = datatype.Object()

class Json(Model):
    DEFAULT_FIELD_MODEL = Field

class Request(Model):
    json = datatype.Object(model=Json)


def test_init():

    u = User()
    assert u.name == None
    u.format()
    assert u.name == 'wxnacy'
    u.name = 'wen'
    assert u.name == 'wen'

    b = Book()
    assert b.name == 'wxnacy'

    # 重复执行 防止类维度数据导致 bug
    u = User()
    assert u.name == None
    u.format()
    assert u.name == 'wxnacy'
    u.name = 'wen'
    assert u.name == 'wen'

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

    u = User()
    u.book = { "age": 1 }
    u.format()
    assert u.book.age == 1
    assert u.book.name == "wxnacy"

def test_default_field_model():
    m = Json()
    m.name = { "value": "wxnacy", "_type": str }
    m.format()
    assert m.name.value == 'wxnacy'
    assert m.name._type == str

    data = { "json": { "id": { "_value": 1 }, "name": { "_value": "wxnacy" } } }
    r = Request(**data)
    r.format()
    assert r.json.id._value == 1
    assert r.json.name._value == 'wxnacy'

#  if __name__ == "__main__":
    #  test_default_field_model()
