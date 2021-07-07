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

from wapi.argument import ArgumentParser
from wapi.argument import ArgumentParserFactory
from wapi.argument import EnvArgumentParser
from wapi.common.functions import super_function
from wapi.common.files import FileUtils
from wapi.common.loggers import create_logger
from wapi.completion.command import CommandCompleter
from wapi.wapi import Wapi

logger = create_logger('main')
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.completion import WordCompleter

class Shell():
    logger = create_logger('Shell')

    parser_dict = {}
    parser = None
    client = None

    def __init__(self, client):
        self.client = client

    def _get_parser(self, cmd=None):
        if cmd not in self.parser_dict:
            self.parser_dict[cmd] = ArgumentParserFactory.build_parser(cmd)
        return self.parser_dict[cmd]

    def run(self, text):
        """运行"""
        if not text:
            return
        parser = self._get_parser()
        args = parser.parse_args(text)
        cmd = args.cmd
        self.parser = self._get_parser(cmd)
        self.logger.info('run argparser %s', self.parser)

        func = getattr(self, '_' + cmd)
        func(text)

    def _exit(self, text):
        raise EOFError()

    def _run(self, text):
        args = self.parser.parse_args(text)
        if not args.name:
            raise Exception
        self.client.init_config(
            space_name = args.space,
            module_name = args.module,
            request_name = args.name,
            config_root = args.config)
        self.client.request()
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

