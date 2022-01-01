#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""
import json

from wush.common.utils import run_shell
from wush.common.loggers import get_logger

logger = get_logger('wush.run')

__all__ = ['run']

def run(module_name, request_name, **kwargs):
    params = kwargs.get("params", {})
    config = kwargs.get("config")
    cmd = f'wush run --module {module_name} --name {request_name}'
    if params:
        for key, value in params.items():
            cmd += f' --params {key}={value}'
    if config:
        cmd += f' --config {config}'
    logger.info(f'run cmd {cmd}')
    res = run_shell(cmd)
    lines = []
    for line in res:
        line = line.decode()
        for line in line.split('\n'):
            if line.startswith('('):
                continue
            line = line.replace('\n', '')
            lines.append(line)
    text = ''.join(lines)
    logger.info(f'run res {text}')

    return json.loads(text)


if __name__ == "__main__":
    res = run('wush', 'test_get', params={"age": 1})
    print(res)


