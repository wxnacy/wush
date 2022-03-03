#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""
run 命令的参数解析
"""
import os
from csarg import Action
from csarg import CommandArgumentParserFactory

from wush.common import utils
from wush.common.constants import Constants
from wush.common.utils import run_shell
from wush.common.loggers import create_logger
from wush.common.run_mode import RUN_MODE
from wush.common.config_value import environ_keys
from wush.config import load_config
from wush.web.request import RequestClient
from wush.web.request import RequestBuilder
from wush.web.response import ResponseHandler
from wush.web.history import History

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
        item.add_argument('-m', '--module', help='模块名称')
        item.add_argument('-s', '--space', help='空间名称')
        item.add_argument('-n', '--name', help='请求名称')
        item.add_argument('-c', '--config', help='配置地址')
        item.add_argument('--attr', help='属性信息，自定义')
        item.add_argument('--params', action = Action.APPEND.value,
            help='请求地址参数')
        item.add_argument('--json', action = Action.APPEND.value,
            help='请求 body 参数，json 格式')
        item.add_argument('--env', action = Action.APPEND.value,
            help='传递环境变量')
        item.add_argument('--open', action = Action.STORE_TRUE.value,
            help = '是否通过浏览器打开请求结果')
        item.add_argument('--curl', action = Action.STORE_TRUE.value,
            help = '是否使用 curl 文本')
        item.add_argument('--with-browser-cookie',
            action = Action.STORE_TRUE.value,
            help = '是否使用 curl 文本')
        item.add_argument('--no-handle-response',
            action = Action.STORE_TRUE.value,
            help = '不对 response 做处理')
        item.add_argument('--no-browser',
            action = Action.STORE_TRUE.value,
            help = '不使用浏览器打开结果页面')
        if RUN_MODE.is_command:
            item.add_argument('--url', help='请求地址')

        #  item.config = load_config()

        return item

    def get_completions_after_argument(self, word_for_completion):
        """
        获取补全的单词列表
        :param word_for_completion: 补全需要的单词
        """
        self.config = load_config()
        words = []
        if not self.argument:
            return words
        arg = self.argument
        if word_for_completion == '--name':
            # 针对 --name 参数的自动补全
            requests = self.config.get_requests(arg.module)
            words = []
            for req in requests:
                words.append(dict( text = req.name, display_meta=req.title))
            return words
        elif word_for_completion == '--module':
            modules = self.config.get_modules()
            words = [ dict(text = o.name) for o in modules ]
            return words
        elif word_for_completion == '--params':
            # 参数补全
            request = self.config.get_request(arg.module, arg.name)
            params = request.params.to_dict()
            words = self._dict_to_completions(params)
            return words
        elif word_for_completion == '--json':
            # 参数补全
            request = self.config.get_request(arg.module, arg.name)
            words = self._dict_to_completions(request.json.to_dict())
            return words
        elif word_for_completion == '--env':
            # 环境变量
            # 使用当前请求的环境变量 keys 做补全
            request = self.config.get_request(arg.module, arg.name,
                    set_env=False)
            keys = environ_keys(request)
            self.logger.info(request.path)
            self.logger.info(
                f'request {arg.module} {arg.name} environ_keys {keys}')
            data = { f"{o}": "" for o in keys }

            words = self._dict_to_completions(data)
            return words

        return super().get_completions_after_argument(word_for_completion)

    def _dict_to_completions(self, data):
        """字典转为自动补全信息"""
        words = []
        for k, v in data.items():
            words.append(dict(
                text = '{}='.format(k),
                display = '{}={}'.format(k, v),
                display_meta=''))
        return words

    def run_command(self, text):
        """运行命令行模式"""
        self.config = load_config()
        args = self.parse_args(text)
        # curl 模式下打开一个文件并输入文本供后续使用
        builder = RequestBuilder()
        builder.set_run_mode(RUN_MODE.mode)
        if args.curl:
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
        builder.argument = args

        self.logger.info('builder {}'.format(builder.to_dict()))

        req_client = RequestClient(builder)
        res = req_client.request()
        self._run(args, builder, res)

    def _get_request_builder(self, args):
        """获取请求构造体"""
        params = utils.list_key_val_to_dict(args.params or [])
        json_data = utils.list_key_val_to_dict(args.json or [])
        environs = utils.list_key_val_to_dict(args.env or [])
        self.logger.info('arg params %s', params)
        self.logger.info('arg json %s', json_data)
        self.logger.info('arg env %s', environs)

        request_model = self.config.get_request(args.module, args.name,
                environs = environs)
        request_model.add_params(**params)
        request_model.add_json(**json_data)

        builder = RequestBuilder.loads_request_model(request_model,
            args.with_browser_cookie)
        builder.argument = args
        return builder

    def run_shell(self, text):
        self.config = load_config()
        args = self.parse_args(text)

        if not args.name:
            raise Exception

        builder = self._get_request_builder(args)
        builder.set_run_mode(RUN_MODE.mode)
        request_client = RequestClient(builder)

        self._print('Space: {}'.format(args.space))
        self._print('Module: {}'.format(args.module))
        self._print('Request: {}'.format(args.name))
        self._print('Url: {}'.format(builder.url))
        self._print('Params: {}'.format(builder.params))
        self._print('Json: {}'.format(builder.json))
        self._print('请求中。。。')

        res = request_client.request()

        self._print('Status: {}'.format(res.status_code))

        self._run(args, builder, res)

    def _run(self, args, builder, res):

        # 保存历史记录
        History().save(res)

        if args.open:
            self._print('See in browser')
            self._open(builder.version)
            return

        handler_func = ResponseHandler.get_handler(args.module,
            args.name)
        if handler_func and not args.no_handle_response:
            handler_func(res)
            return

        self.config.function.handler_response( res)

    def _open(self, version):
        #  """打开请求信息"""
        port = self.config.server_port
        url = f"http://localhost:{port}/api/version/{version}"
        utils.open_url(url)
