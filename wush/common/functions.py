#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import importlib
import os
import subprocess

from rich.console import Console

console = Console()

from wush.common.loggers import get_logger

logger = get_logger('function')

def run_shell(command):
    """运行 shell 语句"""
    res = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE,
        stderr = subprocess.PIPE)
    return res.communicate()

def open_version(version, otype=None):
    """使用浏览器打开 url"""
    request_url = ("http://0.0.0.0:{port}/api/version/{version}").format(
        port = get_current_web_port(),
        version = version)
    if otype:
        request_url += '/' + otype
    os.system('open -a "/Applications/Google Chrome.app" "{}"'.format(
        request_url))

def load_module(module_name):
    """加载模块"""
    views_module = importlib.import_module(module_name)
    return views_module
