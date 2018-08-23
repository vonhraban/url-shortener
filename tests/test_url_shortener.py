import pytest
from falcon import testing
from url_shortener.app import init
import json

@pytest.fixture()
def client():
    return testing.TestClient(init())


def test_shorten_url(client):
    # add a url
    original_url = 'http://google.com'
    body = json.dumps({
        'url': original_url
    })

    result = client.simulate_post('/', body=body)
    assert result.status_code == 201
    key = result.json['key']

    # retrieve the url
    result = client.simulate_get('/' + key)
    assert result.status_code == 301
    retrieved_url = result.json['moved']
    assert retrieved_url == original_url


def test_unknown_key(client):
    result = client.simulate_get('/unknown-key')
    assert result.status_code == 404



def test_broken_payload(client):
    result = client.simulate_post('/', body='invalid-json')
    assert result.status_code == 400
    assert result.json['error'] == "Invalid JSON provided"

    result = client.simulate_post('/', body=json.dumps({
        'unknown-key': 'some-value'
    }))
    assert result.status_code == 400
    assert result.json['error'] == "`url` parameter is required"
