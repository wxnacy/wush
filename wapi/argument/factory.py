#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
from argparse import Namespace
from collections import deque
from enum import Enum

from wapi.common.loggers import create_logger
from .parse import ArgumentParser
from .env import EnvArgumentParser
from .run import RunArgumentParser

PARSERS = [
    ArgumentParser,
    EnvArgumentParser,
    RunArgumentParser,
]

class ArgumentParserFactory():
    logger = create_logger('ArgumentParserFactory')

    @classmethod
    def build_parser(cls, text=None):
        """根据命令构建参数解析器"""
        Parser = ArgumentParser
        cmd = None
        if text:
            args = Parser.default().parse_args(text)
            cmd = args.cmd
        for p in PARSERS:
            if p.cmd == cmd:
                Parser = p
        return Parser.default()
