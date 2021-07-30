#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""

from .decorates import argparser_register
from wpy.argument import CommandArgumentParser

@argparser_register()
class HistoryArgumentParser(CommandArgumentParser):
    cmd = 'history'

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        return item

    def run(self, text):
        #  items = [o for o in self.session.history.load_history_strings():
        items = self.prompt_session.history.get_strings()
        history_max_num_len = len(str(len(items)))
        for i, item in enumerate(items):
            show_index = i + 1
            show_index_fmt = '{{:<{}d}}'.format(history_max_num_len)
            line = '{} {}'.format(show_index_fmt.format(show_index), item)
            self._print(line)
