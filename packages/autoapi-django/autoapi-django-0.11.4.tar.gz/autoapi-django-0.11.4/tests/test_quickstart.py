import pytest

from tests.client import JSONClient
from tests.utils import install_django


@pytest.fixture
def client():
    install_django('tests.django_proj.settings.hello_world')
    return JSONClient()


def test_hello_world(client: JSONClient):
    status, response = client.post('/quick_start/hello/', {'name': 'John'})
    assert status == 200
    assert response['ok'] is True
    assert response['result']['message'] == 'Hello, John!'

    status, response = client.post('/quick_start/hello/', {'name': 'Michael'})
    assert status == 200
    assert response['ok'] is True
    assert response['error'] is None
    assert response['panic'] is None
    assert response['result']['message'] == 'Hello, Michael!'

    status, response = client.post('/quick_start/hello/', {'bad_key': 'Michael'})
    assert status == 200
    assert response['ok'] is False
    assert response['result'] is None
    assert response['panic'] is None
    assert response['error']['name'] == 'TypeError'
    assert response['error']['args'][0] == "QuickStartService.hello() missing 1 required positional argument: 'name'"
