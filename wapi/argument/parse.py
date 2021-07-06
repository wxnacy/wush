#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
from argparse import Namespace
from collections import deque
from enum import Enum

from wapi.common.loggers import create_logger

class Action(Enum):
    STORE = 'store'
    STORE_TRUE = 'store_true'

class ArgumentNamespace(Namespace):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #  self._dict = kwargs

    def has_args(self):
        """是否包含参数"""
        count = 0
        for k, v in self.__dict__.items():
            if v:
                count += 1
        return count > 1

class Argument():
    name = ''
    short_name = ''
    is_cmd = False
    action = ''
    value = None
    required = False

    def __init__(self, name, action):
        self.name = name.replace('--', '')
        self.is_cmd = True if not name.startswith('--') else False
        self.required = True if self.is_cmd else False
        self.action = action
        self.clear()

    def clear(self):
        self.value = None
        if self.action == Action.STORE_TRUE.value:
            self.value = False

class ArgumentParser():
    logger = create_logger('ArgumentParser')
    cmd = ''
    args = []
    cmd_arg = None

    def add_argument(self, *args, action=None):
        """
        添加参数
        """
        if not action:
            action = Action.STORE.value
        arg = Argument(args[0], action)
        if arg.is_cmd:
            self.cmd_arg = arg
        self.args.append(arg)

    def get_arguments(self):
        """
        获取参数列表
        """
        return self.args

    def parse_args(self, args):
        if not args:
            return None
        args = args if isinstance(args, list) else args.split(" ")
        self._parse_args(args)

            #  d_args = deque(args[1:])
            #  d_args.rotate(-1)
            #  for i, (k, v) in enumerate(zip(args[1:], d_args)):
                #  if i % 2  == 1 or not k.startswith('--'):
                    #  continue
                #  k = k.replace('--', '')
                #  arg = arg_dict.get(k)
                #  if not arg:
                    #  raise Exception('No name arg be {}'.format(k))
                #  arg.value = v
        res = {}
        for arg in self.args:
            res[arg.name] = arg.value
        res[self.cmd_arg.name] = self.cmd_arg.value
        self.logger.info('argument %s', res)

        return ArgumentNamespace(**res)

    def _parse_args(self, args):
        self.logger.info('args %s', args)
        args_len = len(args)
        if args_len == 0:
            return None
        # 情况数据
        for arg in self.args:
            arg.clear()
        # 赋值命令参数
        self.cmd_arg.value = args[0]
        arg_dict = {o.name: o for o in self.args}
        i = 1
        while i < args_len:
            item = args[i]
            if not item.startswith('--'):
                i += 1
                continue
            key = item.replace('--', '')
            arg = arg_dict.get(key)
            if not arg:
                i += 1
                continue
            arg.clear()
            if arg.action == Action.STORE_TRUE.value:
                arg.value = True
            else:
                val_index = i + 1
                if val_index < args_len:
                    arg.value = args[val_index]
                    i += 1
            i += 1

    @classmethod
    def default(cls):
        """
        初始化一个默认实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--config')
        item.add_argument('--space')
        item.add_argument('--module')
        item.add_argument('--root')
        item.add_argument('--name')
        return item

if __name__ == "__main__":
    an = ArgumentNamespace( cmd = 'env', desease_id = 'xx' )
    print(an.__dict__)
    print(len(an.__dict__))
