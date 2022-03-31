#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
配置模型
"""
import os
#  from collections import defaultdict

from wpy.base import BaseObject

from wush.common.config_value import ConfigValue
from wush.common.constants import Constants
from wush.common.loggers import get_logger
from wush.model import datatype
from wush.model import Model
from wush.web.enums import MethodEnum
from wush.web.enums import ProtocolEnum

logger = get_logger('config.models')

class BaseModel(BaseObject):

    def inherit(self, super_ins, keys):
        """继承数据"""
        for key in keys:
            super_value = getattr(super_ins, key)
            sub_value = getattr(self, key)
            if not sub_value:
                setattr(self, key, super_value)
            else:
                # 字段结构进行拼接
                if isinstance(super_value, dict):
                    super_value = dict(super_value)
                    super_value.update(sub_value)
                # 列表结构进行拼接
                if isinstance(super_value, list):
                    super_value = list(super_value)
                    super_value.extend(sub_value)

                setattr(self, key, super_value)

class EnvModel(BaseObject):
    _default = None

    def __init__(self, **kwargs):
        # 将数字类型转为字符串
        for k, v in kwargs.items():
            for clz in (int, float):
                if isinstance(v, clz):
                    v = str(v)
            kwargs[k] = v
        #  for k, v in dict(os.environ).items():
            #  setattr(self, k, v)
        super().__init__(**kwargs)

    @classmethod
    def default(cls):
        """使用默认环境变量

        """
        _env = {}
        if not cls._default:
            cls._default = cls(**_env)
        return cls._default

class FieldModel(Model):
    """配置字段
    在配置中，单一值无法描述字段时，可以使用该模型
    """

    AUTO_FORMAT = True

    _doc = datatype.Str()
    _value = datatype.Object()
    _data_type = datatype.Object()

class AutoFieldModel(Model):
    """该模型自动使用 FieldModel"""
    AUTO_FORMAT = True
    DEFAULT_DATATYPE = datatype.Object(model = FieldModel)


    def __init__(self, **kwargs):
        """对数据进行前置过滤"""
        for k, v in kwargs.items():
            v = self._format_value(v)
            kwargs[k] = v

        super().__init__(**kwargs)

    def to_dict(self):
        """重载方法
        value 值只保留 _value 部分
        """
        logger.info('AutoFieldModel.to_dict')
        data = super().to_dict()
        for k, v in data.items():
            if isinstance(v, FieldModel):
                data[k] = v._value
            if isinstance(v, dict):
                data[k] = v.get("_value")
        return data

    def _format_value(self, v):
        if isinstance(v, dict) and '_value' in v:
            # 如果对象字段已经包含当前结构，进行格式转换
            data_type = v.get("_data_type", str)
            # 针对字符串转为基础类型
            if isinstance(data_type, str):
                data_type = Constants.str_to_basetype(data_type)
            v['_value'] = data_type(v['_value'])
        else:
            # 如果结构不对，则进行结构转换
            v = { "_value": v, "_data_type": type(v) }
        return v


class RequestModel(Model, BaseModel):
    """请求配置模型"""
    AUTO_FORMAT = True

    name = datatype.Str()
    title = datatype.Str()
    path = datatype.Str()
    method = datatype.Str(enum = MethodEnum, default=MethodEnum.GET.value,
        upper=True)
    protocol = datatype.Str()
    domain = datatype.Str()
    cookies = datatype.Dict()
    cookie_domains = datatype.List()                # 获取 cookie 的域名列表
    headers = datatype.Dict()
    json = datatype.Object(model=AutoFieldModel)
    params = datatype.Object(model=AutoFieldModel)
    data = datatype.Str()
    url = datatype.Str()

    def add_params(self, **kwargs):
        """添加 params 参数"""
        for k, v in kwargs.items():
            origin_value = None
            if hasattr(self.params, k):
                origin_value = getattr(self.params, k)
                v = origin_value._data_type(v)
            v = self.params._format_value(v)
            setattr(self.params, k, v)
        self.params.format()

    def add_json(self, **kwargs):
        """添加 params 参数"""
        for k, v in kwargs.items():
            origin_value = None
            if hasattr(self.json, k):
                origin_value = getattr(self.json, k)
                v = origin_value._data_type(v)
            v = self.json._format_value(v)
            setattr(self.json, k, v)
        self.json.format()


class ModuleModel(Model, BaseModel):
    AUTO_FORMAT = True

    name = datatype.Str()
    protocol = datatype.Str(enum = ProtocolEnum,
            default=ProtocolEnum.HTTP.value)
    domain = datatype.Str()
    url_prefix = datatype.Str()
    cookie_domains = datatype.List()                # 获取 cookie 的域名列表
    cookies = datatype.Dict()
    headers = datatype.Dict()
    requests = datatype.List(model=RequestModel)
    include = datatype.Str()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for req in self.requests:
            logger.info('test %s', req.to_dict())
        self.__req__ = {o.name: o for o in self.requests}

    def get_request(self, name):
        """获取 request 模型"""
        req = self.__req__.get(name)
        if req:
            # 继承 module 的字段
            inherit_keys = ('protocol', 'domain', 'cookies', 'headers',
                'cookie_domains')
            req.inherit(self, inherit_keys)

            # 拼装 url
            if not req.url:
                req.url = f'{req.protocol}://{req.domain}' \
                    f'{self.url_prefix}{req.path}'
        return req

class ConfigModel(Model):
    """客户端全局配置模型"""
    __all__ = ['api_history_dir','server_port', 'server_host']

    modules = datatype.List(model = ModuleModel)
    env = datatype.Object(model = EnvModel)
    cookies = datatype.Dict()
    headers = datatype.Dict()
    modules_include = datatype.List()
    function_modules = datatype.List()
    server_port = datatype.Str(default = Constants.SERVER_PORT)
    server_host = datatype.Str(default = Constants.SERVER_HOST)
    api_history_dir = datatype.Str(default = Constants.API_HISTORY_DIR)

    def format(self):
        """重载 format
        先进行 modules 处理
        """
        super().format()
        # 对变量进行格式化
        default_env = EnvModel.default()
        for i, _module in enumerate(self.function_modules):
            self.function_modules[i] = ConfigValue(_module
                ).set_env(**default_env.to_dict()).format()
        #  ConfigValue(self).format()
        self.__mod__ = {o.name: o for o in self.modules}

    def get_module(self, name):
        """获取模块"""
        if not self.__is_format__:
            raise Exception('ConfigModel must format first')
        module = self.__mod__.get(name)
        if module:
            inherit_keys = ['headers', 'cookies']
            module.inherit(self, inherit_keys)

        return module

    @classmethod
    def _iter_path(cls, filepath):
        """迭代地址"""
        if os.path.isfile(filepath):
            yield filepath
        if os.path.isdir(filepath):
            names = os.listdir(filepath)
            for _dir, _, names in os.walk(filepath):
                for name in names:
                    yield os.path.join(_dir, name)
        yield None

    def iter_module_path(self):
        """迭代模块地址列表"""
        for module_path in self.modules_include or []:
            for path in self._iter_path(module_path):
                if not path:
                    continue
                # 过滤掉不是 yml 结尾的配置文件
                if not path.endswith('.yml'):
                    continue
                yield path

