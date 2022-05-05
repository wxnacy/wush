import multiprocessing as mp
from wush.argument.run import (
    RunArgumentParser, run_in_shell
)
from wush.cli.server import run_server
from wush.config.models import RequestModel

CONFIG_PATH = 'tests/data/config/config.yml'

#  p = mp.Process(target=run_server,
    #  kwargs={"config_path": CONFIG_PATH}, daemon=True)

#  def setup_module(module):
    #  """
    #  这是一个module级别的setup，它会在本module(test_website.py)里
    #  所有test执行之前，被调用一次。
    #  注意，它是直接定义为一个module里的函数"""
    #  p.start()


#  def teardown_module(module):
    #  """
    #  这是一个module级别的teardown，它会在本module(test_website.py)里
    #  所有test执行完成之后，被调用一次。
    #  注意，它是直接定义为一个module里的函数"""
    #  import time
    #  time.sleep(100)
    #  p.terminate()

def test_load_builder_from_request():
    req = RequestModel(
        name = 'test',
        url = 'https://wxnacy.com',
        method = 'GET',
        params = { "name": "wxnacy" },
        json = { "name": "wxnacy" },
        headers = { "name": "wxnacy" },
        cookies = { "name": "wxnacy" },
    )

    builder = RunArgumentParser._load_builder_from_request(req)
    assert builder.url == req.url
    assert builder.method == req.method
    assert builder.params == req.params.dict()
    assert builder.json_data == req.json_data.dict()
    assert builder.headers == req.headers
    assert builder.cookies == req.cookies
    has_version = True if builder.version else False
    assert has_version


#  def test_run_in_shell():
    #  res = run_in_shell('wush', 'test',
        #  config = CONFIG_PATH)
    #  print(res)
