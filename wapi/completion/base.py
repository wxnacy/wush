#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
命令补全
"""

from prompt_toolkit.completion import Completer

from wapi.common import utils
from wapi.common.loggers import create_logger


class BaseCompleter(Completer):
    logger = create_logger("BaseCompleter")
    char_before_cursor = ''
    current_line_before_cursor = ''
    first_word = ''

    def yield_completer(self, completer):
        self.logger.info('completer.__name__ %s', completer)
        items = completer.get_completions(self.document, self.complete_event)
        for item in items:
            yield item

    @property
    def first_word(self):
        """
        获取第一个单词
        """
        def _():
            current_line_before_cursor = self.current_line_before_cursor.strip()
            args = current_line_before_cursor.split(' ')
            args_len = len(args)
            return args[0] if args_len > 0 else ''
        res = _()
        self.logger.info('first_word %s', res)
        return res

    @property
    def word_for_completion(self):
        """补全使用的单词"""
        def _():
            char_before_cursor = self.char_before_cursor
            current_line_before_cursor = self.current_line_before_cursor.strip()
            args = current_line_before_cursor.split(' ')
            args_len = len(args)
            if char_before_cursor == ' ':
                return args[-1]

            return args[-1] if args_len == 1 else args[-2]
        res = _()
        self.logger.info('word_for_completion %s', res)
        return res

    @property
    def word_before_cursor(self):
        """光标前的单词"""
        def _():
            if self.char_before_cursor == ' ':
                return ''
            text = self.current_line_before_cursor
            text = text.split(' ')[-1]
            if text in ('/', '~/'):
                return text
            return text.split('/')[-1]

        res = _()
        self.logger.info('word_before_cursor %s', res)
        return res

    def get_completions(self, document, complete_event):
        self.document = document
        self.complete_event = complete_event
        self.logger.info('-' * 100)
        self.logger.info('word_before_cursor %s', self.word_before_cursor)
        self.logger.info('dir %s', dir(document))
        for k in dir(document):
            if k.startswith('_'):
                continue
            val = getattr(document, k)
            if k.startswith('get'):
                continue
            if k.startswith('find'):
                continue
            #  self.logger.info('%s:=%s= - %s', k, val, type(val))
            if isinstance(val, int) or isinstance(val, str):
                setattr(self, k, val)

    def get_start_position(self):
        """获取文字补全的位置"""
        word = self.word_before_cursor
        if word in ('/', '~/'):
            return 0
        return -len(word)

    def filter(self, name):
        """过滤文件名"""
        name = name.lower()
        word = self.word_before_cursor.lower()
        self.logger.info('name %s word %s', name, word)
        if word in ('/', '~/'):
            return True
        if name.startswith(word):
            return True
        return False

    def search(self, words):
        """搜索"""
        keyword = self.word_before_cursor.lower()
        if keyword in ('/', '~/'):
            return words
        return utils.search(words, keyword)

