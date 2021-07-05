#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import pytest

from wapi.common import utils
from wapi.argument import ArgumentParser

def test_parse_args():
    parser = ArgumentParser()
    parser.add_argument('cmd')
    parser.add_argument('--config')
    parser.add_argument('--module')
    parser.add_argument('--save', action='store_true')

    line = 'run'
    arg = parser.parse_args(line)
    assert arg.cmd, 'run'
    assert not arg.save, True

    line = 'env --save'
    arg = parser.parse_args(line)
    assert arg.cmd, 'env'
    assert arg.save, True

    line = 'run --config config'
    arg = parser.parse_args(line)
    assert arg.cmd, 'run'
    assert arg.config, 'config'

    line = 'run --config config --module default'
    arg = parser.parse_args(line)
    assert arg.cmd, 'run'
    assert arg.config, 'config'
    assert arg.module, 'module'
