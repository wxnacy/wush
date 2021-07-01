#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
命令补全
"""

from prompt_toolkit.completion import Completer

from wapi.common.loggers import create_logger


class BaseCompleter(Completer):
    logger = create_logger("BaseCompleter")

    def yield_completer(self, completer):
        self.logger.info('completer.__name__ %s', completer)
        items = completer.get_completions(self.document, self.complete_event)
        for item in items:
            yield item

    def get_completions(self, document, complete_event):
        self.document = document
        self.complete_event = complete_event
        self.word_before_cursor = document.get_word_before_cursor()
        self.logger.info('word_before_cursor %s', self.word_before_cursor)

