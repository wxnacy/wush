#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wxnacy@gmail.com
"""

"""

import pytest

from wapi.common import utils
from wapi.common.exceptions import JsonException


def test_filter_json():
    data = { "id": 1, "name": "wxnacy" }
    res = utils.filter_json(data, ['{"name"}'])
    data.pop('id')
    assert res, data

    data = { "id": 1, "name": "wxnacy" }
    with pytest.raises(JsonException) as excinfo:
        utils.filter_json(data, ['"name"}'])
