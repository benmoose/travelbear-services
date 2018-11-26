from unittest.mock import Mock

from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key
from cryptography.hazmat.backends import default_backend
from django.http import HttpResponse, HttpRequest
from django.test import RequestFactory
import jwt
import pytest

from .auth_decorators import require_jwt_auth


test_private_key = generate_private_key(65537, 2048, default_backend())
test_public_key = test_private_key.public_key()


def make_jwt_token(sub="test-sub", valid=True):
    payload = {"sub": sub}
    algorithm = "RS256"
    if not valid:
        return jwt.encode(
            payload, test_private_key, algorithm=algorithm, headers={"exp": 1000}
        )
    return jwt.encode(payload, test_private_key, algorithm=algorithm)


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.fixture
def get_request(request_factory):
    def _make_request_with_auth_header(auth_header):
        return request_factory.get("/", HTTP_AUTHORIZATION=auth_header)

    return _make_request_with_auth_header


@pytest.fixture
def mock_request_handler():
    return Mock(return_value=HttpResponse(status=200))


@pytest.mark.parametrize(
    "authorization",
    ("", "foo", "Bearer: foo", f"Bearer: {make_jwt_token(valid=False)}"),
)
def test_require_jwt_auth_not_authenticated(
    get_request, mock_request_handler, authorization
):
    protected_func = require_jwt_auth(mock_request_handler, public_key=test_public_key)
    response = protected_func(get_request(authorization))

    assert response.status_code == 401
    assert mock_request_handler.call_count == 0


def test_require_jwt_auth_authenticated(get_request, mock_request_handler):
    token = make_jwt_token(sub="test-sub")
    authorization = f"Bearer: {token.decode()}"

    protected_func = require_jwt_auth(mock_request_handler, public_key=test_public_key)
    response = protected_func(get_request(authorization))

    assert response.status_code == 200
    assert mock_request_handler.call_count == 1

    args, kwargs = mock_request_handler.call_args
    request_received = args[0]
    assert isinstance(request_received, HttpRequest)
    assert getattr(request_received, "user") == "test-sub"
