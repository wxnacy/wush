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

from wapi.common.functions import super_function
from wapi.common.loggers import create_logger
from wapi.wapi import Wapi

logger = create_logger('main')

def run(args):
    config_root = args.config

    client = Wapi()
    client.init_config(
        space_name = args.space,
        module_name = args.module,
        request_name = args.name,
        config_root = config_root)

    res = client.request()
    client.print_response()
    client.save()

def body(args):
    client = Wapi()
    client.init_config(
        space_name = args.space,
        module_name = args.module,
        request_name = args.name)

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

def env(args):
    client = Wapi()
    client.init_config(space_name = args.space)
    config = client.config
    name = config.get_current_env_name(client.space_name)
    path = config.get_env_path(name)
    os.system('vim {}'.format(path))

def module(args):
    client = Wapi()
    client.init_config(module_name = args.module)
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
    parser = argparse.ArgumentParser(description='Wapi command')
    parser.add_argument('cmd', help='You can use run, body, env, module')
    parser.add_argument('-s', '--space', help='Space name')
    parser.add_argument('-m', '--module', help='Module name')
    parser.add_argument('-n', '--name', help='Request name')
    parser.add_argument('-c', '--config', help='Config dir name')
    return parser

def run_cmd():
    parser = init_argparse()
    args = parser.parse_args()
    cmd = args.cmd
    name = args.name
    if cmd == 'run':
        if not name:
            raise Exception
    func_dict.get(cmd)(args)

from prompt_toolkit import PromptSession

def run_shell():
    session = PromptSession(complete_in_thread=True)
    parser = init_argparse()
    client = Wapi()

    while True:
        try:
            text = session.prompt('wapi> ')
            args = parser.parse_args(text.split(' '))
            cmd = args.cmd
            if cmd == 'exit':
                break

            # 设置 client
            client.init_config(
                space_name = args.space,
                module_name = args.module,
                request_name = args.name,
                config_root = args.config)

            name = args.name
            if cmd == 'run':
                if not name:
                    raise Exception
            #  func_dict.get(cmd)(args)
            res = client.request()
            client.print_response()
            client.save()
        except KeyboardInterrupt:
            continue
        except EOFError:
            break
        except Exception as e:
            traceback.print_exc()
            print(e)
        else:
            print('You entered:', text)
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

