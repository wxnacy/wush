#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import argparse
import sys
import os
import re

from wpy.argument import CommandArgumentParserFactory

from wush.argument.command import CmdArgumentParser
from wush.common.constants import Constants
from wush.common.loggers import create_logger
from wush.common.run_mode import RUN_MODE
from wush.config import load_config

from wush.cli.shell import Shell

logger = create_logger('main')

__all__ = ['Command']


class Command(object):
    logger = create_logger('Command')

    def __init__(self, *args, **kwargs):
        if not os.path.exists(Constants.TMPDIR):
            os.makedirs(Constants.TMPDIR)
        #  self.config = load_config()

    def convert_argparse(self, cmd):
        self.parser = CommandArgumentParserFactory.build_parser(cmd)
        arguments = self.parser.get_arguments()
        parser = argparse.ArgumentParser(description='Wush command',)
        parser.add_argument('cmd')
        for arg in arguments:
            names = []
            if arg.name:
                names.append(f'--{arg.name}')
            if arg.short_name:
                names.append(f'-{arg.short_name}')
            parser.add_argument(*names, help=arg.help, action=arg.action)
        return parser

    #  @profile
    def run(self):
        sys_args = sys.argv[1:]
        cmd = 'shell'
        if sys_args:
            cmd = sys_args[0]

        args_text = ' '.join(sys_args)
        # 判断 cmd 是否为 url 格式
        if re.match(r'^https?:/{2}\w.+$', cmd):
            args_text = 'run ' + args_text.replace(cmd, f'--url {cmd}')
            cmd = 'run'

        RUN_MODE.set_command()
        # 转换参数解析器
        parser = self.convert_argparse(cmd)
        args = parser.parse_args()
        self.config = load_config(args.config)
        self.config.module_name = args.module
        self.config.space_name = args.space
        cmd = args.cmd
        if cmd == 'shell':
            shell = Shell()
            shell.run()
            return

        if isinstance(self.parser, CmdArgumentParser):
            self.parser.run(args_text)

