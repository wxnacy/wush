#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""
import os
#  import subprocess
from wpy.argument import Action
from wpy.argument import CommandArgumentParserFactory

from wush.common import utils
from wush.common.constants import Constants
from wush.common.functions import open_version
from wush.common.functions import run_shell
from wush.common.loggers import create_logger
from wush.common.run_mode import RUN_MODE
from wush.web.request import RequestClient
from wush.web.request import RequestBuilder

from .command import CmdArgumentParser

@CommandArgumentParserFactory.register()
class RunArgumentParser(CmdArgumentParser):
    cmd = 'run'
    logger = create_logger('RunArgumentParser')

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
        item.add_argument('--curl', action = Action.STORE_TRUE.value,
            help = '是否使用 curl 文本')
        if RUN_MODE.is_command:
            item.add_argument('--url', help='请求地址')

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
        try:
            wapi.init_config(
                module_name = arg.module,
                request_name = arg.name
            )
        except:
            pass
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

    def _run_command(self, args):
        """运行命令行模式"""
        # curl 模式下打开一个文件并输入文本供后续使用
        builder = RequestBuilder()
        if args.curl:
            print('curl')
            filepath = Constants.build_tmpfile('curl')
            run_shell(f'echo "# 请输入 cUrl 文本\n" > {filepath}')
            vim_cmd = f'vim {filepath}'
            os.system(vim_cmd)
            builder = RequestBuilder.load_curl(filepath)

        if args.url:
            builder.url = args.url
            builder.format()

        if args.name:
            builder = self._get_request_builder(args)

        self.logger.info('builder {}'.format(builder.to_dict()))

        req_client = RequestClient(builder)
        res = req_client.request()
        res.print()

    def _get_request_builder(self, args):
        """获取请求构造体"""
        params = utils.list_key_val_to_dict(args.params or [])
        json_data = utils.list_key_val_to_dict(args.json or [])

        self.wapi.build(
            space_name = args.space,
            module_name = args.module,
            request_name = args.name,
            params = params,
            json = json_data
        )
        self.logger.info('arg params %s', params)
        self.logger.info('arg json %s', json_data)
        return self.wapi.request_builder

    def run(self, text):
        args = self.parse_args(text)
        # 判断运行模式
        if RUN_MODE.is_command:
            self._run_command(args)
            return

        if not args.name:
            raise Exception

        self._get_request_builder(args)

        self._print('Space: {}'.format(self.wapi.space_name))
        self._print('Module: {}'.format(self.wapi.module_name))
        self._print('Request: {}'.format(self.wapi.request_name))
        self._print('Url: {}'.format(self.wapi.url))
        self._print('Params: {}'.format(self.wapi._request_data.get("params")))
        self._print('Json: {}'.format(self.wapi._request_data.get("json")))
        self._print('请求中。。。')

        self.wapi.request()

        self._print('Status: {}'.format(self.wapi.response.status_code))
        #  self._print('Response:')

        self.wapi.save()
        if args.open:
            self._print('See in browser')
            self._open()
        else:
            #  self._print(self.wapi.get_pertty_response_content())
            self.wapi.config.get_function().handler_response(
                self.wapi._request, self.wapi.response)

    def _open(self):
        #  """打开请求信息"""
        open_version(self.wapi.version, 'response')
