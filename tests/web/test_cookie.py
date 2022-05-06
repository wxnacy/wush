

from wush.web.cookie import Cookie

def test_get_brower_cookie():
    cookies = Cookie.get_browser_cookie('.baidu.com', '.google.com')
    print(cookies)
    baidu_id = cookies.get('BAIDUID')
    assert baidu_id

    baidu_id = cookies.get('OGPC')
    assert baidu_id

    cookie = Cookie()
    cookies = cookie.get_cookies('.baidu.com', '.google.com')
    print(cookies)
    baidu_id = cookies.get('BAIDUID')
    assert baidu_id

    baidu_id = cookies.get('OGPC')
    assert baidu_id
