#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""
import os
from wpy.argument import Action

from wush.common import utils
from wush.common.loggers import create_logger
from .command import CmdArgumentParser
from wush.cli.server import PORT
from wpy.argument import CommandArgumentParserFactory

from rich.console import Console
from rich.table import Table

console = Console()

@CommandArgumentParserFactory.register()
class FuncArgumentParser(CmdArgumentParser):
    cmd = 'func'
    logger = create_logger('FuncArgumentParser')

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        return item

    def run(self, text):
        functions = self.wapi.config.get_function().get_functions()
        max_func_length = max([len(o) for o in functions.keys()])
        table = Table(show_header=True, show_lines=True, header_style="bold magenta")
        table.add_column("方法名", width=max_func_length)
        table.add_column("描述", )
        table.add_column("模块", )

        for k, v in functions.items():
            table.add_row(k, getattr(v, '__doc__'), getattr(v, '__module__'))
        console.print(table)
