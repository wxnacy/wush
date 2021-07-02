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

class ExecutableCompleter(BaseCompleter):
    logger = create_logger("ExecutableCompleter")

    def get_completions(self, document, complete_event):
        super().get_completions(document, complete_event)
        last_word = document.text.split(' ')[-1]
        self.logger.info('last_word %s', last_word)

        path = os.path.expanduser(last_word)
        dirname = os.path.dirname(path)
        self.logger.info('dirname %s', dirname)

        for name in self.search(os.listdir(dirname)):
            self.logger.info('filename %s', name)
            start_position = self.get_start_position()
            yield Completion(name, start_position=start_position)

