#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import sys
import os
import argparse
import shutil
import traceback
from datetime import datetime

from prompt_toolkit import PromptSession
from prompt_toolkit.application import run_in_terminal
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.completion import WordCompleter

from wapi.argument import ArgumentParser
from wapi.argument import ArgumentParserFactory
from wapi.argument import EnvArgumentParser
from wapi.common import utils
from wapi.common.functions import super_function
from wapi.common.files import FileUtils
from wapi.common.loggers import create_logger
from wapi.completion.command import CommandCompleter
from wapi.wapi import Wapi

from .exceptions import ContinueException
from .exceptions import CommnadNotFoundException


class Shell():
    logger = create_logger('Shell')

    parser_dict = {}
    parser = None
    client = None
    _prompt_default = ''

    def __init__(self):
        self.parser = self._get_parser()
        args = self.parser.parse_args(sys.argv)
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
            self.parser_dict[cmd] = ArgumentParserFactory.build_parser(cmd)
        return self.parser_dict[cmd]

    def run(self):
        while True:
            try:
                left_prompt = 'wapi/{space}/{module}> '.format(
                    space = self.client.space_name,
                    module = self.client.module_name
                )
                right_prompt = ''
                text = self.session.prompt(
                    left_prompt,
                    default = self._prompt_default,
                    rprompt = right_prompt,
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
                traceback.print_exc()
                self.logger.error(traceback.format_exc())
            self._end_run()

        print('GoodBye!')

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

        try:
            func = getattr(self, '_' + cmd)
            func(text)
        except:
            self.logger.error(traceback.format_exc())
            raise CommnadNotFoundException()

    def _run_base_cmd(self, text):
        """运行基础命令"""
        if text.startswith('!'):
            text = text[1:]
            try:
                history_num = int(text)
                self.logger.info(history_num)
                cmd = self.get_history_by_num(history_num)
                #  def _print_cmd():
                    #  print(cmd)
                #  run_in_terminal(_print_cmd)
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

    def _history(self, text):
        #  items = [o for o in self.session.history.load_history_strings():
        items = self.session.history.get_strings()
        history_max_num_len = len(str(len(items)))
        for i, item in enumerate(items):
            show_index = i + 1
            show_index_fmt = '{{:<{}d}}'.format(history_max_num_len)
            print(show_index_fmt.format(show_index), item)

    def _run(self, text):
        args = self.parser.parse_args(text)
        if not args.name:
            raise Exception
        self.client.init_config(
            space_name = args.space,
            module_name = args.module,
            config_root = args.config)
        _params = args.params or []
        params = utils.list_key_val_to_dict(_params)
        json_data = utils.list_key_val_to_dict(args.json or [])
        self.logger.info('arg params %s', params)
        self.client.request(
            request_name = args.name,
            params = params,
            json = json_data
        )
        self.client.print_response()
        self.client.save()

    def _env(self, text):
        """执行变量操作"""
        args = self.parser.parse_args(text)
        if args.has_args():
            arg_names = [o.name for o in self.parser.get_arguments()]
            for k, v in args.__dict__.items():
                if k not in arg_names:
                    self.client.config.env.add(**{ k: v })
                    print('{}={}'.format(k, v))
            self.client.init_config()
        else:
            for k, v in self.client.config.env.dict().items():
                print('{}={}'.format(k, v))

        # 保存数据
        if args.save:
            env_path = self.client.config.get_env_path()
            env_data = {}
            try:
                env_data = FileUtils.read_dict(env_path)
            except:
                pass
            for k, v in self.client.config.env.dict().items():
                if k in ('body_path',):
                    continue
                if k.isupper():
                    continue
                if not v:
                    continue
                if env_data.get(k) == v:
                    continue
                self.logger.info('Env save %s=%s', k, v)
                env_data[k] = v
            FileUtils.save_yml(env_path, env_data)
            return

    def _config(self, text):
        args = self.parser.parse_args(text)
        if args.has_args():
            self.client.init_config(
                space_name = args.space,
                module_name = args.module,
                config_root = args.config)
        else:
            print('root={}'.format(self.client.config_root))
            print('module={}'.format(self.client.module_name))
            print('space={}'.format(self.client.space_name))

    def _test(self, text):
        #  for k, v in os.environ.items():
            #  print(k, v)
        sname = self.client.config.get_function().get_current_space_name()
        print(sname)
        oname = super_function.get_current_space_name()
        print(oname)

def run_shell():
    parser = ArgumentParserFactory.build_parser()
    client = Wapi()
    session = PromptSession(
        completer=CommandCompleter(parser, client),
        complete_in_thread=True
    )

    cli = Main(client)

    while True:
        try:
            text = session.prompt('wapi> ')
            cli.run(text)

        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        except Exception as e:
            traceback.print_exc()
            print(e)
        #  else:
            #  print('You entered:', text)
    print('GoodBye!')

