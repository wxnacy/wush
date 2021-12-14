#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
基础模块
"""
import json

from wpy.base import BaseObject
from wush.model.datatype import DataType

class Model(BaseObject):

    __auto_format__ = False
    __column__ = {}

    def __init__(self, **kwargs):
        self._init_column()
        super().__init__(**kwargs)

        # 将未赋值的字段设置为 None
        for key in self.__column__.keys():
            if isinstance(getattr(self, key), DataType):
                setattr(self, key, None)

        if self.__auto_format__:
            self.format()

    @classmethod
    def _init_column(cls):
        '''获取默认 dict'''
        cls.__column__ = {}
        classes = [cls]
        # 兼容父类的 __dict__
        #  classes.extend(cls.__bases__)
        for clz in classes:
            for k, v in clz.__dict__.items():
                if isinstance(v, DataType):
                    cls.__column__[k] = v

    def format(self):
        for k, v in self.__column__.items():
            if isinstance(v, DataType):
                try:
                    v.set_value(getattr(self, k))
                except:
                    pass
                v.valid()
                setattr(self, k, v.value())



    #  def to_dict(self):
        #  data = {}
        #  for key in self.__column__.keys():
            #  data[key] = self.__dict__[key]
        #  return data

    #  def to_json(self):
        #  return json.dumps(self, default=lambda o: o.to_dict(), sort_keys=True)
