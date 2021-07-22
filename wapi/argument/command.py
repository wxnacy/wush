#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import abc
import pygments
from argparse import Namespace
from collections import deque

from pygments.token import Token
from pygments.lexers.python import PythonLexer
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit import print_formatted_text

from wpy.argument import ArgumentParser as BaseParser
from wpy.argument import Argument
from wpy.argument import ArgumentNamespace

from wapi.common.loggers import create_logger
from .enum import Action

class CommandArgumentParser(BaseParser, metaclass=abc.ABCMeta):
    logger = create_logger('CommandArgumentParser')
    wapi = None
    prompt_session = None

    #  def __init__(self, wapi=None):
        #  if wapi:
            #  self.wapi = wapi

    def set_wapi(self, client):
        self.wapi = client

    def set_prompt_session(self, client):
        self.prompt_session = client

    @abc.abstractmethod
    def default(cls):
        """
        初始化一个默认实例
        """
        pass

    def get_completions_after_argument(self, wapi, word_for_completion):
        """
        获取补全的单词列表
        :param wapi: Wapi
        :param word_for_completion: 补全需要的单词
        """
        return []

    def get_completions_after_cmd(self, argument, words=None):
        """获取补全使用的单词列表"""
        res = []
        if words and isinstance(words, list):
            res.extend(words)
        args = self.get_arguments()
        for arg in args:
            if arg.is_cmd:
                continue
            # 已经赋值的不需要展示
            if hasattr(argument, arg.name) and getattr(argument, arg.name):
                # 列表除外
                if not arg.is_list:
                    continue
            res.append(dict(text = '--' + arg.name, display_meta = arg.help))
        return res

    @abc.abstractmethod
    def run(self, args):
        """运行"""
        pass

    def _print(self, text):
        tokens = list(pygments.lex(text, lexer=PythonLexer()))
        print_formatted_text(PygmentsTokens(tokens), end='')
