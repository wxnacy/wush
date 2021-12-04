#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import abc
import sys
import os
import argparse
import shutil
import traceback
import pygments

from datetime import datetime
from pygments.token import Token
from pygments.lexers.python import PythonLexer
from prompt_toolkit.formatted_text import PygmentsTokens
from prompt_toolkit import print_formatted_text
from prompt_toolkit import PromptSession
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.completion import WordCompleter

from wush.argument import ArgumentParser
from wush.argument import ArgumentParserFactory
from wush.argument import CommandArgumentParser
from wush.argument import EnvArgumentParser
from wush.common import utils
from wush.common.functions import super_function
from wush.common.functions import run_shell
from wush.common.files import FileUtils
from wush.common.loggers import create_logger
from wush.completion.command import CommandCompleter
from wush.wush import Wapi

from .exceptions import ContinueException
from .exceptions import CommnadNotFoundException

def init_argparse():
    """初始化参数"""
    parser = argparse.ArgumentParser(description='Wapi command',)
    parser.add_argument('-c', '--config', help='Config dir name')
    parser.add_argument('-m', '--module', help='Module name')
    parser.add_argument('-n', '--name', help='Request name')
    parser.add_argument('-s', '--space', help='Space name')
    return parser

class PromptToolkitShell(object, metaclass=abc.ABCMeta):
    logger = create_logger('Shell')

    parser_dict = {}
    parser = None
    _prompt_default = ''
    _prompt_right = ''
    _prompt_left = ''

    def __init__(self):
        self.parser = self._get_parser()
        args = init_argparse().parse_args()
        #  args = init_argparse().parse_args(sys.argv)
        client = Wapi()
        client.init_config(config_root = args.config, space_name = args.space,
            module_name = args.module)
        self.client = client
        self.session = PromptSession(
            completer=CommandCompleter(self.parser, client),
            history = FileHistory(os.path.expanduser('~/.wapi_history')),
            auto_suggest = AutoSuggestFromHistory(),
            complete_in_thread=True
        )

    def _get_parser(self, cmd=None):
        if cmd not in self.parser_dict:
            parser = ArgumentParserFactory.build_parser(cmd)
            if isinstance(parser, CommandArgumentParser):
                parser.set_wapi(self.client)
                parser.set_prompt_session(self.session)
            self.parser_dict[cmd] = parser
        return self.parser_dict[cmd]

    def run(self):
        self._before_run()
        self._run_shell()
        self._after_run()

    def _before_run(self):
        pass

    def _after_run(self):
        pass

    def set_prompt_left(self, text):
        self._prompt_left = text

    def set_prompt_right(self, text):
        self._prompt_right = text

    def set_prompt_default(self, text):
        self._prompt_default = text

    def _run_shell(self):
        while True:
            try:
                text = self.session.prompt(
                    self._prompt_left,
                    default = self._prompt_default,
                    rprompt = self._prompt_right,
                )
                self._run_once_time(text)
            except ContinueException:
                continue
            except CommnadNotFoundException:
                print('command not found: {}'.format(text))
            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                self._print('ERROR: ' + str(e))
                self.logger.error(traceback.format_exc())
            self._end_run()

    def _end_run(self):
        self._prompt_default = ''

    def _run_once_time(self, text):
        """运行"""
        if not text:
            return
        parser = self._get_parser()
        args = parser.parse_args(text)
        cmd = args.cmd
        self.parser = self._get_parser(cmd)
        self.logger.info('run argparser %s', self.parser)

        self._run_base_cmd(text)

        if isinstance(self.parser, CommandArgumentParser):
            self.parser.run(text)
            return

        if not hasattr(self, '_' + cmd):
            raise CommnadNotFoundException()

        func = getattr(self, '_' + cmd)
        func(text)

    def _run_base_cmd(self, text):
        """运行基础命令"""
        if text.startswith('!'):
            text = text[1:]
            try:
                history_num = int(text)
                self.logger.info(history_num)
                cmd = self.get_history_by_num(history_num)
                self._prompt_default = cmd
            except:
                self.logger.error(traceback.format_exc())
                raise CommnadNotFoundException()
            else:
                raise ContinueException()

    def _exit(self, text):
        raise EOFError()

    def get_history_by_num(self, num):
        """获取历史命令"""
        items = self.session.history.get_strings()
        if len(items) < num:
            return None
        return items[num - 1]

    def _print(self, text):
        tokens = list(pygments.lex(text, lexer=PythonLexer()))
        print_formatted_text(PygmentsTokens(tokens), end='')

    @abc.abstractmethod
    def _run_cmd(self, text):
        pass
