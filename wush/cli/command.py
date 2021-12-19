#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
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
from wush.cli.shell import init_argparse

logger = create_logger('main')

class Command(object):
    logger = create_logger('Command')

    def __init__(self, *args, **kwargs):
        if not os.path.exists(Constants.TMPDIR):
            os.makedirs(Constants.TMPDIR)
        self.config = load_config()

    #  @profile
    def run(self):
        RUN_MODE.set_command()
        parser = init_argparse()
        args = parser.parse_args()
        self.config.module_name = args.module
        self.config.space_name = args.space
        cmd = args.cmd
        if cmd == 'shell':
            shell = Shell()
            shell.run()
            return

        sys_args = sys.argv[1:]
        args_text = ' '.join(sys_args)
        # 判断 cmd 是否为 url 格式
        if re.match(r'^https?:/{2}\w.+$', cmd):
            args_text = 'run ' + args_text.replace(cmd, f'--url {cmd}')
            #  print(args_text)
            cmd = 'run'

        parser = CommandArgumentParserFactory.build_parser(cmd)
        if isinstance(parser, CmdArgumentParser):
            parser.run(args_text)

