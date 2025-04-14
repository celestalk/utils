from uutils.utypes import Url

def test_url():
    url = Url('http://localhost:8080')
    assert url == 'http://localhost:8080'
    assert url.p.scheme == 'http'
    assert url.p.port == 8080