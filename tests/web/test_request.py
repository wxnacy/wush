
import pytest
from wush.web import RequestBuilder
from wush.web import RequestClient
from wush.config.models import RequestModel

#  def test_load_curl():

    #  builder = RequestBuilder.load_curl('tests/web/curl_text')
    #  assert builder.version != None
    #  assert builder.method == 'GET'
    #  assert builder.url == 'https://collector.githubapp.com/github/collect'
    #  #  assert builder.params == 'https://collector.githubapp.com/github/collect'


def test_request():
    builder = RequestBuilder(url = 'https://baidu.com')
    req = RequestClient(builder)
    res = req.request()
    assert res.is_html

