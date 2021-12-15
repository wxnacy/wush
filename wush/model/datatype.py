#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
基础模块
"""

from wpy.base import BaseObject
from wpy.base import BaseEnum

# TODO 改为抽象类
class DataType(BaseObject):
    _value = None
    _type = object
    _default = None

    default = None

    def set_value(self, value):
        self._value = value

    def value(self):
        """获取数据"""
        val = str(self.default()) if callable(self.default) else self.default
        return self._value or val or self._default

    def valid(self):
        """校验赋值"""
        if self._value != None and not isinstance(self._value, self._type):
            raise ValueError(f'{self._value} is not be {self._type}')

class Str(DataType):
    _type = str
    _default = str()

    enum = None
    upper = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.enum and not issubclass(self.enum, BaseEnum):
            raise ValueError('enum must be wpy.base.BaseEnum')

    def set_value(self, value):
        super().set_value(value)
        if self.upper and self._value:
            self._value = self._value.upper()

    def valid(self):
        super().valid()
        if self.enum and self._value != None and \
                self._value not in self.enum.values():
            raise ValueError(f'{self._value} is not {self.enum}')


class Dict(DataType):
    _type = dict
    _default = dict()


class List(DataType):
    _type = list
    _default = list()

    model = None

    def value(self):
        """获取数据"""
        if self.model and self._value:
            items = []
            for item in self._value:
                items.append(self.model(**item))
            return items

        return super().value()

class Object(DataType):
    _type = object

    model = None

    def valid(self):
        """校验"""
        if self._value != None and not isinstance(self._value, dict
                ) and self.model:
            raise ValueError(f'{self._value} can not to {self.model}')

    def value(self):
        """获取数据"""
        if self.model and self._value:
            return self.model(**self._value)

        return super().value()
