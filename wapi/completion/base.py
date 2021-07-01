#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
命令补全
"""

from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.completion import ExecutableCompleter

from wapi.common.loggers import create_logger

path_completer = ExecutableCompleter()

cmd_completer = WordCompleter(['run', 'body', 'env', 'module'],
    ignore_case=True)

args_completer = WordCompleter(['--config', '--module', '--name', '--space'],
    ignore_case=True)

class BaseCompleter(Completer):
    logger = create_logger("BaseCompleter")
    # 光标前倒数第二个单次
    last_second_word_before_cursor = None

    def yield_completer(self, completer):
        self.logger.info('completer.__name__ %s', completer)
        items = completer.get_completions(self.document, self.complete_event)
        for item in items:
            yield item

    def input_to_args(self, text):
        """格式化输入"""
        self.logger.info('input %s', text)
        text = text.strip('-').strip()
        input_args = text.split(" ")
        input_len = len(input_args)
        if len(input_args) > 1 and len(input_args) % 2 ==0:
            input_args.append('_')
        word_before_cursor = self.document.get_word_before_cursor()
        self.last_input_text = word_before_cursor
        self.last_input_text = word_before_cursor
        self.logger.info('document =%s=', word_before_cursor)
        self.logger.info('crp %s', self.document.get_word_under_cursor())
        self.logger.info('crp %s', self.document.current_line_before_cursor)

        # 光标之前的参数列表
        before_cursor_input_args = self.document.current_line_before_cursor.split()
        if len(before_cursor_input_args) > 1:
            self.last_second_word_before_cursor = before_cursor_input_args[-2]
        self.logger.info('last_second_word_before_cursor %s',
                self.last_second_word_before_cursor)

        args = self.argparser.parse_args(input_args)
        self.logger.info('cmd %s', args.cmd)
        self.logger.info('cmd config %s', args.config)
        self.logger.info('cmd module %s', args.module)
        return args

    def get_completions(self, document, complete_event):
        self.document = document
        self.complete_event = complete_event
