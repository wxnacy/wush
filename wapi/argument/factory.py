#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
from wapi.common.loggers import create_logger
from .decorates import get_argparsers
from .parse import ArgumentParser

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
        cls.logger.info('text %s argparser %s', text, Parser.cmd)
        return Parser.default()

    @classmethod
    def get_cmd_names(cls):
        return cls.PARSERS.keys()
