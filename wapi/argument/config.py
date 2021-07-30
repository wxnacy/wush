#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""

from .command import CmdArgumentParser
from wpy.argument import CommandArgumentParserFactory

@CommandArgumentParserFactory.register()
class ConfigArgumentParser(CmdArgumentParser):
    cmd = 'config'

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--config')
        item.add_argument('--module')
        item.add_argument('--space')
        return item

    def run(self, text):
        args = self.parse_args(text)
        if args.has_args():
            self.wapi.init_config(
                space_name = args.space,
                module_name = args.module,
                config_root = args.config)
        else:
            self._print('root={}'.format(self.wapi.config_root))
            self._print('module={}'.format(self.wapi.module_name))
            self._print('space={}'.format(self.wapi.space_name))
