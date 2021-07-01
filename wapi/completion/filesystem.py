#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
命令补全
"""

import os
from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import Completion

from wapi.common.loggers import create_logger
from .base import BaseCompleter

class ExecutableCompleter(BaseCompleter):
    logger = create_logger("ExecutableCompleter")

    def get_completions(self, document, complete_event):
        super().get_completions(document, complete_event)
        text = document.text
        last_word = document.text.split(' ')[-1]
        self.logger.info('last_word %s', last_word)

        path = os.path.expanduser(last_word)
        dirname = os.path.dirname(path)
        self.logger.info('dirname %s', dirname)

        word = self.word_before_cursor
        for name in os.listdir(dirname):
            self.logger.info('filename %s', name)
            if not self.filter_filename(name):
                continue
            start_position = self.get_start_position()
            yield Completion(name, start_position=start_position)
                         #  style='class:special-completion')

    def get_start_position(self):
        """获取文字补全的位置"""
        if self.word_before_cursor in ('/', '~/'):
            return 0
        return -len(self.word_before_cursor)

    def filter_filename(self, name):
        """过滤文件名"""
        name = name.lower()
        word = self.word_before_cursor.lower()
        if word in ('/', '~/'):
            return True
        if name.startswith(word):
            return True
        return False

