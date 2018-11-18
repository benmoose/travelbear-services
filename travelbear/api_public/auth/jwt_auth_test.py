import pytest

from django.test import RequestFactory
from django.http import HttpRequest

from .jwt_auth import require_jwt_auth


@require_jwt_auth
def protected_function(request, expected_user):
    assert request.user == expected_user
    assert isinstance(request, HttpRequest)


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.mark.parametrize('authorization', (
    '',
    'foo',
    'Bearer: foo',
    'Bearer: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
    '.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ'
    '.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
))
def test_require_jwt_auth_not_authenticated(request_factory, authorization):
    request = request_factory.get('/', HTTP_AUTHORIZATION=authorization)
    protected_function(request, expected_user=None)
