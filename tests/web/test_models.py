import pytest

from wush.web.models import Header

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

