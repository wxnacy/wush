#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""
import os
from wpy.argument import Action

from wapi.common import utils
from wapi.common.functions import open_version
from wapi.common.loggers import create_logger
from .command import CmdArgumentParser
from wapi.cli.server import PORT
from wpy.argument import CommandArgumentParserFactory

from rich.console import Console
from rich.table import Table

from wapi.models import Version

console = Console()

@CommandArgumentParserFactory.register()
class ViewArgumentParser(CmdArgumentParser):
    cmd = 'view'
    logger = create_logger('ViewArgumentParser')
    _versions = []

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--grep', help='过滤')
        item.add_argument('--open', help='打开')
        item.add_argument('--page', help='页数', datatype=int, default=1)
        item.add_argument('--size', help='每页条数', datatype=int, default=10)
        item.add_argument('--version', help='请求版本')
        return item

    def run(self, text):
        args = self.parse_args(text)
        if args.open:
            self._print('See in browser')
            open_version(args.open)
            return
        self._list(args)

    def _list(self, args):
        items = Version.find()
        items.sort(key = lambda x: x._id, reverse=True)
        #  max_func_length = max([len(o) for o in functions.keys()])
        table = Table(show_header=True, show_lines=True, header_style="bold magenta")
        table.add_column("Version", )
        table.add_column("Space", )
        table.add_column("Module", )
        table.add_column("Name", )

        def _filter(x):
            text = args.grep
            if text in x.space_name or text in x.module_name or \
                    text in x.request_name:
                return True
            return False

        # 过滤列表
        if args.grep:
            items = list(filter(_filter, items))

        total_count = len(items)

        # 分页展示
        start = (args.page - 1) * args.size
        end = start + args.size
        items = items[start:end]
        self._versions = items
        for item in items:
            table.add_row(item._id, item.space_name, item.module_name,
                item.request_name)
        console.print(table)
        if end < total_count:
            console.print('With `--page {}` to see more'.format(args.page + 1))

    def get_completions_after_argument(self, wapi, word_for_completion):
        """
        获取补全的单词列表
        :param wapi: Wapi
        :param word_for_completion: 补全需要的单词
        """
        words = []
        if not self.argument:
            return words
        arg = self.argument
        if word_for_completion == '--open':
            items = self._versions
            if not items:
                items = Version.find()
                items.sort(key = lambda x: x._id, reverse=True)
            for item in items:
                dm = '{}_{}_{}'.format(item.space_name, item.module_name,
                    item.request_name)
                words.append(dict( text = item._id, display_meta=dm))
            return words

        return super().get_completions_after_argument(wapi, word_for_completion)
