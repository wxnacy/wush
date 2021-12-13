#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import sys
import os
import re
import argparse

from wpy.argument import CommandArgumentParserFactory

from wush.argument.command import CmdArgumentParser
from wush.common.constants import Constants
from wush.common.loggers import create_logger
from wush.common.run_mode import RUN_MODE

from wush.cli.shell import Shell
from wush.wush import Wapi

logger = create_logger('main')


def init_argparse():
    """初始化参数"""
    parser = argparse.ArgumentParser(description='Wush command',)
    parser.add_argument('cmd', help='You can use run, body, env, module')
    parser.add_argument('-c', '--config', help='Config dir name')
    parser.add_argument('-m', '--module', help='Module name')
    parser.add_argument('-n', '--name', help='Request name')
    parser.add_argument('-s', '--space', help='Space name')
    parser.add_argument('--curl', help="是否使用 curl", action='store_true')
    return parser

class Command(object):
    logger = create_logger('Command')

    def __init__(self, *args, **kwargs):
        if not os.path.exists(Constants.TMPDIR):
            os.makedirs(Constants.TMPDIR)

    #  @profile
    def run(self):
        RUN_MODE.set_command()
        sys_args = sys.argv[1:]
        if not sys_args:
            shell = Shell()
            shell.run()
            return

        parser = init_argparse()
        args = parser.parse_args()
        cmd = args.cmd
        args_text = ' '.join(sys_args)

        # 判断 cmd 是否为 url 格式
        if re.match(r'^https?:/{2}\w.+$', cmd):
            args_text = 'run ' + args_text.replace(cmd, f'--url {cmd}')
            #  print(args_text)
            cmd = 'run'

        parser = CommandArgumentParserFactory.build_parser(cmd)
        if isinstance(parser, CmdArgumentParser):
            parser.set_wapi(Wapi())
            parser.run(args_text)

