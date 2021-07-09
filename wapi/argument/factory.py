#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
from argparse import Namespace
from collections import deque
from enum import Enum

from wapi.common.loggers import create_logger
from .decorates import get_argparsers
from .parse import ArgumentParser
#  from .env import EnvArgumentParser
#  from .run import RunArgumentParser
#  from .history import HistoryArgumentParser
#  from .config import ConfigArgumentParser

# TODO delete after 2021-07-16
#  PARSERS = [
    #  ArgumentParser,
    #  EnvArgumentParser,
    #  RunArgumentParser,
    #  ConfigArgumentParser,
    #  HistoryArgumentParser,
#  ]


class ArgumentParserFactory():
    logger = create_logger('ArgumentParserFactory')
    PARSERS = get_argparsers()

    @classmethod
    def build_parser(cls, text=None):
        """根据命令构建参数解析器"""
        Parser = ArgumentParser
        cmd = None
        if text:
            args = Parser.default().parse_args(text)
            cmd = args.cmd
        Parser = cls.PARSERS.get(cmd, ArgumentParser)
        #  for p in PARSERS:
            #  if p.cmd == cmd:
                #  Parser = p
        cls.logger.info('text %s argparser %s', text, Parser.cmd)
        return Parser.default()

    @classmethod
    def get_cmd_names(cls):
        return cls.PARSERS.keys()
