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
        last_word = document.text.split(' ')[-1]
        self.logger.info('last_word %s', last_word)

        path = os.path.expanduser(last_word)
        dirname = os.path.dirname(path)
        self.logger.info('dirname %s', dirname)

        for name in os.listdir(dirname):
            self.logger.info('filename %s', name)
            if not self.filter_filename(name):
                continue
            start_position = self.get_start_position()
            yield Completion(name, start_position=start_position)

    def get_start_position(self):
        """获取文字补全的位置"""
        word = self.get_last_full_word(self.document.current_line_before_cursor)
        if word in ('/', '~/'):
            return 0
        return -len(word)

    def filter_filename(self, name):
        """过滤文件名"""
        name = name.lower()
        word = self.get_last_full_word(self.document.current_line_before_cursor)
        if word in ('/', '~/'):
            return True
        if name.startswith(word):
            return True
        return False

    @classmethod
    def get_last_full_word(cls, text):
        """获取最后一个完整的单词"""
        if text is None:
            return None
        text = text.strip()
        if not text:
            print('not', type(text), '-{}-'.format(text))
            return text
        text = text.split(' ')[-1]
        if text in ('/', '~/'):
            return text
        last_text = text.split('/')[-1]
        return last_text

