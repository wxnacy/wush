#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

env_functions = {}

def env_func_register(active=True):
    def decorate(func):
        #  print('running register(active=%s)->decorate(%s)'
                #  % (active, func))
        if active:
            env_functions[func.__name__] = func
        else:
            env_functions.pop(func.__name__, None)

        return func
    return decorate

if __name__ == "__main__":
    import random
    print(env_functions)
    eval('print(random.random())')
