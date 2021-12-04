#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""
from collections import deque

from wpy.files import FileUtils
from wush.common.loggers import create_logger
from .command import CmdArgumentParser
from wpy.argument import CommandArgumentParserFactory

@CommandArgumentParserFactory.register()
class EnvArgumentParser(CmdArgumentParser):
    cmd = 'env'

    def get_completions_after_cmd(self, argument, words=None):
        words = []
        for k ,v in self.wapi.config.env.dict().items():
            text = '--{}'.format(k)
            display = '--{}={}'.format(k, v)
            words.append(dict(text = text, display = display))
        return super().get_completions_after_cmd(argument, words)

    def _make_args_dict(self, args):
        res = super()._make_args_dict(args)
        args = list(filter(lambda x: x != '--save', args))
        if len(args) < 3:
            return res
        # 将所有成对的参数都放入参数列表
        d_args = deque(args[1:])
        d_args.rotate(-1)
        for i, (k, v) in enumerate(zip(args[1:], d_args)):
            if i % 2  == 1 or not k.startswith('--'):
                continue
            k = k.replace('--', '')
            res[k] = v
        return res

    @classmethod
    def default(cls):
        """
        初始化一个实例
        """
        item = cls()
        item.add_argument('cmd')
        item.add_argument('--save', action='store_true')
        return item

    def run(self, args):
        """执行"""
        args = self.parse_args(args)
        if args.has_args():
            arg_names = [o.name for o in self.get_arguments()]
            for k, v in args.__dict__.items():
                if k not in arg_names:
                    self.wapi.config.env.add(**{ k: v })
                    print('{}={}'.format(k, v))
            self.wapi.init_config()
        else:
            for k, v in self.wapi.config.env.dict().items():
                print('{}={}'.format(k, v))

        # 保存数据
        if args.save:
            env_path = self.wapi.config.get_env_path()
            env_data = {}
            try:
                env_data = FileUtils.read_dict(env_path)
            except:
                pass
            for k, v in self.wapi.config.env.dict().items():
                if k in ('body_path',):
                    continue
                if k.isupper():
                    continue
                if not v:
                    continue
                if env_data.get(k) == v:
                    continue
                self.logger.info('Env save %s=%s', k, v)
                env_data[k] = v
            FileUtils.write_yml(env_path, env_data)

