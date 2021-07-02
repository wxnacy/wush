#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import pytest

from wapi.common import utils
from wapi.common.args import ArgumentParser


def test_init():
    line = ''
    arg = ArgumentParser(line)
    #  assert arg.cmd, ''
    #  for k in ('cmd', 'module', 'name', 'space', 'config'):
        #  assert getattr(arg, k), ''

    line = 'run'
    arg = ArgumentParser(line)
    assert arg.cmd, 'run'
    #  assert arg.module, ''
    #  for k in ('module', 'name', 'space', 'config'):
        #  assert getattr(arg, k), ''

    line = 'run --config config'
    arg = ArgumentParser(line)
    assert arg.cmd, 'run'
    assert arg.config, 'config'

    line = 'run --config config --module default'
    arg = ArgumentParser(line)
    assert arg.cmd, 'run'
    assert arg.config, 'config'
    assert arg.module, 'module'
