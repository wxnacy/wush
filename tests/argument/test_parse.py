#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import pytest

#  from wapi.common import utils
#  from wapi.argument import ArgumentParser
#  from wapi.argument import Action

#  def test_parse_args():
    #  parser = ArgumentParser()
    #  parser.add_argument('cmd')
    #  parser.add_argument('--config')
    #  parser.add_argument('--module')
    #  parser.add_argument('--name')
    #  parser.add_argument('--save', action=Action.STORE_TRUE.value)
    #  parser.add_argument('--params', action=Action.APPEND.value)

    #  line = 'run'
    #  arg = parser.parse_args(line)
    #  assert arg.cmd == 'run'
    #  assert arg.save is False

    #  line = 'env --save'
    #  arg = parser.parse_args(line)
    #  assert arg.cmd == 'env'
    #  assert arg.save == True

    #  line = 'run --config config'
    #  arg = parser.parse_args(line)
    #  assert arg.cmd == 'run'
    #  assert arg.config == 'config'

    #  line = 'run --config config --module default'
    #  arg = parser.parse_args(line)
    #  assert arg.cmd == 'run'
    #  assert arg.config == 'config'
    #  assert arg.module == 'default'

    #  line = 'run --config config --name test name'
    #  arg = parser.parse_args(line)
    #  assert arg.cmd == 'run'
    #  assert arg.config == 'config'
    #  #  assert arg.name == 'test name'

    #  line = 'run --name test name --config config'
    #  arg = parser.parse_args(line)
    #  assert arg.cmd == 'run'
    #  assert arg.config == 'config'
    #  #  assert arg.name == 'test name'

    #  line = 'run --params key=value --params name=wxnacy --config config'
    #  arg = parser.parse_args(line)
    #  assert arg.cmd == 'run'
    #  assert arg.config == 'config'
    #  assert arg.params == ['key=value', 'name=wxnacy']
