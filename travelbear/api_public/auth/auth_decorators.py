import functools
import logging
from pathlib import Path

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from django.http import HttpResponse
from jwt import decode
from jwt.exceptions import InvalidTokenError

from common.request import get_authorization_header


logger = logging.getLogger(__name__)

CERTIFICATE_NAME = "travel-bear.pem"
CERTIFICATE_FILE_PATH = Path(__file__).parent / CERTIFICATE_NAME


def require_jwt_auth(_func=None, *, public_key=None):
    """
    This rejects requests without a valid JWT token in the authorization header.
    If invalid:
     - return HTTP 401
    If valid:
     - Populate request.user with the JWT's sub claim
    """
    if public_key is None:
        public_key = get_public_key_from_certificate_file()

    def decorator_require_jwt_auth(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            auth_header = get_authorization_header(request)

            if auth_header is None:
                return HttpResponse(status=401)

            token = get_token_from_authorization_header(auth_header)

            try:
                claims = decode(token, public_key, algorithms="RS256")
                request.user = claims["sub"]
            except InvalidTokenError:
                return HttpResponse(status=401)
            except KeyError:
                logger.warning("Got JWT with no sub claim: %s", token)
                return HttpResponse(status=401)
            return func(request, *args, **kwargs)

        return wrapper

    if _func is None:
        return decorator_require_jwt_auth
    else:
        return decorator_require_jwt_auth(_func)


def get_public_key_from_certificate_file(certificate_file=None):
    certificate_file = certificate_file or CERTIFICATE_FILE_PATH
    certificate = read_certificate_from_file(certificate_file)
    return certificate.public_key


def read_certificate_from_file(certificate_file):
    with open(certificate_file) as f:
        certificate = f.read().encode()
        return load_pem_x509_certificate(certificate, default_backend())


def get_token_from_authorization_header(authorization_header):
    """
    >>> get_token_from_authorization_header('Bearer: foo')
    'foo'
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