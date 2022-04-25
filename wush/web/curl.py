#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""
网络相关工具方法
"""

import argparse
from shlex import split
from http.cookies import SimpleCookie
from urllib.parse import urlparse
from w3lib.http import basic_auth_header

from wush.common.loggers import get_logger

logger = get_logger('curl')

class CurlParser(argparse.ArgumentParser):
    def error(self, message):
        error_msg = \
            'There was an error parsing the curl command: {}'.format(message)
        raise ValueError(error_msg)

curl_parser = CurlParser()
curl_parser.add_argument('url')
curl_parser.add_argument('-H', '--header', dest='headers', action='append')
curl_parser.add_argument('-X', '--request', dest='method', default='get')
curl_parser.add_argument('-d', '--data', '--data-raw', dest='data')
curl_parser.add_argument('-u', '--user', dest='auth')

safe_to_ignore_arguments = [
    ['--compressed'],
    # `--compressed` argument is not safe to ignore, but it's included here
    # because the `HttpCompressionMiddleware` is enabled by default
    ['-s', '--silent'],
    ['-v', '--verbose'],
    ['-#', '--progress-bar']
]
for argument in safe_to_ignore_arguments:
    curl_parser.add_argument(*argument, action='store_true')

def curl_to_request_kwargs(curl_command, ignore_unknown_options=True):
    """Convert a cURL command syntax to Request kwargs.
    :param str curl_command: string containing the curl command
    :param bool ignore_unknown_options: If true, only a warning is emitted when
    cURL options are unknown. Otherwise raises an error. (default: True)
    :return: dictionary of Request kwargs
    """
    curl_args = split(curl_command)
    if curl_args[0] != 'curl':
        raise ValueError('A curl command must start with "curl"')
    parsed_args, argv = curl_parser.parse_known_args(curl_args[1:])
    if argv:
        msg = 'Unrecognized options: {}'.format(', '.join(argv))
        if ignore_unknown_options:
            #  warnings.warn(msg)
            logger.warn(msg)
        else:
            raise ValueError(msg)
    url = parsed_args.url
    # curl automatically prepends 'http' if the scheme is missing, but Request
    # needs the scheme to work
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        url = 'http://' + url
    result = {'method': parsed_args.method.upper(), 'url': url}
    headers = {}
    cookies = {}
    for header in parsed_args.headers or ():
        name, val = header.split(':', 1)
        name = name.strip()
        val = val.strip()
        if name.title() == 'Cookie':
            for name, morsel in SimpleCookie(val).items():
                cookies[name] = morsel.value
        else:
            headers[name] = val
    if parsed_args.auth:
        user, password = parsed_args.auth.split(':', 1)
        headers['Authorization']= basic_auth_header(user, password)
    if headers:
        result['headers'] = headers
    if cookies:
        result['cookies'] = cookies
    if parsed_args.data:
        result['body'] = parsed_args.data
    return result

class cUrl(object):

    @classmethod
    def dump(cls, filepath):
        with open(filepath, 'r') as f:
            lines = f.readlines()
        texts = []
        for line in lines:
            line = line.strip().strip('\n').strip('\\')
            if line.startswith('#'):
                continue
            texts.append(line)
        text = ''.join(texts)
        return cls.dumps(text)

    @classmethod
    def dumps(cls, text):
        return curl_to_request_kwargs(text)