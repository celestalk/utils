import pytest
from uutils import uconfig

@pytest.fixture
def serialized():
    return {
        'client': {
            'url': 'http://example.com',
            'timeout': 10,
        },
        'templates': [
            {
                'name': 'alfa',
                'path': '/alfa',
                'chars': None,
            },
            {
                'name': 'omega',
                'path': '/omega',
                'chars': ['a', 'b', 'c'],
            }
        ]
    }

def test_uconfig(serialized):
    conf = uconfig.Config(serialized)
    assert conf
    assert conf.client
    assert conf.client.url == 'http://example.com'
    assert conf.client.timeout == 10
    assert tuple(conf.client) == ('url', 'timeout')
    assert len(conf.client) == 2
    assert dict(url='http://example.com', timeout=10) == dict(**conf.client)

    assert conf.templates
    assert conf.templates[0]
    assert conf.templates[0].name == 'alfa'
    assert conf.templates[0].path == '/alfa'
    assert conf.templates[1]
    assert conf.templates[1].name == 'omega'
    assert conf.templates[1].path == '/omega'
    assert tuple(conf.templates) == (conf.templates[0], conf.templates[1])
    assert len(conf.templates) == 2
    assert dict(name='alfa', path='/alfa', chars=None) == dict(**conf.templates[0])
    assert dict(name='omega', path='/omega', chars=['a', 'b', 'c']) == dict(**conf.templates[1])

    assert dict(**conf) == serialized


def test_uconfig_exception():
    nested_arrays = {
        'a':10,
        'b': [
            {'s': 500},
            [
                {'q': 200},
                {'w': 300},
            ]
        ],
    }

    with pytest.raises(ValueError, match="Nested arrays"):
        uconfig.Config(nested_arrays)

