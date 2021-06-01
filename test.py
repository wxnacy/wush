#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

from wapi.common.decorates import env_functions
from wapi.common.config_value import ConfigValue

if __name__ == "__main__":
    print(env_functions)
    func_str = "test(1, 'ww')"
    name, args_str = func_str.split("(")
    print(name, args_str)
    args = eval('(' + args_str)
    print(args)

    for name, func in env_functions.items():
        print(name, func(1))
