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

PARSERS = [
    ArgumentParser,
    EnvArgumentParser,
]

class ArgumentParserFactory():
    logger = create_logger('ArgumentParserFactory')

    @classmethod
    def build_parser(cls, cmd=None):
        """根据命令构建参数解析器"""
        Parser = ArgumentParser
        for p in PARSERS:
            if p.cmd == cmd:
                Parser = p
        return Parser.default()
