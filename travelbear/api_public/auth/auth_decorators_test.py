import jwt
import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import generate_private_key
from django.test import RequestFactory

from db_layer.user import User, get_or_create_user

from .auth_decorators import AUDIENCE_NAME, require_jwt_auth

test_private_key = generate_private_key(65537, 2048, default_backend())
test_public_key = test_private_key.public_key()


def create_user(external_id):
    user, _ = get_or_create_user(external_id=external_id)
    return user


def make_jwt_token(sub="test-sub", valid=True):
    payload = {"sub": sub, "aud": AUDIENCE_NAME}
    algorithm = "RS256"
    if not valid:
        return jwt.encode(
            payload, test_private_key, algorithm=algorithm, headers={"exp": 1000}
        )  # exp in past
    return jwt.encode(payload, test_private_key, algorithm=algorithm)


@require_jwt_auth(public_key=test_public_key)
def protected_function(request):
    return request.user


@pytest.fixture
def request_factory():
    return RequestFactory()


@pytest.mark.parametrize(
    "authorization",
    ("", "foo", "Bearer: foo", f"Bearer: {make_jwt_token(valid=False)}"),
)
def test_require_jwt_auth_not_authenticated(request_factory, authorization):
    request = request_factory.get("/", HTTP_AUTHORIZATION=authorization)
    response = protected_function(request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_require_jwt_auth_authenticated(request_factory):
    user = create_user(external_id="test-sub")
    token = make_jwt_token(sub="test-sub")
    authorization = f"Bearer: {token.decode()}"

    assert len(User.objects.all()) == 1
    request = request_factory.get("/", HTTP_AUTHORIZATION=authorization)
    request_user = protected_function(request)
    assert len(User.objects.all()) == 1
    assert request_user == user


@pytest.mark.django_db
def test_user_created_if_not_in_db(request_factory):
    token = make_jwt_token(sub="test-sub")
    authorization = f"Bearer: {token.decode()}"

    assert len(User.objects.all()) == 0
    request = request_factory.get("/", HTTP_AUTHORIZATION=authorization)
    request_user = protected_function(request)
    assert len(User.objects.all()) == 1
    assert User.objects.get(external_id="test-sub") == request_user
