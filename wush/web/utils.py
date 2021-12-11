#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
网络相关工具方法
"""

import socket


def telnet(server_ip, port):
    """链接服务"""
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sk.settimeout(1) #设置超时时间
    try:
        sk.connect((server_ip,port))
        sk.close()
        return True
    except Exception:
        sk.close()
        return False
