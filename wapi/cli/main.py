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
from wapi.common.functions import super_function
from wapi.common.loggers import create_logger
from wapi.completion.command import CommandCompleter
from wapi.wapi import Wapi

logger = create_logger('main')

def run(client):
    res = client.request()
    client.print_response()
    client.save()

def body(args):

    config = client.config
    default_body_name = config.get_current_body_name('default', client.module_name, client.request_name)
    default_body_path = config.get_body_path(default_body_name)
    body_name = config.get_current_body_name(client.space_name, client.module_name, client.request_name)
    body_path = config.get_body_path(body_name)
    logger.info('Default body path: %s', default_body_path)
    logger.info('Body path: %s', body_path)
    # 如果存在默认 body 文件，切不存在 space body 文件时，copy 默认文件
    if os.path.exists(default_body_path) and not os.path.exists(body_path):
        shutil.copy(default_body_path, body_path)
    os.system('vim {}'.format(body_path))
    # 如果不存在默认文件，生成一份
    if not os.path.exists(default_body_path):
        shutil.copy(body_path, default_body_path)

def env(client):
    client.config.env.add
    config = client.config
    name = config.get_current_env_name(client.space_name)
    path = config.get_env_path(name)
    os.system('vim {}'.format(path))

def module(args):
    config = client.config
    path = config.get_module_path(client.module_name)
    os.system('vim {}'.format(path))

func_dict = {
    "run": run,
    "body": body,
    "env": env,
    "module": module,
}

def init_argparse():
    """初始化参数"""
    parser = argparse.ArgumentParser(description='Wapi command',)
    parser.add_argument('cmd', help='You can use run, body, env, module')
    parser.add_argument('-c', '--config', help='Config dir name')
    parser.add_argument('-m', '--module', help='Module name')
    parser.add_argument('-n', '--name', help='Request name')
    parser.add_argument('-s', '--space', help='Space name')
    return parser

def run_cmd():
    parser = init_argparse()
    args = parser.parse_args()
    cmd = args.cmd
    name = args.name
    if cmd == 'run':
        if not name:
            raise Exception

    client = Wapi()
    client.init_config(
        space_name = args.space,
        module_name = args.module,
        request_name = args.name,
        config_root = args.config)
    func_dict.get(cmd)(client)

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.completion import WordCompleter

def init_wapi_args():
    parser = ArgumentParser()
    parser.add_argument('cmd')
    parser.add_argument('--config')
    parser.add_argument('--root')
    parser.add_argument('--module')
    parser.add_argument('--name')
    parser.add_argument('--space')
    parser.add_argument('--save', action='store_true')
    return parser


def run_shell():
    wapi_parser = init_wapi_args()
    parser = init_argparse()
    client = Wapi()
    session = PromptSession(
        completer=CommandCompleter(wapi_parser, client),
        complete_in_thread=True
    )

    while True:
        try:
            text = session.prompt('wapi> ')
            input_args = text.split(" ")
            logger.info(input_args)
            wapi_args = wapi_parser.parse_args(text)
            cmd = wapi_args.cmd
            logger.info('cmd %s',  cmd)
            if cmd == 'exit':
                break

            if cmd == 'run':
                args = parser.parse_args(input_args)
                if not args.name:
                    raise Exception
                # 设置 client
                client.init_config(
                    space_name = args.space,
                    module_name = args.module,
                    request_name = args.name,
                    config_root = args.config)

            if cmd == 'env':
                if wapi_args.save:
                    continue
                if wapi_args.has_args():
                    client.config.env.add(**wapi_args.__dict__)
                else:
                    for k, v in client.config.env.dict().items():
                        print('{}={}'.format(k, v))
            elif cmd == 'config':
                if wapi_args.has_args():
                    client.init_config(
                        space_name = wapi_args.space,
                        module_name = wapi_args.module,
                        config_root = wapi_args.root)
                else:
                    print('root={}'.format(client.config_root))
                    print('module={}'.format(client.module_name))
                    print('space={}'.format(client.space_name))
            else:
                func = func_dict.get(cmd)
                if func:
                    func(client)
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

def main():
    import sys
    args = sys.argv[1:]
    if not args:
        # 使用交互模式
        run_shell()
    else:
        # 使用命令行模式
        run_cmd()

if __name__ == "__main__":
    main()

