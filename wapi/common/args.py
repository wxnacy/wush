#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
#  from argparse import Namespace
#  from collections import deque

#  class ArgumentNamespace(Namespace):
    #  def __init__(self, **kwargs):
        #  super().__init__(**kwargs)
        #  #  self._dict = kwargs

    #  def has_args(self):
        #  """是否包含参数"""
        #  return len(self.__dict__) > 1

#  class ArgumentParser():
    #  cmd = ''
    #  module = ''
    #  name = ''
    #  space = ''
    #  config = ''

    #  def __init__(self, args):
        #  ns = self.parse_args(args)
        #  for k, v in ns.__dict__.items():
            #  setattr(self, k, v)

    #  @classmethod
    #  def parse_args(cls, args):
        #  args = args if isinstance(args, list) else args.split(" ")

        #  args_len = len(args)
        #  res = {}
        #  if args_len >= 1:
            #  res['cmd'] = args[0]

        #  if args_len < 3:
            #  return ArgumentNamespace(**res)

        #  d_args = deque(args[1:])
        #  d_args.rotate(-1)

        #  for i, (k, v) in enumerate(zip(args[1:], d_args)):
            #  if i % 2  == 1 or not k.startswith('--'):
                #  continue
            #  k = k.replace('--', '')
            #  res[k] = v

        #  return ArgumentNamespace(**res)

