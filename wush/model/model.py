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

    __column__ = {}

    def __init__(self, **kwargs):

        self._init_column()
        #  print(self.__column__)
        for k, v in self.__column__.items():
            if isinstance(v, DataType):
                v.set_value(kwargs.get(k))
                v.valid()
                setattr(self, k, v.value())

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

    #  def to_dict(self):
        #  data = {}
        #  for key in self.__column__.keys():
            #  data[key] = self.__dict__[key]
        #  return data

    #  def to_json(self):
        #  return json.dumps(self, default=lambda o: o.to_dict(), sort_keys=True)
