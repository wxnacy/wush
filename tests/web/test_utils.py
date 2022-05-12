
from wush.web import utils


def test_telnet():
    assert utils.telnet('localhost', 6666)
    assert not utils.telnet('localhost', 9999)
