#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import sys
import os
import re

from csarg import CommandArgumentParserFactory

from wush.argument.command import CmdArgumentParser
from wush.common.constants import Constants
from wush.common.loggers import create_logger
from wush.common.run_mode import RUN_MODE
from wush.config import load_config

__all__ = ['Command']

class Command(object):
    logger = create_logger('Command')

    def __init__(self, *args, **kwargs):
        if not os.path.exists(Constants.TMPDIR):
            os.makedirs(Constants.TMPDIR)

    def convert_argparse(self, cmd):

        for clz in CmdArgumentParser.__subclasses__():
            if clz.cmd == cmd:
                return clz.default()

        return CommandArgumentParserFactory.build_parser(cmd)

    #  @profile
    def run(self):
        sys_args = sys.argv[1:]
        if not sys_args:
            sys_args = ['shell']
        cmd = sys_args[0]

        args_text = ' '.join(sys_args)
        # 判断 cmd 是否为 url 格式
        if re.match(r'^https?:/{2}\w.+$', cmd):
            args_text = 'run ' + args_text.replace(cmd, f'--url {cmd}')
            cmd = 'run'

        RUN_MODE.set_command()
        # 转换参数解析器
        parser = self.convert_argparse(cmd)

        args = parser.parse_args(args_text)
        # 加载配置
        config_path = None
        if hasattr(args, 'config'):
            config_path = args.config
        self.config = load_config(config_path)
        if hasattr(args, 'module'):
            self.config.module_name = args.module
        if hasattr(args, 'space'):
            self.config.space_name = args.space

        if isinstance(parser, CmdArgumentParser):
            parser.run(args_text)

