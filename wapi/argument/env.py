#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
from argparse import Namespace
from collections import deque

from wapi.common.loggers import create_logger
from .parse import ArgumentNamespace
from .parse import ArgumentParser

class EnvArgumentNamespace(ArgumentNamespace):
    save = False
    pass

class EnvArgumentParser(ArgumentParser):
    cmd = 'env'

    def parse_args(self, args):
        args = args if isinstance(args, list) else args.split(" ")

        args_len = len(args)
        res = {}
        if args_len >= 1:
            res['cmd'] = args[0]

        if args_len < 3:
            return EnvArgumentNamespace(**res)

        d_args = deque(args[1:])
        d_args.rotate(-1)

        for i, (k, v) in enumerate(zip(args[1:], d_args)):
            if i % 2  == 1 or not k.startswith('--'):
                continue
            k = k.replace('--', '')
            res[k] = v

        return EnvArgumentNamespace(**res)

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--save', action='store_true')
        return item

