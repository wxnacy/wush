#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
基础模块
"""

from wpy.base import BaseObject

class DataType(object):
    pass

class List(DataType):
    datatype = None
    def __init__(self, datatype):
        self.datatype = datatype

    def value(self):
        #  return self.datatype()
        return []

    def conver(self, data):
        items = []
        for item in data:
            items.append(self.datatype(**item))
        return items

class ModelColumn(BaseObject):
    datatype = None
    default = None

    def __init__(self, datatype, **kwargs):
        super().__init__(**kwargs)
        self.datatype = datatype

    def value(self):
        """获取数据"""
        val = str(self.default()) if callable(self.default) else self.default
        if not val:
            if isinstance(self.datatype, DataType):
                if callable(self.datatype):
                    val = self.datatype()
                else:
                    val = self.datatype.value()
            else:
                val = self.datatype()
        return val

class BaseModel(BaseObject):

    __column__ = {}

    def __init__(self, **kwargs):
        init_data = self.__default_dict__()
        init_data.update(kwargs)
        for k, v in init_data.items():
            setattr(self, k, v)
        self.format()

    @classmethod
    def __default_dict__(cls):
        '''获取默认 dict'''
        res = {}
        classes = [cls]
        # 兼容父类的 __dict__
        classes.extend(cls.__bases__)
        for clz in classes:
            for k, v in clz.__dict__.items():
                if isinstance(v, ModelColumn):
                    cls.__column__[k] = v
                    res[k] = v.value()
        return res

    def format(self):
        for key, column in self.__column__.items():
            if isinstance(column.datatype, DataType):
                value = column.datatype.conver(getattr(self, key))
                setattr(self, key, value)
            print(key, getattr(self, key))

