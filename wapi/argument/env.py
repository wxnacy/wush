#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
from argparse import Namespace
from collections import deque

from wapi.common.loggers import create_logger
from .decorates import argparser_register
from .parse import ArgumentNamespace
from .parse import ArgumentParser

class EnvArgumentNamespace(ArgumentNamespace):
    save = False
    pass

@argparser_register()
class EnvArgumentParser(ArgumentParser):
    cmd = 'env'

    def get_completions_after_cmd(self, argument, words=None):
        words = []
        for k ,v in self.wapi.config.env.dict().items():
            words.append(dict(text = '--' + k))
        return super().get_completions_after_cmd(argument, words)

    def set_wapi(self, client):
        self.wapi = client

    @property
    def _argument_namespace(self):
        return EnvArgumentNamespace

    def _make_args_dict(self, args):
        res = super()._make_args_dict(args)
        args = list(filter(lambda x: x != '--save', args))
        if len(args) < 3:
            return res
        # 将所有成对的参数都放入参数列表
        d_args = deque(args[1:])
        d_args.rotate(-1)
        for i, (k, v) in enumerate(zip(args[1:], d_args)):
            if i % 2  == 1 or not k.startswith('--'):
                continue
            k = k.replace('--', '')
            res[k] = v
        return res

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--save', action='store_true')
        return item

