#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
命令补全
"""

from prompt_toolkit.completion import Completer

from wapi.common import constants
from wapi.common.loggers import create_logger
from wapi.common.args import ArgumentParser

from .base import BaseCompleter
from .filesystem import ExecutableCompleter
from .word import WordCompleter as WapiWordCompleter

path_completer = ExecutableCompleter()

cmd_completer = WapiWordCompleter(constants.COMMANDS)

class CommandCompleter(BaseCompleter):
    logger = create_logger("CommandCompleter")
    # 光标前倒数第二个单次
    last_second_word_before_cursor = None
    def __init__(self, argparser, wapi):
        self.argparser = argparser
        self.wapi = wapi

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

    @classmethod
    def get_word_before_completion(cls, document):
        """获取补全的判定单词"""
        char_before_cursor = document.char_before_cursor
        current_line_before_cursor = document.current_line_before_cursor.strip()
        if char_before_cursor == ' ':
            return current_line_before_cursor.split(' ')[-1]
        return current_line_before_cursor.split(' ')[-2]

    def get_cmd_args_completer(self, cmd, arg):
        """获取命令参数的补全器"""
        words = []
        if cmd == constants.COMMAND_ENV:
            for k, v in self.wapi.config.env.dict().items():
                words.append(k)
        else:
            args = constants.COMMAND_CMD_ARGS.get(cmd, [])
            words = {o: 0 for o in args}
            remove_keys = []
            for k in words.keys():
                if getattr(arg, k):
                    self.logger.info(getattr(arg, k))
                    remove_keys.append(k)
            for k in remove_keys:
                words.pop(k, None)
            words = words.keys()
        words = ['--' + o for o in words]
        args_completer = WapiWordCompleter(words)
        yield from self.yield_completer(args_completer)

    def get_completions(self, document, complete_event):
        super().get_completions(document, complete_event)
        self.document = document
        self.complete_event = complete_event
        try:
            arg = self.argparser.parse_args(document.text)
            cmd = self.first_word
            if cmd in cmd_completer.words:
                word_for_completion = self.word_for_completion
                self.logger.info('word_for_completion %s', word_for_completion)
                if word_for_completion in cmd_completer.words:
                    yield from self.get_cmd_args_completer(cmd, arg)
                elif word_for_completion in ('--config', '--root'):
                    self.logger.info('-' * 100)
                    yield from self.yield_completer(path_completer)
                elif word_for_completion == '--module':
                    self.logger.info('-' * 100)
                    self.wapi.init_config(config_root = arg.config)
                    modules = self.wapi.config.get_modules()
                    module_completer = WapiWordCompleter(modules)
                    yield from self.yield_completer(module_completer)
                elif word_for_completion == '--name':
                    self.wapi.init_config(module_name = arg.module)
                    module_name = self.wapi.module_name
                    requests = self.wapi.config.get_requests(module_name)
                    _completer = WapiWordCompleter(requests)
                    yield from self.yield_completer(_completer)
            else:
                yield from self.yield_completer(cmd_completer)
        except:
            import traceback
            self.logger.error(traceback.format_exc())
            self.logger.error(traceback.format_stack())

        #  yield Completion('completion3', start_position=0,
                         #  style='class:special-completion')
