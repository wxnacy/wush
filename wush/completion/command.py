#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
命令补全
"""
import copy

from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import Completion

from wush.common import constants
from wush.common.loggers import create_logger

from wpy.argument import CommandArgumentParser
from wpy.argument import CommandArgumentParserFactory
from wpy.completion import BaseCompleter
from wpy.completion import WordCompleter
from wpy.completion import ExecutableCompleter

class CommandCompleter(BaseCompleter):
    logger = create_logger("CommandCompleter")

    def __init__(self, argparser, wapi):
        self.argparser = argparser
        self.wapi = wapi
        self.path_completer = ExecutableCompleter()

    def yield_words(self, words):
        """获取命令参数的补全器"""
        if words and isinstance(words[0], dict):
            words = [Completion(**o) for o in words]
        _completer = WordCompleter(words)
        yield from self.yield_completer(_completer)

    def get_completions(self, document, complete_event):
        super().get_completions(document, complete_event)
        self.document = document
        self.complete_event = complete_event
        try:
            self.argparser = CommandArgumentParserFactory.build_parser(document.text)
            self.logger.info('completer argparser %s', self.argparser.cmd)
            arg = self.argparser.parse_args(document.text)
            if arg.cmd == 'env':
                self.argparser.set_wapi(self.wapi)
            self.logger.info('args %s', arg)
            cmd = self.first_word

            all_cmds = list(CommandArgumentParserFactory.get_cmd_names())
            # 补全命令
            if cmd not in all_cmds:
                yield from self.yield_words(all_cmds)
                return

            word_for_completion = self.word_for_completion

            # 使用自定义方法返回补全单词
            words = self.wapi.config.get_function().get_completion_words(
                word_for_completion)
            if words:
                yield from self.yield_completer(WordCompleter(words))
                return

            # 补全参数后的信息
            words = self.argparser.get_completions_after_argument(
                    copy.deepcopy(self.wapi), word_for_completion)
            if words:
                yield from self.yield_words(words)
                return

            # 使用模块自带的补全
            if word_for_completion in ('--config', '--root'):
                yield from self.yield_completer(self.path_completer)
            else:
                words = self.argparser.get_completions_after_cmd(arg,
                    word_for_completion)
                yield from self.yield_words(words)

        except:
            import traceback
            self.logger.error(traceback.format_exc())
            self.logger.error(traceback.format_stack())
