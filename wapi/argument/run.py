#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""

from .decorates import argparser_register
from .enum import Action
from .parse import ArgumentParser

@argparser_register()
class RunArgumentParser(ArgumentParser):
    cmd = 'run'

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--module', help='模块名称')
        item.add_argument('--space', help='空间名称')
        item.add_argument('--name', help='请求名称')
        item.add_argument('--params', action = Action.APPEND.value,
            help='请求地址参数')
        item.add_argument('--json', action = Action.APPEND.value,
            help='请求 body 参数，json 格式')
        item.add_argument('--open', action = Action.STORE_TRUE.value,
            help = '是否通过浏览器打开请求结果')
        return item

    def get_completions_after_argument(self, wapi, word_for_completion):
        """
        获取补全的单词列表
        :param wapi: Wapi
        :param word_for_completion: 补全需要的单词
        """
        words = []
        if not self.argument:
            return words
        arg = self.argument
        wapi.init_config(
            module_name = arg.module,
            request_name = arg.name
        )
        if word_for_completion == '--name':
            module_name = wapi.module_name
            requests = wapi.config.get_requests(module_name)
            words = []
            for req in requests:
                words.append(dict( text = req.get("name"),
                    display_meta=req.get("title")
                    ))
            return words
        elif word_for_completion == '--module':
            modules = wapi.config.get_modules()
            words = [ dict(text = o) for o in modules ]
            return words
        elif word_for_completion == '--params':
            # 参数补全
            module_name = wapi.module_name
            request = wapi.config.get_module(module_name
                ).get_request(wapi.request_name)
            params = request.params or {}
            words = self._dict_to_completions(params)
            return words
        elif word_for_completion == '--json':
            # 参数补全
            module_name = wapi.module_name
            request = wapi.config.get_module(module_name
                ).get_request(wapi.request_name)
            params = request.json or {}
            words = self._dict_to_completions(params)
            return words

        return super().get_completions_after_argument(wapi, word_for_completion)

    def _dict_to_completions(self, data):
        words = []
        for k, v in data.items():
            words.append(dict(
                text = '{}='.format(k),
                display = '{}={}'.format(k, v),
                display_meta=''))
        return words
