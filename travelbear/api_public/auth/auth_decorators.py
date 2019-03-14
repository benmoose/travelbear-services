import functools
import logging
from pathlib import Path

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from django.conf import settings
from jwt import decode
from jwt.exceptions import InvalidTokenError

from common.request import get_authorization_header
from common.response import error_response
from db_layer.user import get_or_create_user

logger = logging.getLogger(__name__)

CERTIFICATE_NAME = "travel-bear.pem"
CERTIFICATE_FILE_PATH = Path(__file__).parent / CERTIFICATE_NAME

TEST_ENVIRONMENT_TEST_USER_SUB_HEADER = "HTTP_TEST_USER_EXTERNAL_ID"

AUDIENCE_NAME = getattr(settings, "API_AUDIENCE_NAME")


def require_jwt_auth(_func=None, *, public_key=None):
    if public_key is None:
        public_key = get_public_key_from_certificate_file(CERTIFICATE_FILE_PATH)

    def decorator_require_jwt_auth(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            if settings.IS_TEST_ENVIRONMENT:
                user = get_user_from_test_user_header(request.META)
                if user is not None:
                    request.user = user
                    return func(request, *args, **kwargs)

            auth_header = get_authorization_header(request.META)
            logger.info("request has auth header '%s'", auth_header)
            if auth_header is None:
                return error_response(
                    status=401, message="Missing authorization header"
                )

            token = get_token_from_authorization_header(auth_header)

            try:
                claims = decode(
                    token, public_key, algorithms="RS256", audience=AUDIENCE_NAME
                )
                user, created = get_or_create_user(claims["sub"])
            except (InvalidTokenError, KeyError) as e:
                logger.info("Failed to decode authorization token: %s", e)
                return error_response(status=401, message="Invalid authorization token")

            if created:
                logger.info(
                    "First time user with external_id '%s' has authenticated",
                    claims["sub"],
                )

            request.user = user
            return func(request, *args, **kwargs)

        return wrapper

    if _func is None:
        return decorator_require_jwt_auth
    else:
        return decorator_require_jwt_auth(_func)


def get_public_key_from_certificate_file(certificate_file):
    certificate = read_certificate_from_file(certificate_file)
    public_key = certificate.public_key()
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def read_certificate_from_file(certificate_file):
    with open(certificate_file, "rb") as f:
        certificate = f.read()
        return load_pem_x509_certificate(certificate, default_backend())


def get_user_from_test_user_header(request_headers):
    mock_user_sub = request_headers.get(TEST_ENVIRONMENT_TEST_USER_SUB_HEADER)
    if mock_user_sub is None:
        return None
    user, _ = get_or_create_user(mock_user_sub)
    return user


def get_token_from_authorization_header(authorization_header):
    """
    >>> get_token_from_authorization_header('Bearer: foo')
    'foo'
    >>> get_token_from_authorization_header('  bearer:      bar')
    'bar'
    >>> get_token_from_authorization_header('Bearer:') is None
    True
    >>> get_token_from_authorization_header('foo') is None
    True
    """
    try:
        bearer, token = authorization_header.split(":")
        token = token.strip()
        return token if len(token) > 0 else None
    except ValueError:
        return None
