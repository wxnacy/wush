#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
网络相关枚举模块
"""

from wpy.base import BaseEnum

class HeaderEnum(BaseEnum):
    CONTENT_TYPE = 'Content-Type'

class ContentTypeEnum(BaseEnum):
    APPLICATION_JSON = 'application/json'
