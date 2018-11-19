from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key
from cryptography.hazmat.backends import default_backend
from django.http import HttpResponse
from django.test import RequestFactory
import jwt
import pytest

from .auth_decorators import require_jwt_auth


test_private_key = generate_private_key(65537, 2048, default_backend())
test_public_key = test_private_key.public_key()


def make_jwt_token(sub='test-sub', valid=True):
    if valid:
        return jwt.encode({'sub': sub}, test_private_key, algorithm='RS256')
    return jwt.encode({'sub': sub}, test_private_key, algorithm='RS256', headers={'exp': 1000})


@pytest.fixture
def request_factory():
    return RequestFactory()


@require_jwt_auth(public_key=test_public_key)
def protected_endpoint(request, expected_user=None):
    assert request.user == expected_user
    return HttpResponse()


@pytest.mark.parametrize('authorization', (
    '',
    'foo',
    'Bearer: foo',
    f'Bearer: {make_jwt_token(valid=False)}',
))
def test_require_jwt_auth_not_authenticated(request_factory, authorization):
    request = request_factory.get('/', HTTP_AUTHORIZATION=authorization)
    response = protected_endpoint(request)
    assert response.status_code == 401


def test_require_jwt_auth_authenticated(request_factory):
    token = make_jwt_token(sub='test-sub')
    authorization = f'Bearer: {token.decode()}'

    request = request_factory.get('/', HTTP_AUTHORIZATION=authorization)
    result = protected_endpoint(request, expected_user='test-sub')
    assert result.status_code == 200
