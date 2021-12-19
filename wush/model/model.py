#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
基础模块
"""
import json
from collections import defaultdict

from wpy.base import BaseObject
from wush.model.datatype import DataType
from wush.model.datatype import Object

__FILTER_SET_FIELDS__ = set(('AUTO_FORMAT', 'DEFAULT_DATATYPE',
    '__is_format__', '__datatype_fields__'))

class Model(BaseObject):

    AUTO_FORMAT = False     # 是否自动 format
    # 字段默认的 datatype
    DEFAULT_DATATYPE = None

    # 装载 Model 的 datatype 类型字段
    __datatype_fields__ = defaultdict(dict)
    # 对象是否已经进行过 format 操作
    __is_format__ = False

    def __init__(self, **kwargs):
        #  self.__is_format__ = False
        self.__init_datatype_fields()
        super().__init__(**kwargs)

        # 将未赋值的字段设置为 None
        for key in self.__get_datatype_fields().keys():
            if hasattr(self, key) and isinstance(getattr(self, key), DataType):
                setattr(self, key, None)

        # 判断自动 format
        if self.AUTO_FORMAT:
            self.format()

    def __is_need_format_setattr__(self, key, value):
        """是否需要格式化 __setattr__"""
        if not self.DEFAULT_DATATYPE:
            return False
        if key in __FILTER_SET_FIELDS__:
            return False

        return True

    def __setattr__(self, key, value):
        #  """重载设置值的方法"""
        # 如果字段的默认模型存在，则设置值之前先添加 datatype
        if self.DEFAULT_DATATYPE:
            default_datatype = self.__build_default_datatype()
            self.__add_datatype_fields(**{ key: default_datatype })

        super().__setattr__(key, value)

    @classmethod
    def __add_datatype_fields(cls, **kwargs):
        """添加 datatype 字段"""
        for k, v in kwargs.items():
            if k in __FILTER_SET_FIELDS__:
                continue
            if not isinstance(v, DataType):
                continue
            # 设置 datatype 名称
            v._name = k
            if k not in cls.__datatype_fields__[cls]:
                cls.__datatype_fields__[cls][k] = v

    @classmethod
    def __get_datatype_fields(cls):
        """获取 datatype 字段"""
        return cls.__datatype_fields__.get(cls, {})

    @classmethod
    def __init_datatype_fields(cls):
        '''获取默认 dict'''
        classes = [cls]
        # 兼容父类的 __dict__
        #  classes.extend(cls.__bases__)
        for clz in classes:
            cls.__add_datatype_fields(**clz.__dict__)

    def __build_default_datatype(self):
        """构建默认的 datatype"""
        return self.DEFAULT_DATATYPE

    def format(self):
        """将 datatype 字段进行格式化处理"""
        self._format(self)

    def _format(self, model):
        """嵌套 format"""
        # 判断是否有默认字段
        # 并对对象中存在的赋值添加到 __datatype_fields__ 中
        if model.DEFAULT_DATATYPE:
            for key in model.__dict__.keys():
                # 符合条件的 key 才会进行添加 datatype 处理
                default_datatype = model.__build_default_datatype()
                model.__add_datatype_fields(**{key: default_datatype })

        for k, v in model.__get_datatype_fields().items():
            # 格式化单个字段
            self._format_field(model, k)

        model.__is_format__ = True

    def _format_field(self, model, field):
        """格式化 field"""
        # 如果 field 不是 datatype 类型，直接返回
        datatype_fields = model.__get_datatype_fields()
        dt_ins = datatype_fields.get(field)
        if not dt_ins:
            return

        try:
            dt_ins.set_value(getattr(model, field))
        except:
            pass
        # 校验
        dt_ins.valid()
        set_val = dt_ins.value()
        setattr(model, field, set_val)
        # 嵌套 format
        if isinstance(set_val, Model):
            #  self._format(set_val)
            set_val.format()

    def to_dict(self):
        """
        将实例转为 dict 数据
        执行前需要保证实例已经执行过 format 方法或设置成员变量 AUTO_FORMAT=True
        """
        return self._to_dict(self)

    @classmethod
    def _to_dict(cls, model):
        """对 Model 进行循环 to_dict 操作"""
        data = {}
        for key in model.__get_datatype_fields().keys():
            if not hasattr(model, key):
                continue
            origin_value = getattr(model, key)
            if isinstance(origin_value, Model):
                data[key] = origin_value.to_dict()
            else:
                data[key] = origin_value
        return data

    def to_json(self):
        return json.dumps(self, default=lambda o: o.to_dict(), sort_keys=True)

from wush.model import datatype
class Book(Model):
    name = datatype.Str(default='book')

class User(Model):
    AUTO_FORMAT = True
    DEFAULT_DATATYPE = Object(model = Book)
    #  DEFAULT_DATATYPE = Book
    #  book = datatype.Str()

class Field(Model):
    doc = datatype.Str()
    _type = datatype.Object()
    value = datatype.Object()

class Json(Model):
    DEFAULT_DATATYPE = datatype.Object(model = Field)

    cust_field = datatype.Str(default='cust')

class Request(Model):
    json = datatype.Object(model=Json)

if __name__ == "__main__":

    #  u = User()
    #  u.name = { "name": 'wxnacy' }
    #  u.format()
    #  assert u.name.name == 'wxnacy'

    #  b = Book()
    #  b.format()
    #  b.name = 'books'
    #  u = User()
    #  u.name = 'wxnacy'
    
    data = { "json": { "id": { "_value": 1 }, "name": { "_value": "wxnacy" } } }
    r = Request(**data)
    r.format()
    assert r.json.id._value == 1
    assert r.json.name._value == 'wxnacy'
    # 手动设置的字段，使用原类型
    assert r.json.cust_field == 'cust'
