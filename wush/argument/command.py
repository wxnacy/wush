#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import abc
import pygments

from pygments.token import Token
from pygments.lexers.python import PythonLexer
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit import print_formatted_text

from wpy.argument import CommandArgumentParser

from wush.common.loggers import create_logger
from wush.config import load_config

class CmdArgumentParser(CommandArgumentParser):
    logger = create_logger('CmdArgumentParser')
    prompt_session = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config = load_config()

    def set_prompt_session(self, client):
        self.prompt_session = client

    def get_completions_after_argument(self, word_for_completion):
        """
        获取补全的单词列表
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
            # 列表除外
            if arg.is_set and not arg.is_list:
                continue
            res.append(dict(text = '--' + arg.name, display_meta = arg.help))
        return res

    def parse_args(self, text):
        """解析参数"""
        args = super().parse_args(text)
        arg_list = self.get_arguments()
        for arg in arg_list:
            log_text = f'{self.cmd} argument {arg.name}' \
                f' {getattr(args, arg.name.replace("-", "_"))}'
            self.logger.info(log_text)
        return args

    def _print(self, text):
        tokens = list(pygments.lex(text, lexer=PythonLexer()))
        print_formatted_text(PygmentsTokens(tokens), end='')

