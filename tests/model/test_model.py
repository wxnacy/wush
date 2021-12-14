#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
datatype 测试用例
"""
import pytest

from wush.model import datatype
from wush.model import Model

class User(Model):
    name = datatype.Str(default='wxnacy')

class Book(Model):
    __auto_format__ = True

    name = datatype.Str(default='wxnacy')

def test_init():

    u = User()
    assert u.name == None
    u.format()
    assert u.name == 'wxnacy'

    b = Book()
    assert b.name == 'wxnacy'
