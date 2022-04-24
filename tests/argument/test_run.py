from wush.argument.run import RunArgumentParser
from wush.config.models import RequestModel



def test_load_builder_from_request():
    req = RequestModel(
        url = 'https://wxnacy.com',
        method = 'GET',
        params = { "name": "wxnacy" },
        json = { "name": "wxnacy" },
        headers = { "name": "wxnacy" },
        cookies = { "name": "wxnacy" },
    )
    req.format()

    builder = RunArgumentParser._load_builder_from_request(req)
    assert builder.url == req.url
    assert builder.method == req.method
    assert builder.params == req.params.to_dict()
    assert builder.json_data == req.json.to_dict()
    assert builder.headers == req.headers
    assert builder.cookies == req.cookies
    has_version = True if builder.version else False
    assert has_version
