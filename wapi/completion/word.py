#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
命令补全
"""

import os
from prompt_toolkit.completion import Completer
from prompt_toolkit.completion import Completion

from wapi.common.loggers import create_logger
from .base import BaseCompleter

class WordCompleter(BaseCompleter):
    logger = create_logger("WordCompleter")

    def __init__(self, words):
        self.words = words

    def get_completions(self, document, complete_event):
        super().get_completions(document, complete_event)
        for name in self.words:
            if not self.filter(name):
                continue
            start_position = self.get_start_position()
            yield Completion(name, start_position=start_position)

