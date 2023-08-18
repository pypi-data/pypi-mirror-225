from unittest.mock import MagicMock

import pytest
from django.http import HttpRequest

from autoapi.auth.interface import IAuthProvider
from tests.client import JSONClient
from tests.utils import install_django


@pytest.fixture
def client():
    install_django('tests.django_proj.settings.auth')
    return JSONClient()


@pytest.fixture
def client_custom_provider():
    install_django('tests.django_proj.settings.auth_custom_provider')
    return JSONClient()


def test_no_auth(client: JSONClient):
    response = client.get('/auth/get_user/')
    assert response.status_code == 200
    response = response.json()
    assert response['result'] is None


def test_auth(client: JSONClient):
    client.login(username='admin', password='admin')
    response = client.get('/auth/get_user/')
    assert response.status_code == 200
    response = response.json()
    result = response['result']
    assert result is not None
    assert result['username'] == 'admin'


def test_bad_credentials_auth(client: JSONClient):
    client.login(username='admin1', password='admin')
    response = client.get('/auth/get_user/')
    assert response.status_code == 200
    response = response.json()
    result = response['result']
    assert result is None


def test_default_auth_provider_no_auth(client: JSONClient):
    user_var_mock = MagicMock()
    from tests.django_proj.api.auth import api
    api.container.auth_provider.user_context_var = user_var_mock
    client.get('/auth/get_user/')
    assert len(user_var_mock.mock_calls) == 1
    call = user_var_mock.mock_calls[0]
    assert call.set is not None
    assert call.args[0] is None


def test_default_auth_provider_with_auth(client: JSONClient):
    user_var_mock = MagicMock()
    from tests.django_proj.api.auth import api
    api.container.auth_provider.user_context_var = user_var_mock
    client.login(username='admin', password='admin')
    client.get('/auth/get_user/')
    assert len(user_var_mock.mock_calls) == 1
    call = user_var_mock.mock_calls[0]
    assert call.set is not None
    assert call.args[0].__class__.__name__ == 'User'


def test_custom_auth_provider(client_custom_provider: JSONClient):
    response = client_custom_provider.get('/auth/get_user/')
    assert response.status_code == 200
    json = response.json()
    result = json['result']
    assert result['id'] == -44
    assert result['username'] == 'Testman'
