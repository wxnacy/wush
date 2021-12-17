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

class Model(BaseObject):

    AUTO_FORMAT = False     # 是否自动 format
    DEFAULT_FIELD_MODEL = None    # 字段的默认类型

    # 装载 Model 的 datatype 类型字段
    __datatype_fields__ = defaultdict(dict)
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
        if not self.DEFAULT_FIELD_MODEL:
            return False
        if key in ('__is_format__', '__datatype_fields__', 'AUTO_FORMAT',
                'DEFAULT_FIELD_MODEL'):
            return False

        return True

    def __setattr__(self, key, value):
        """重载设置值的方法"""
        # 如果字段的默认模型存在，则设置值之前先添加 datatype
        if self.__is_need_format_setattr__(key, value):
            self.__add_datatype_fields(
                **{ key: Object(model=self.DEFAULT_FIELD_MODEL) })

        super().__setattr__(key, value)

    @classmethod
    def __add_datatype_fields(cls, **kwargs):
        """添加 datatype 字段"""
        for k, v in kwargs.items():
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

    def format(self):
        """将 datatype 字段进行格式化处理"""
        self._format(self)

    def _format(self, model):
        """嵌套 format"""
        # 判断是否为 DEFAULT_FIELD_MODEL
        # 并对对象中存在的赋值添加到 __datatype_fields__ 中
        if self.DEFAULT_FIELD_MODEL:
            for key in self.__dict__.keys():
                self.__add_datatype_fields(**{
                    key: Object(model=self.DEFAULT_FIELD_MODEL) })

        for k, v in model.__get_datatype_fields().items():
            if isinstance(v, DataType):
                try:
                    v.set_value(getattr(model, k))
                except:
                    pass
                # 执行数据校验
                v.valid()
                set_val = v.value()
                setattr(model, k, set_val)
                # 嵌套 format
                if isinstance(set_val, Model):
                    self._format(set_val)

        model.__is_format__ = True

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
        #  print(model.__class__.__name__, model.__get_datatype_fields())
        for key in model.__get_datatype_fields().keys():
            if not hasattr(model, key):
                continue
            origin_value = getattr(model, key)
            if isinstance(origin_value, Model):
                data[key] = cls._to_dict(origin_value)
            else:
                data[key] = origin_value
        return data

    def to_json(self):
        return json.dumps(self, default=lambda o: o.to_dict(), sort_keys=True)

#  from wush.model import datatype
#  class Book(Model):
    #  name = datatype.Str(default='book')

#  class User(Model):
    #  AUTO_FORMAT = True
    #  book = datatype.Str()

#  if __name__ == "__main__":

    #  u = User()
    #  u.name = ''
    #  u.format()

    #  b = Book()
    #  b.format()
    #  print(b.name)
    #  b.name = 'books'
    #  print(b.name)
    #  #  u = User()
    #  #  u.name = 'wxnacy'
    #  #  print(u.name)
    
