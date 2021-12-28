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


def test_init():

    u = User()
    assert u.name == None
    u.format()
    assert u.name == 'wxnacy'
    u.name = 'wen'
    assert u.name == 'wen'

    b = Book()
    assert b.name == 'wxnacy'
    #  with pytest.raises(ValueError):
        #  b.name = 1

    # 重复执行 防止类维度数据导致 bug
    u = User()
    assert u.name == None
    u.format()
    assert u.name == 'wxnacy'
    u.name = 'wen'
    assert u.name == 'wen'

class Field(Model):
    doc = datatype.Str()
    _type = datatype.Object()
    value = datatype.Object()

class Json(Model):
    DEFAULT_DATATYPE = datatype.Object(model = Field)

    cust_field = datatype.Str(default='cust')

class Request(Model):
    json = datatype.Object(model=Json)


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

class DefaultDatatype(Model):
    DEFAULT_DATATYPE = datatype.Str(convert=True)


def test_default_datatype():
    m = Json()
    m.name = { "value": "wxnacy", "_type": str }
    m.format()
    assert m.name.value == 'wxnacy'
    assert m.name._type == str

    data = { "json": { "id": { "value": 1 }, "name": { "value": "wxnacy" } } }
    r = Request(**data)
    r.format()
    assert r.json.id.value == 1
    assert r.json.name.value == 'wxnacy'
    # 手动设置的字段，使用原类型
    assert r.json.cust_field == 'cust'

    req_dict = r.to_dict()
    assert req_dict['json']['id']['value'] == 1

    # 测试 datatype 类型
    dd = DefaultDatatype()
    dd.name = 1
    dd.format()
    assert dd.name == '1'

    data = { "id": { "value": 12, "_type": int } }
    m2 = Json( **data )
    #  m2.id = { "value": 12, "_type": int }
    m2.format()
    assert m2.dict() == { "id": {  "value": 12, "_type": int, 'doc': '' } ,
            "cust_field": "cust"}



class InitTwo(Model):
    AUTO_FORMAT = True

    params = datatype.Dict()
    json = datatype.Dict()

class InitTwoGroup(Model):
    AUTO_FORMAT = True

    init_two = datatype.List(model = InitTwo)

def test_format_field():

    item = InitTwo(params = {"id": 12})
    assert item.params == {"id": 12}
    assert item.json == {}

    item = InitTwo(json = {"id": 12})
    assert item.json == {"id": 12}
    assert item.params == {}

    data = [
            { "params": { "id": 12 } },
            { "json": { "id": 12 } },
            ]
    item_group = InitTwoGroup(init_two = data)
    assert item_group.init_two[0].params == {"id": 12}
    assert item_group.init_two[0].json == {}

    assert item_group.init_two[1].json == {"id": 12}
    assert item_group.init_two[1].params == {}

if __name__ == "__main__":
    test_default_datatype()
