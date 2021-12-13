#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy(wxnacy@gmail.com)
"""

"""

import pytest

from wush.web.curl_utils import cUrl

def test_curl_to_request_kwargs():

    text = 'test'
    with pytest.raises(ValueError) as excinfo:
        cUrl.dumps(text)
        assert str(excinfo) == 'A curl command must start with "curl"'

    text = 'curl -X post https://wxnacy.com'
    res = cUrl.dumps(text)

    assert res['method'] == 'POST'
    assert res['url'] == 'https://wxnacy.com'

    res = cUrl.dump('tests/web/curl_text')

    assert res['url'] == 'https://collector.githubapp.com/github/collect'
    assert res['headers']['Content-Type'] == 'text/plain;charset=UTF-8'
