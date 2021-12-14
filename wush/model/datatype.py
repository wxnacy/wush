#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
基础模块
"""

from wpy.base import BaseObject
from wpy.base import BaseEnum

class DataType(BaseObject):
    default = None
    _value = None
    _type = object

    def set_value(self, value):
        print(self, value)
        self._value = value

    @property
    def emtry_value(self):
        return None

    def value(self):
        """获取数据"""
        val = str(self.default()) if callable(self.default) else self.default
        return self._value or val or self.emtry_value

    def valid(self):
        """校验赋值"""
        if self._value and not isinstance(self._value, self._type):
            raise ValueError(f'{self._value} is not be {self._type}')

class Str(DataType):
    enum = None
    upper = False
    _type = str

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.enum and not issubclass(self.enum, BaseEnum):
            raise ValueError('enum must be BaseEnum')

    def set_value(self, value):
        super().set_value(value)
        if self.upper and self._value:
            self._value = self._value.upper()

    @property
    def emtry_value(self):
        return ""

    def valid(self):
        super().valid()
        if self.enum and self._value and self._value not in self.enum.values():
            raise ValueError(f'{self._value} is a error value for {self.enum}')


class Dict(DataType):
    _type = dict

    #  def valid(self):
        #  if self._value and not isinstance(self._value, dict):
            #  raise ValueError(f'{self._value} is not dict')

    @property
    def emtry_value(self):
        return {}

class List(DataType):
    _type = list
    model = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def emtry_value(self):
        return []

    #  def valid(self):
        #  if self._value and not isinstance(self._value, list):
            #  raise ValueError(f'{self._value} is not list')

    def value(self):
        """获取数据"""
        if self.model and self._value:
            items = []
            for item in self._value:
                items.append(self.model(**item))
            return items

        return super().value()

