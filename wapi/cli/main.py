#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import sys
import os
import argparse

from wapi.common.functions import super_function
from wapi.wapi import Wapi
from wapi.common.loggers import create_logger

logger = create_logger('main')


def run(args):

    client = Wapi()
    client.init_config(
        space_name = args.space,
        module_name = args.module,
        request_name = args.name)

    res = client.request()
    print('Space:', client.space_name)
    print('Module:', client.module_name)
    print('Name:', client.request_name)
    print("Status:", res.status_code)
    try:
        import json
        print("Response Format:")
        print(json.dumps(res.json(), indent=4, ensure_ascii=False))
    except:
        print('Response Content:')
        print(res.content)
        print('解析 json 失败')

def body(args):
    client = Wapi()
    logger.info(args.space)
    client.init_config(
        space_name = args.space,
        module_name = args.module,
        request_name = args.name)
    config = client.get_config()
    body_name = config.get_current_body_name(client.space_name, client.module_name, client.request_name)
    body_path = config.get_body_path(body_name)
    os.system('vim {}'.format(body_path))

def env(args):
    client = Wapi()
    client.init_config(space_name = args.space)
    config = client.get_config()
    name = config.get_current_env_name(client.space_name)
    path = config.get_env_path(name)
    os.system('vim {}'.format(path))

def module(args):
    client = Wapi()
    client.init_config(module_name = args.module)
    config = client.get_config()
    path = config.get_module_path(client.module_name)
    os.system('vim {}'.format(path))

func_dict = {
    "run": run,
    "body": body,
    "env": env,
    "module": module,
}

def run_cmd():
    parser = argparse.ArgumentParser(description='Wapi command')
    parser.add_argument('cmd', help='You can use run, body, env, module')
    parser.add_argument('-s', '--space', help='Space name')
    parser.add_argument('-m', '--module', help='Module name')
    parser.add_argument('-n', '--name', help='Request name')
    args = parser.parse_args()
    cmd = args.cmd
    name = args.name
    if cmd == 'run':
        if not name:
            raise Exception
    func_dict.get(cmd)(args)



def main():
    run_cmd()

if __name__ == "__main__":
    main()

