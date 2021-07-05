#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""

class RunArgument():

    cmd = ''
    module = ''
    name = ''
    space = ''
    config = ''

    def __init__(self, args):
        self.args = args if isinstance(args, list) else args.split(" ")

        args_len = len(self.args)
        if args_len >= 1:
            self.cmd = self.args[0]

        if args_len < 3:
            return

        i = 1
        while i < args_len:
            item = self.args[i]
            for k in ('module', 'name', 'space', 'config'):
                if item == '--' + k:
                    val_index = i + 1
                    if val_index < args_len:
                        i += 1
                        setattr(self, k, self.args[val_index])
            i += 1


