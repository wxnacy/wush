#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

from wpy.base import BaseEnum

class ModeEnum(BaseEnum):
    COMMAND = 'command'
    SHELL = 'shell'

class RunMode(object):
    name = 'run_mode'
    value = None

    @property
    def is_command(self):
        """是否为命令模式"""
        return self.value == ModeEnum.COMMAND.value

    @property
    def is_shell(self):
        """是否为 shell 模式"""
        return self.value == ModeEnum.SHELL.value

    def set_command(self):
        self.value = ModeEnum.COMMAND.value

    def set_shell(self):
        self.value = ModeEnum.SHELL.value

RUN_MODE = RunMode()
