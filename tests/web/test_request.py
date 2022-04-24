
import pytest
from wush.web.request import RequestBuilder
from wush.config.models import RequestModel

#  def test_load_curl():

    #  builder = RequestBuilder.load_curl('tests/web/curl_text')
    #  assert builder.version != None
    #  assert builder.method == 'GET'
    #  assert builder.url == 'https://collector.githubapp.com/github/collect'
    #  #  assert builder.params == 'https://collector.githubapp.com/github/collect'

def test_check_and_format_method():
    with pytest.raises(ValueError):
        RequestBuilder(url = 'test', method = 'ss')

    builder = RequestBuilder(url = 'test', method = 'get')
    assert builder.method == 'GET'

def test_root_validatory():
    builder = RequestBuilder(
        url = 'test',
        method = 'get',
        json = { "name": "wxnacy" }
    )

    assert builder.json_data == { "name": "wxnacy"  }
