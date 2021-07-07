#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

_env_functions = {}

from wapi.common.loggers import create_logger

logger = create_logger('decorates')

def env_func_register(active=True):
    def decorate(func):
        logger.info('register active=%s func %s.%s', active, func.__module__,
            func)
        #  print('running register(active=%s)->decorate(%s)'
                #  % (active, func))
        if isinstance(func, str):
            raise Exception('test')
        if active:
            _env_functions[func.__name__] = func
        else:
            _env_functions.pop(func.__name__, None)

        return func
    return decorate

def get_env_functions():
    return dict(_env_functions)

if __name__ == "__main__":
    import random
    print(env_functions)
    eval('print(random.random())')
