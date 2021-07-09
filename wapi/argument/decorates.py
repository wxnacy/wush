#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

_argparser = {}

from wapi.common.loggers import create_logger

logger = create_logger('decorates')

def argparser_register(active=True):
    def decorate(func):
        logger.info('register active=%s func %s.%s', active, func.__module__,
            func)
        #  print('running register(active=%s)->decorate(%s)'
                #  % (active, func))
        if isinstance(func, str):
            raise Exception('test')
        if active:
            _argparser[func.cmd] = func
        else:
            _argparser.pop(func.cmd, None)

        return func
    return decorate

def get_argparsers():
    return dict(_argparser)
