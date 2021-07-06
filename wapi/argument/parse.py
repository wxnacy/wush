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
    _arg_dict = {}

    def add_argument(self, *args, action=None):
        """
        添加参数
        """
        if not action:
            action = Action.STORE.value
        arg = Argument(args[0], action)
        if arg.is_cmd:
            self.cmd_arg = arg
        self._arg_dict[arg.name] = arg

    def get_arguments(self):
        """
        获取参数列表
        """
        return self._arg_dict.values()

    def get_completion_words(self, words=None):
        """获取补全使用的单词列表"""
        res = []
        if words and isinstance(words, list):
            res.extend(words)
        args = self.get_arguments()
        for arg in args:
            if arg.is_cmd:
                continue
            res.append(arg.name)
        return res

    def parse_args(self, args):
        if not args:
            return None
        args = args if isinstance(args, list) else args.split(" ")
        self._parse_args(args)

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
        for _, arg in self._arg_dict.items():
            arg.clear()
        # 赋值命令参数
        self.cmd_arg.value = args[0]
        i = 1
        while i < args_len:
            item = args[i]
            if not item.startswith('--'):
                i += 1
                continue
            key = item.replace('--', '')
            arg = self._arg_dict.get(key)
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
        item.add_argument('--space')
        item.add_argument('--module')
        return item

if __name__ == "__main__":
    an = ArgumentNamespace( cmd = 'env', desease_id = 'xx' )
    print(an.__dict__)
    print(len(an.__dict__))
