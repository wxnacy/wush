import pytest

from wush.web.models import Header
from wush.web import RequestBuilder

def test_header():

    data = {
        "Content-Type": "application/json",
        "X-Id": 1
    }

    header = Header(**data)
    assert header.content_type == data['Content-Type']
    assert header['X-Id'] == data['X-Id']
    assert header.get('X-Id') == data['X-Id']
    assert not header.get('U-Id')

    with pytest.raises(KeyError):
        header['U-Id']

    with pytest.raises(AttributeError):
        header.id = 1

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
