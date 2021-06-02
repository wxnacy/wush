#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
import sys
import os

from wapi.common import constants
from wapi.wapi import Wapi

def run():
    import sys
    import os
    args = sys.argv[1:]
    module_name = args[0]
    request_name = args[1]

    client = Wapi()
    func = client.get_config().get_function()
    body_name = func.get_current_body_name(module_name, request_name)
    body_path = os.path.join(constants.CONFIG_ROOT, 'body', body_name)
    os.system('vim {}'.format(body_path))


if __name__ == "__main__":
    run()

