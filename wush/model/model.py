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

    def __init__(self, **kwargs):
        self.__init_datatype_fields()
        super().__init__(**kwargs)

        # 将未赋值的字段设置为 None
        for key in self.__get_datatype_fields().keys():
            if isinstance(getattr(self, key), DataType):
                setattr(self, key, None)

        # 判断自动 format
        if self.AUTO_FORMAT:
            self.format()

    def __setattr__(self, key, value):
        """重载设置值的方法"""
        # 如果字段的默认模型存在，则设置值之前先添加 datatype
        if self.DEFAULT_FIELD_MODEL:
            self.__add_datatype_fields(
                **{ key: Object(model=self.DEFAULT_FIELD_MODEL) })

        super().__setattr__(key, value)

    @classmethod
    def __add_datatype_fields(cls, **kwargs):
        """添加 datatype 字段"""
        for k, v in kwargs.items():
            if not isinstance(v, DataType):
                continue
            if k not in cls.__datatype_fields__[cls.__name__]:
                cls.__datatype_fields__[cls.__name__][k] = v

    @classmethod
    def __get_datatype_fields(cls):
        """获取 datatype 字段"""
        return cls.__datatype_fields__.get(cls.__name__, {})

    @classmethod
    def __init_datatype_fields(cls):
        '''获取默认 dict'''
        classes = [cls]
        # 兼容父类的 __dict__
        #  classes.extend(cls.__bases__)
        for clz in classes:
            cls.__add_datatype_fields(**clz.__dict__)

    def format(self):
        for k, v in self.__get_datatype_fields().items():
            if isinstance(v, DataType):
                try:
                    v.set_value(getattr(self, k))
                except:
                    pass
                v.valid()
                setattr(self, k, v.value())

    def to_dict(self):
        """
        将实例转为 dict 数据
        执行前需要保证实例已经执行过 format 方法或设置成员变量 AUTO_FORMAT=True
        """
        data = {}
        for key in self.__get_datatype_fields().keys():
            data[key] = getattr(self, key)
        return data

    def to_json(self):
        return json.dumps(self, default=lambda o: o.to_dict(), sort_keys=True)

class User(Model):
    name = None

if __name__ == "__main__":
    u = User()
    u.name = 'wxnacy'
    print(u.name)
    
