
import json
from wush.web import RequestClient
from wush.config.config import Config
from wush.argument.run import RunArgumentParser

TEST_CONFIG_PATH = 'tests/data/config/config.yml'

def test_response_client():
    test_config = Config.load(TEST_CONFIG_PATH)
    request_model = test_config.get_request('wush', 'test_get')
    request_builder = RunArgumentParser._load_builder_from_request(request_model)

    req = RequestClient(request_builder)
    res = req.request()

    assert isinstance(res.content, bytes)
    assert isinstance(res.text, str)

    assert res.json() == json.loads(res.content)
    assert res.json() == json.loads(res.text)

    assert res.headers.content_type == 'application/json'
    assert res.content_type == 'application/json'

    assert not res.is_html
    assert res.is_json


