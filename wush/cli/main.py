#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
#  import sys
#  import os
#  import re
#  import argparse
#  import shutil
#  import traceback

#  from wpy.argument import CommandArgumentParserFactory

#  from wush.argument.command import CmdArgumentParser
#  from wush.argument.run import RunArgumentParser
#  from wush.common.constants import Constants
from wush.common.loggers import create_logger
#  from wush.common.run_mode import RUN_MODE
#  from wush.wush import Wapi
#  from wush.web.request import RequestClient
#  from wush.web.request import RequestBuilder

#  from wush.cli.shell import Shell
from wush.cli.command import Command

logger = create_logger('main')

#  def run(client):
    #  res = client.request()
    #  client.print_response()
    #  client.save()

#  def body(args):

    #  config = client.config
    #  default_body_name = config.get_current_body_name('default', client.module_name, client.request_name)
    #  default_body_path = config.get_body_path(default_body_name)
    #  body_name = config.get_current_body_name(client.space_name, client.module_name, client.request_name)
    #  body_path = config.get_body_path(body_name)
    #  logger.info('Default body path: %s', default_body_path)
    #  logger.info('Body path: %s', body_path)
    #  # 如果存在默认 body 文件，切不存在 space body 文件时，copy 默认文件
    #  if os.path.exists(default_body_path) and not os.path.exists(body_path):
        #  shutil.copy(default_body_path, body_path)
    #  os.system('vim {}'.format(body_path))
    #  # 如果不存在默认文件，生成一份
    #  if not os.path.exists(default_body_path):
        #  shutil.copy(body_path, default_body_path)

#  def env(client):
    #  client.config.env.add
    #  config = client.config
    #  name = config.get_current_env_name(client.space_name)
    #  path = config.get_env_path(name)
    #  os.system('vim {}'.format(path))

#  def module(args):
    #  config = client.config
    #  path = config.get_module_path(client.module_name)
    #  os.system('vim {}'.format(path))

#  func_dict = {
    #  "run": run,
    #  "body": body,
    #  "env": env,
    #  "module": module,
#  }

#  def init_argparse():
    #  """初始化参数"""
    #  parser = argparse.ArgumentParser(description='Wush command',)
    #  parser.add_argument('cmd', help='You can use run, body, env, module')
    #  parser.add_argument('-c', '--config', help='Config dir name')
    #  parser.add_argument('-m', '--module', help='Module name')
    #  parser.add_argument('-n', '--name', help='Request name')
    #  parser.add_argument('-s', '--space', help='Space name')
    #  parser.add_argument('--curl', help="是否使用 curl", action='store_true')
    #  return parser

#  def run_cmd():
    #  parser = init_argparse()
    #  args = parser.parse_args()
    #  cmd = args.cmd
    #  name = args.name
    #  if cmd == 'run':
        #  if not name:
            #  raise Exception
    #  client = Wapi()
    #  client.init_config(
        #  space_name = args.space,
        #  module_name = args.module,
        #  request_name = args.name,
        #  config_root = args.config)
    #  func_dict.get(cmd)(client)

#  def run_shell():
    #  cli = Shell()
    #  cli.run()

#  from line_profiler import LineProfiler

#  class Command(object):
    #  logger = create_logger('Command')

    #  def __init__(self, *args, **kwargs):
        #  if not os.path.exists(Constants.TMPDIR):
            #  os.makedirs(Constants.TMPDIR)

    #  #  @profile
    #  def run(self):
        #  RUN_MODE.set_command()
        #  sys_args = sys.argv[1:]
        #  if not sys_args:
            #  shell = Shell()
            #  shell.run()
            #  return

        #  parser = init_argparse()
        #  args = parser.parse_args()
        #  cmd = args.cmd
        #  args_text = ' '.join(sys_args)

        #  # 判断 cmd 是否为 url 格式
        #  if re.match(r'^https?:/{2}\w.+$', cmd):
            #  args_text = 'run ' + args_text.replace(cmd, f'--url {cmd}')
            #  print(args_text)
            #  cmd = 'run'

        #  parser = CommandArgumentParserFactory.build_parser(cmd)
        #  if isinstance(parser, CmdArgumentParser):
            #  parser.run(args_text)
        #  else:
            #  # 直接执行 url 的请求
            #  builder = RequestBuilder(method='get', url = cmd)
            #  req_client = RequestClient(builder)
            #  res = req_client.request()
            #  import json
            #  if res.is_json():
                #  print(json.dumps(res.json(), indent=4))
            #  else:
                #  print(res.text)


def main():
    import time
    begin = time.time()
    cmd = Command()
    cmd.run()
    logger.info('wush time used: {}'.format(time.time() - begin))

if __name__ == "__main__":
    main()

#  index_model.__subclasses__():
